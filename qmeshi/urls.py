from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('qmeshi_app.urls')), # サイト
    path('admin/', admin.site.urls), # admin
    path('api/', include('api.urls')), # API
]

# サーバーエラーの詳細を表示する
from qmeshi_app import views

handler500 = views.my_customized_server_error