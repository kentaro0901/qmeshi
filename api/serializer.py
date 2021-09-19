from rest_framework import serializers

from qmeshi_app.models import *


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'  


class MenuSerializer(serializers.ModelSerializer):
    item = ItemSerializer()
    class Meta:
        model = Menu
        fields = ('cafeteria', 'item',)


class CafeteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafeteria
        fields = '__all__'
