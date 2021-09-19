import re
import datetime
import os
from unicodedata import name
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmeshi.settings')

import tweepy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import django
django.setup()

from qmeshi_app.models import Menu, Cafeteria, Item, Tag
from update_functions import *

today = datetime.date.today()

# タグ要約
tag_dict = {'C丼':'丼', 'HALA  L対応':'HALAL', 'HALAL  カレー':'HALAL', 'とり天・豚汁':'定食', 'カレー':'カレー', 'カレー  定番':'カレー', 'カレー定番':'カレー', 'カレー類（スープなし）':'カレー', 'クイック丼':'丼', 'サラダ/スープ':'副菜', 'スープ/サラダ他':'副菜', 'スープ・サラダ':'副菜', 'デザート':'その他', 'パスタ':'麺', 'ビーフ丼':'丼', 'プレートランチMスープ付':'定食', 'プレートランチSスープ付':'定食', 'ボール':'丼', 'マグロ丼':'丼', 'ランチ':'定食', '主菜  (焼･炒･煮)':'主菜', '主菜（揚）':'主菜', '主菜（魚）':'主菜', '丼':'丼', '丼他':'丼', '和麺定番  うどん':'麺', '固定うどん':'麺', '固定丼':'丼', '夕メニュー�@':'定食', '夕メニュー�A':'定食', '夜メニュー':'定食', '夜限定メニュー':'定食', '定番うどん':'麺', '定番カレー':'カレー', '定番丼':'丼', '定番（麺）':'麺', '定番：唐揚':'主菜', '定番：麻婆':'主菜', '定食':'定食', '手作りカレー':'カレー' ,'揚':'主菜', '揚げ':'主菜', '揚げ２':'主菜', '揚げ３':'主菜', '揚げ４':'主菜', '日替り定食':'定食', '日替アグリ定食':'定食', '日替定食':'定食', '炒め':'主菜', '焼・炒・煮':'主菜', '豚丼':'丼', '週替':'カレー', '週替1':'麺', '週替2':'麺', '週替3':'麺', '週替うどん':'麺', '週替うどん  (月・火・水）':'麺', '週替うどん  (木・金）':'麺', '週替うどん1':'麺', '週替うどん2':'麺', '週替わり':'カレー', '週替カレー':'カレー', '週替ラーメン  (月・火・水）':'麺', '週替ラーメン  (木・金）':'麺', '週替中華麺':'麺', '週替中華麺1':'麺', '週替中華麺2':'麺', '週替麺A':'麺', '週替麺B':'麺', '週替麺C':'麺', '週替麺D':'麺', '魚':'主菜', '魚丼':'丼', '魚丼1':'丼', '魚丼2':'丼', '鮭丼':'丼', '鶏/豚丼':'丼', '鶏丼':'丼', '鶏丼/豚丼':'丼', '鶏天定食':'定食', '麺定番':'麺', '麺定番  うどん':'麺', '麻婆系':'主菜'}
def summarized_tag(tag):
    if type(tag) != str:
        return 'その他'
    else:
        return tag_dict[tag] if tag in tag_dict else 'その他'

# ここ要検討
def summarized_menu(s):
    if type(s) != str:
        return s
    tmp = []
    for sep in s.split('/'):
        tmp.append(sep.replace('　', '').replace(' ','').replace('（','(').replace('）',')').replace('★', '').strip())
        #sep = re.sub(r'(\w+)(\(.+\))?', r'\1', sep)
    return '/'.join(tmp)

#最長共通部分列
def lcs(S, T):
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
    tag = Tag.objects.get(name=tag)
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
            item = Item(tag=tag, name=name)
            item.save()
    return item


