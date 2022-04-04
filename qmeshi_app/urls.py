from django.urls import path
from . import views

app_name = 'qmeshi_app'
urlpatterns = [
    path('', views.default),  # メニューにリダイレクト
    path('menues', views.MenuList.as_view(), name='menu_list'),  # メニュー一覧
    path('menues/<str:date>', views.MenuList.as_view(), name='menu_list'),  # 日付指定のメニュー一覧
    path('about', views.About.as_view(), name='about'),  # 概要
]
