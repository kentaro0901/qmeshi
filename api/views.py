import datetime

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response

from qmeshi_app.models import Item, Menu, Cafeteria
from api.serializer import ItemSerializer, MenuSerializer, CafeteriaSerializer


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


class GoogleAssistant(APIView):
    def get(self, request):
        cafeteria_id = int(request.GET.get('cafeteria', 0))
        today = datetime.date.today()
        cafeteria = Cafeteria.objects.get(id=cafeteria_id)
        menues = Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria)
        items = [menu.item.name for menu in menues]
        data = {
            'speech': '，'.join(items),
            'displayText': '¥n'.join(items),
            'source': ''
        }
        return Response(data)