# 生協
def seikyo_update(table_num:int):
    cafeteria = Cafeteria.objects.get(table_num=table_num)
    if Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria).exists():
        return

    new_menues_df = pd.read_html('http://www.coop.kyushu-u.ac.jp/shokudou/month_menu.html', flavor='bs4')
    menu_df = new_menues_df[table_num]

    for i in menu_df:
        if len(menu_df) < 3: # メニューがない（あとで変える）
            break
        if menu_df.isnull()[i][1] or not re.search(r'\d', menu_df[i][1]): #nanまたは数値を含まない
            continue
        try:
            w, s_d, e_d = re.findall(r'\d*/*\d+',menu_df[i][1])
        except:
            continue
        m = int(re.findall(r'\d', menu_df[i][0])[0])
        s_day = int(s_d.split('/')[-1])
        e_day = int(e_d.split('/')[-1])

        if s_day > e_day: #月の切り替わりあり
            s_month = m if w != '1' else m-1 if m > 1 else 12
            e_month = m if w == '1' else m+1 if m < 12 else 1
        else:
            s_month = e_month = m

        if s_month > e_month : #年の切り替わりあり
            s_year = today.year-1 if today.month == 1 else today.year
            e_year = today.year if today.month == 1 else today.year+1
        else:
            s_year = e_year = today.year

        start_date = datetime.date(s_year, s_month, s_day)
        end_date = datetime.date(e_year, e_month, e_day)

        # 更新
        for menu in menu_df[[0,i]][2:].dropna(how='any').drop_duplicates().iterrows():
            cafeteria = Cafeteria.objects.get(table_num=table_num)
            tag = summarized_tag(menu[1][0])
            menu = summarized_menu(menu[1][i])
            for m in menu.split('/'): #A/B
                item = flexible_get_item(tag=tag, name=m)                        
                new_menu = Menu(cafeteria=cafeteria, start_date=start_date, end_date=end_date, item=item)
                new_menu.save()


# 日替（生協）
def daily_update():
    cafeteria = Cafeteria.objects.get(short_name='daily')
    if Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria).exists():
        return

    monday = today-datetime.timedelta(days=today.weekday())
    monday_str = monday.strftime('%y%m%d')
    url = f'http://www.coop.kyushu-u.ac.jp/teishoku{monday_str}.html'
    dfs = pd.read_html(url, flavor='bs4')
    dfs = pd.concat([dfs[i][:1] for i in range(4, 10)]).reset_index().drop('index', axis=1)

    m = monday.month
    y = monday.year
    for index, item in dfs.iterrows():
        d = int(re.findall(r'\d+',item[0])[0])
        m = m if d != 1 or index == 0 else m+1 if m < 12 else 1 #月の切り替わり
        y = y if not (m == 1 and d == 1) else y+1 #年の切り替わり
        date = datetime.date(y, m, d)
        lunch = item[2].replace(' ', '').strip() if not item.isnull()[2] else '-' #-も登録されるのあとで直す
        dinner = item[5].replace(' ', '').strip() if not item.isnull()[5] else '-'

        lunch_item = flexible_get_item(tag='定食', name=lunch)
        lunch_menu = Menu(cafeteria=cafeteria, start_date=date, end_date=date, period='昼', item=lunch_item)
        lunch_menu.save()
        dinner_item = flexible_get_item(tag='定食', name=dinner)
        dinner_menu = Menu(cafeteria=cafeteria, start_date=date, end_date=date, period='夜', item=dinner_item)
        dinner_menu.save()
    return


# あじや
def ajiya_update():
    cafeteria = Cafeteria.objects.get(short_name='ajiya')
    if Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria).exists():
        return

    url = 'http://ajiya1.com/menu/daily/'
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'}
    response = requests.get(url, headers = headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    elems = soup.select('h2')[1]
    today_menu = elems.contents[0].split()

    y = today.year
    md = re.findall(r'\d+', today_menu[0])
    m, d = map(int, md)
    date = datetime.date(y, m, d)
    menu = today_menu[1]
    item = flexible_get_item(tag='弁当', name=menu)
    new_menu = Menu(cafeteria=cafeteria, start_date=date, end_date=date, item=item)
    new_menu.save()


#　理食
def rishoku_update():
    CK = os.environ['TWITTER_CK']
    CS = os.environ['TWITTER_CS']
    AT = os.environ['TWITTER_AT']
    AS = os.environ['TWITTER_AS']
    auth = tweepy.OAuthHandler(CK, CS)
    auth.set_access_token(AT, AS)
    api = tweepy.API(auth)
    cafeteria = Cafeteria.objects.get(short_name='rishoku')

    statuses = api.user_timeline(id='bigleaf201510') #毎日11:00すぎに昼定食，16:30すぎに夜定食をツイートする模様
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
                new_menu, _ = Menu.objects.update_or_create(cafeteria=cafeteria, start_date=today, end_date=today, period=period, item=item)


def delete_oldmenu():
    Menu.objects.filter(end_date__lt=today).delete()