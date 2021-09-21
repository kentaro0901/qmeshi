import datetime

from rest_framework import viewsets

from qmeshi_app.models import *
from api.serializer import *


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_fields = ('tag',)
    http_method_names = ['get']


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today())
    serializer_class = MenuSerializer
    filter_fields = ('cafeteria',)
    http_method_names = ['get']


class CafeteriaViewSet(viewsets.ModelViewSet):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer
    http_method_names = ['get']

