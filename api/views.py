import datetime
import json

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
    def post(self, request):
        cafeteria_name = json.loads(request.body).get('queryResult', dict()).get('parameters', dict()).get('cafeteria', 'main')
        today = datetime.date.today()
        cafeteria = Cafeteria.objects.get(short_name=cafeteria_name)
        menues = Menu.objects.filter(start_date__lte=today, end_date__gte=today, cafeteria=cafeteria)
        items = [menu.item.name for menu in menues]
        data = {
            'speech': f'今日の{cafeteria.name}のメニューは，{"，".join(items)}です．',
            'displayText': f'今日の{cafeteria.name}のメニューは，¥n{"¥n".join(items)}¥nです．',
        }
        return Response(data)
