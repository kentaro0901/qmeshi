import datetime

from rest_framework import viewsets

from qmeshi_app.models import *
from api.serializer import *


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_fields = ('tag',)


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(start_date__lte=datetime.date.today(), end_date__gte=datetime.date.today())
    serializer_class = MenuSerializer
    filter_fields = ('cafeteria',)


class CafeteriaViewSet(viewsets.ModelViewSet):
    queryset = Cafeteria.objects.all()
    serializer_class = CafeteriaSerializer

