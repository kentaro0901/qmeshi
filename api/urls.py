# from django.urls import path
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register('cafeterias', views.CafeteriaViewSet)
router.register('menues', views.MenuViewSet)
router.register('items', views.ItemViewSet)
urlpatterns = router.urls
