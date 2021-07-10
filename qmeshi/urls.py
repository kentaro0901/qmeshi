from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('qmeshi_app.urls')),   #本体
    path('admin/', admin.site.urls),        #admin
    path('api/', include('api.urls')),      #API
]
