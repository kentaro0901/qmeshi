import re
import datetime
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qmeshi.settings')

#import tweepy
import pandas as pd
import requests
from bs4 import BeautifulSoup
import django
django.setup()

from qmeshi_app.models import Menu, Cafeteria, Item, Tag
from update_functions import *

new_menues_df = pd.read_html('http://www.coop.kyushu-u.ac.jp/shokudou/month_menu.html', flavor='bs4')
today = datetime.date.today()


for table_num in range(3,13):

    menu_df = new_menues_df[table_num]

    for i in menu_df:
        if len(menu_df) < 3: # メニューがない（あとで変える）
            break
        if menu_df.isnull()[i][1] or not re.search(r'\d',menu_df[i][1]): #nanまたは数値を含まない
            continue
        w, s_d, e_d = re.findall(r'\d*/*\d+',menu_df[i][1])
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

   
        for menu in menu_df[[0,i]][2:].dropna(how='any').iterrows():
            cafeteria = Cafeteria.objects.get(table_num=table_num)
            tag = summarized_tag(menu[1][0])
            menu = summarized_menu(fit_string(menu[1][i]))
            for m in menu.split('/'): #A/B
                tag = Tag.objects.get(name=tag)

                try:
                    item = Item.objects.get(tag=tag, name=m)
                except:
                    r_items = Item.objects.filter(tag=tag, name__startswith=m[0])
                    flag = False
                    for r_item in r_items:
                        if max(len(r_item.name), len(m))-1 <= len(lcs(r_item.name, m)): #1文字以内の誤差なら同一とする
                            item = r_item
                            flag = True
                            break
                    if not flag:
                        item = Item(tag=tag, name=m)
                        item.save()
                    
                new_menu = Menu(cafeteria=cafeteria, start_date=start_date, end_date=end_date, item=item)
                new_menu.save()
