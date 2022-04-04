import argparse
import datetime
import os
import re

import django
import pandas as pd
import requests
import tweepy
from bs4 import BeautifulSoup

from utils import lcs, get_string_width

# モデルの読み込み前に実行する必要がある
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmeshi.settings')
django.setup()

from qmeshi_app.models import Cafeteria, Item, Menu, Tag  # NOQA


def flexible_get_item(tag: str, name: str):
    """誤差1文字以内ならItem取得 それ以外はItem作成"""
    tag, _ = Tag.objects.get_or_create(name=tag)

    try:
        item = Item.objects.get(tag=tag, name=name)
    except Exception:
        candidate_items = Item.objects.filter(
            tag=tag, name__startswith=name[0])
        for candidate_item in candidate_items:
            if max(len(candidate_item.name), len(name))-1 <= len(lcs(candidate_item.name, name)):  # 1文字以内の誤差なら同一アイテムとみなす
                return candidate_item
        item = Item.objects.create(tag=tag, name=name)

    return item


def print_update_result(cafeteria_name, is_updated):
    num_of_tabs = max(2 - get_string_width(cafeteria_name) // 8, 0)
    tabs = '\t' * num_of_tabs
    result = '\033[32mupdated.\033[0m' if is_updated else '\033[31mskipped.\033[0m'
    print(f'{tabs}{result}')


# 生協
def seikyo_update(table_num: int):
    cafeteria = Cafeteria.objects.get(table_num=table_num)
    print(cafeteria.name, end='\t')
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        print_update_result(cafeteria.name, False)
        return

    new_menues_df = pd.read_html('http://www.coop.kyushu-u.ac.jp/shokudou/month_menu.html', flavor='bs4')
    menu_df = new_menues_df[table_num]

    for i in menu_df:
        # メニューが公開されていないなら終了
        if len(menu_df) < 3:
            print_update_result(cafeteria.name, False)
            return
        # メニューでない列（属性や金額など）はスルー
        if menu_df.isnull()[i][1] or not re.search(r'\d', menu_df[i][1]):
            continue

        try:
            week_num_str, start_day_str, end_day_str = re.findall(
                r'\d*/*\d+', menu_df[i][1])
        except Exception:
            continue
        month = int(re.findall(r'\d+', menu_df[i][0])[0])
        week_num = int(week_num_str)
        start_day = int(start_day_str.split('/')[-1])
        end_day = int(end_day_str.split('/')[-1])

        # 月の切り替わり（年の切り替わりは必ず休業なので発生しない）
        if start_day > end_day:
            start_month = month-1 if week_num == 1 else month
            end_month = month+1 if week_num >= 4 else month
        else:
            start_month = end_month = month

        start_date = datetime.date(today.year, start_month, start_day)
        end_date = datetime.date(today.year, end_month, end_day)

        # 更新
        for menu in menu_df[[0, i]][2:].dropna(how='any').drop_duplicates(subset=i).iterrows():
            cafeteria = Cafeteria.objects.get(table_num=table_num)
            tag = menu[1][0].replace(' ', '').replace('　', '')
            Menu.objects.create(cafeteria=cafeteria, start_date=start_date,
                                end_date=end_date, item=flexible_get_item(tag=tag, name=menu[1][i]))

    print_update_result(cafeteria.name, True)


# 日替（生協）
def daily_update():
    cafeteria = Cafeteria.objects.get(short_name='daily')
    print(cafeteria.name, end='\t')
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        print_update_result(cafeteria.name, False)
        return

    monday = today-datetime.timedelta(days=today.weekday())
    dfs = pd.read_html(
        f'http://www.coop.kyushu-u.ac.jp/teishoku{monday.strftime("%y%m%d")}.html', flavor='bs4')
    dfs = pd.concat([dfs[i][:1] for i in range(4, 10)]
                    ).reset_index().drop('index', axis=1)

    month = monday.month
    year = monday.year

    # 日々のメニューを取得
    for index, item in dfs.iterrows():
        # 祝日と休業日はスキップ
        if item[2][-1:] == '日' or '休業' in item[2]:
            continue

        day = int(re.findall(r'\d+', item[0])[0])
        if day == 1:  # 月の切り替わり
            month = month+1 if month < 12 else 1
        if month == 1 and day == 1:  # 年の切り替わり
            year = year+1
        date = datetime.date(year, month, day)

        if not item.isnull()[2]:
            lunch = item[2].replace(' ', '').replace('・', '\n・').strip()
            Menu.objects.create(cafeteria=cafeteria, start_date=date, end_date=date,
                                period='昼', item=flexible_get_item(tag='定食', name=lunch))
        if not item.isnull()[5]:
            dinner = item[5].replace(' ', '').replace('・', '\n・').strip()
            Menu.objects.create(cafeteria=cafeteria, start_date=date, end_date=date,
                                period='夜', item=flexible_get_item(tag='定食', name=dinner))

    print_update_result(cafeteria.name, True)


# あじや
def ajiya_update():
    cafeteria = Cafeteria.objects.get(short_name='ajiya')
    print(cafeteria.name, end='\t')
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        print_update_result(cafeteria.name, False)
        return

    response = requests.get('http://ajiya1.com/menu/daily/', headers={
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')
    elems = soup.select('h2')[1]
    menu = elems.contents[0].split()[1]
    item = flexible_get_item(tag='弁当', name=menu)
    Menu.objects.create(cafeteria=cafeteria,
                        start_date=today, end_date=today, item=item)

    print_update_result(cafeteria.name, True)


# 理食
def rishoku_update():
    cafeteria = Cafeteria.objects.get(short_name='rishoku')
    print(cafeteria.name, end='\t')

    # メモ：毎日11:00すぎに昼定食，16:30すぎに夜定食をツイートする模様
    statuses = api.user_timeline(user_id='bigleaf201510')
    for status in statuses:
        created_date = status.created_at.astimezone()
        if created_date.date() != today:
            print_update_result(cafeteria.name, True)
            break
        if '日替わり' not in status.text:  # ここ表記揺れが不安
            continue

        # 各メニューを取得
        for text in status.text.split():
            if '定食' in text:
                text = text.replace('：', ':').split(':')[-1]
                item = flexible_get_item(tag='定食', name=text)
                period = '昼' if created_date <= datetime.datetime(today.year, today.month, today.day, 13, 0, 0).astimezone() else '夜'
                Menu.objects.update_or_create(
                    cafeteria=cafeteria, start_date=today, end_date=today, period=period, item=item)


# Manly
def manly_update():
    cafeteria = Cafeteria.objects.get(short_name='manly')
    print(cafeteria.name, end='\t')

    # メモ：毎日11:00すぎにツイートする模様
    statuses = api.user_timeline(user_id='kyushuManly')
    for status in statuses:
        created_date = status.created_at+datetime.timedelta(hours=9)
        if created_date.date() != today:
            print_update_result(cafeteria.name, True)
            break
        if '日替わり' not in status.text:
            continue

        # 各メニューを取得
        for text in status.text.split():
            if '♕' in text:
                item = flexible_get_item(tag='メイン', name=text.replace('♕', ''))
                Menu.objects.update_or_create(
                    cafeteria=cafeteria, start_date=today, end_date=today, item=item)
            if '♔' in text or '♚' in text:
                item = flexible_get_item(
                    tag='プラスワンデザート', name=text.replace('♔', '').replace('♚', ''))
                Menu.objects.update_or_create(
                    cafeteria=cafeteria, start_date=today, end_date=today, item=item)


def delete_oldmenu(days=7):
    date = today - datetime.timedelta(days=days)
    Menu.objects.filter(end_date__lt=date).delete()
    print('\033[31moldmenu deleted.\033[0m')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--seikyo', action='store_true')
    parser.add_argument('--daily', action='store_true')
    parser.add_argument('--ajiya', action='store_true')
    parser.add_argument('--rishoku', action='store_true')
    parser.add_argument('--manly', action='store_true')
    parser.add_argument('--delete', action='store_true')

    args = parser.parse_args()
    today = datetime.date.today()
    CK = os.environ['TWITTER_CK']
    CS = os.environ['TWITTER_CS']
    AT = os.environ['TWITTER_AT']
    AS = os.environ['TWITTER_AS']
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)

    if args.seikyo:
        for i in range(3, 13):
            seikyo_update(table_num=i)
    elif args.daily:
        daily_update()
    elif args.ajiya:
        ajiya_update()
    elif args.rishoku:
        rishoku_update()
    elif args.manly:
        manly_update()
    elif args.delete:
        delete_oldmenu()
    else:
        for i in range(3, 13):
            seikyo_update(table_num=i)
        daily_update()
        ajiya_update()
        rishoku_update()
        manly_update()
        delete_oldmenu()
