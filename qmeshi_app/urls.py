from django.urls import path
from . import views

#appの各ページを設定

app_name = 'qmeshi_app'
urlpatterns = [
    path('', views.menu_list, name='menu_list'),   #メニュー一覧
    path('item/', views.item_list, name='item_list'),   #アイテム一覧
    path('impression/<int:item_id>/', views.ImpressionList.as_view(), name='impression_list'),  # 一覧
    path('impression/add/<int:item_id>/', views.impression_edit, name='impression_add'),        # 登録
]