import re
import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmeshi.settings')

import tweepy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import django
django.setup()

from qmeshi_app.models import Menu, Cafeteria, Item, Tag


today = datetime.date.today()


def lcs(S, T):
    """最長共通部分列"""
    L1 = len(S)
    L2 = len(T)
    dp = [[0]*(L2+1) for i in range(L1+1)]

    for i in range(L1-1, -1, -1):
        for j in range(L2-1, -1, -1):
            r = max(dp[i+1][j], dp[i][j+1])
            if S[i] == T[j]:
                r = max(r, dp[i+1][j+1] + 1)
            dp[i][j] = r

    res = []
    i = 0; j = 0
    while i < L1 and j < L2:
        if S[i] == T[j]:
            res.append(S[i])
            i += 1; j += 1
        elif dp[i][j] == dp[i+1][j]:
            i += 1
        elif dp[i][j] == dp[i][j+1]:
            j += 1
    return ''.join(res)


def flexible_get_item(tag:str, name:str):
    """誤差1文字以内ならItem取得，それ以外はItem作成"""
    tag, _ = Tag.objects.get_or_create(name=tag)
    try:
        item = Item.objects.get(tag=tag, name=name)
    except:
        r_items = Item.objects.filter(tag=tag, name__startswith=name[0])
        flag = False
        for r_item in r_items:
            if max(len(r_item.name), len(name))-1 <= len(lcs(r_item.name, name)): #1文字以内の誤差なら同一
                item = r_item
                flag = True
                break
        if not flag:
            item = Item.objects.create(tag=tag, name=name)
    return item


# 生協
def seikyo_update(table_num:int):
    cafeteria = Cafeteria.objects.get(table_num=table_num)
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        return

    new_menues_df = pd.read_html('http://www.coop.kyushu-u.ac.jp/shokudou/month_menu.html', flavor='bs4')
    menu_df = new_menues_df[table_num]

    for i in menu_df:
        if len(menu_df) < 3: # メニューがない
            break
        if menu_df.isnull()[i][1] or not re.search(r'\d', menu_df[i][1]): # nanまたは数値を含まない
            continue

        try:
            w, s_d, e_d = re.findall(r'\d*/*\d+',menu_df[i][1])
        except:
            continue
        m = int(re.findall(r'\d+', menu_df[i][0])[0])
        s_day = int(s_d.split('/')[-1])
        e_day = int(e_d.split('/')[-1])

        if s_day > e_day: # 月の切り替わりあり
            s_month = m if w != '1' else m-1 if m > 1 else 12
            e_month = m if w == '1' else m+1 if m < 12 else 1
        else:
            s_month = e_month = m

        if s_month > e_month : # 年の切り替わりあり
            s_year = today.year-1 if today.month == 1 else today.year
            e_year = today.year if today.month == 1 else today.year+1
        else:
            s_year = e_year = today.year

        start_date = datetime.date(s_year, s_month, s_day)
        end_date = datetime.date(e_year, e_month, e_day)

        # 更新
        for menu in menu_df[[0,i]][2:].dropna(how='any').drop_duplicates(subset=i).iterrows():
            cafeteria = Cafeteria.objects.get(table_num=table_num)
            tag = menu[1][0].replace(' ', '').replace('　', '')   
            Menu.objects.create(cafeteria=cafeteria, start_date=start_date, end_date=end_date, item=flexible_get_item(tag=tag, name=menu[1][i]))


# 日替（生協）
def daily_update():
    cafeteria = Cafeteria.objects.get(short_name='daily')
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        return

    monday = today-datetime.timedelta(days=today.weekday())
    dfs = pd.read_html(f'http://www.coop.kyushu-u.ac.jp/teishoku{monday.strftime("%y%m%d")}.html', flavor='bs4')
    dfs = pd.concat([dfs[i][:1] for i in range(4, 10)]).reset_index().drop('index', axis=1)

    m = monday.month
    y = monday.year
    for index, item in dfs.iterrows():
        d = int(re.findall(r'\d+',item[0])[0])
        m = m if d != 1 or index == 0 else m+1 if m < 12 else 1 # 月の切り替わり
        y = y if not (m == 1 and d == 1) else y+1 # 年の切り替わり
        date = datetime.date(y, m, d)

        if not item.isnull()[2] and item[2][-1:]!='日':
            lunch = item[2].replace(' ', '').replace('・', '\n・').strip()
            Menu.objects.create(cafeteria=cafeteria, start_date=date, end_date=date, period='昼', item=flexible_get_item(tag='定食', name=lunch))
        if not item.isnull()[5]:
            dinner = item[5].replace(' ', '').replace('・', '\n・').strip()
            Menu.objects.create(cafeteria=cafeteria, start_date=date, end_date=date, period='夜', item=flexible_get_item(tag='定食', name=dinner))


# あじや
def ajiya_update():
    cafeteria = Cafeteria.objects.get(short_name='ajiya')
    if Menu.objects.filter(end_date__gte=today, cafeteria=cafeteria).exists():
        return

    response = requests.get('http://ajiya1.com/menu/daily/', headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
    soup = BeautifulSoup(response.content, 'html.parser')
    elems = soup.select('h2')[1]
    menu = elems.contents[0].split()[1]
    item = flexible_get_item(tag='弁当', name=menu)
    Menu.objects.create(cafeteria=cafeteria, start_date=today, end_date=today, item=item)


# 理食
def rishoku_update():
    CK = os.environ['TWITTER_CK']
    CS = os.environ['TWITTER_CS']
    AT = os.environ['TWITTER_AT']
    AS = os.environ['TWITTER_AS']
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    cafeteria = Cafeteria.objects.get(short_name='rishoku')

    # メモ：毎日11:00すぎに昼定食，16:30すぎに夜定食をツイートする模様
    statuses = api.user_timeline(id='bigleaf201510') 
    for status in statuses:
        created_date = status.created_at+datetime.timedelta(hours=9) 
        if created_date.date() != today:
            break
        if not '日替わり' in status.text:
            continue
        for text in status.text.split():
            if '定食' in text:
                text = text.split('：')[-1]
                item = flexible_get_item(tag='定食', name=text)
                period = '昼' if created_date <= datetime.datetime(today.year, today.month, today.day, 13, 0, 0) else '夜'
                Menu.objects.update_or_create(cafeteria=cafeteria, start_date=today, end_date=today, period=period, item=item)


def delete_oldmenu():
    Menu.objects.filter(end_date__lt=today).delete()