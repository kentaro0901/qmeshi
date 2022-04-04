from django.contrib import admin
from django.urls import path, include

# from qmeshi_app import views


urlpatterns = [
    path('', include('qmeshi_app.urls')),  # メインページ
    path('admin/', admin.site.urls),  # admin
    path('api/', include('api.urls')),  # API
]

# サーバーエラーの詳細を表示する
# handler500 = views.my_customized_server_error
