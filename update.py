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

from qmeshi_app.models import Menu


new_menues_df = pd.read_html('http://www.coop.kyushu-u.ac.jp/shokudou/month_menu.html', flavor='bs4')
main = 3
menu_df = new_menues_df[main]
today = datetime.date.today()

for i in menu_df:
    if menu_df.isnull()[i][1]:
        continue
    w, s_d, e_d = re.findall(r'\d*/*\d',menu_df[i][1])
    m = int(menu_df[i][0].split()[1].replace("月",""))
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

    menu_str = ''
    for menu in menu_df[i][2:].dropna().drop_duplicates():
        menu_str += f'{menu}\n'

    new_menu = Menu(start_date=start_date, end_date=end_date, menu=menu_str)
    new_menu.save()