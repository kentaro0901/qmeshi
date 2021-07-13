from django.urls import path
from api import views

app_name = 'api'
urlpatterns = [
    path('', views.menu_list, name='menu_list'), 
]