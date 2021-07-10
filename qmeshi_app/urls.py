from django.urls import path
from . import views

#appの各ページを設定

app_name = 'qmeshi_app'
urlpatterns = [
    path('', views.menu_list, name='menu_list'),   #メニュー一覧
]