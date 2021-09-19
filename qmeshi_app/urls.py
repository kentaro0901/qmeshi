from django.urls import path
from . import views

app_name = 'qmeshi_app'
urlpatterns = [
    path('menues', views.MenuList.as_view(), name='menu_list'), # メニュー一覧
    path('items', views.ItemList.as_view(), name='item_list'), # アイテム一覧
    path('impressions/<int:item_id>/', views.ImpressionList.as_view(), name='impression_list'), # 感想一覧
    path('impressions/add/<int:item_id>/', views.ImpressionAdd.as_view(), name='impression_add'), # 感想登録
]