from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView

from qmeshi_app.models import Menu

import datetime

def menu_list(request):
    """メニュー一覧"""
    today = datetime.date.today()
    weekdays = ['月', '火', '水' , '木', '金', '土', '日']
    date = f'{today.strftime("%m月%d日")}（{weekdays[today.weekday()]}）'
    menues = Menu.objects.all().filter(start_date__lte=today, end_date__gte=today)
    menu_items = []
    for menu in menues:
        menu_items.extend(menu.menu.split('\n'))
    return render(request,'qmeshi_app/menu_list.html', {'date':date, 'menues':menu_items})
