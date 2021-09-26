from rest_framework import serializers

from qmeshi_app.models import *


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'  


class ItemSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    class Meta:
        model = Item
        fields = '__all__'  


class CafeteriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cafeteria
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    cafeteria = CafeteriaSerializer()
    item = ItemSerializer()
    class Meta:
        model = Menu
        fields = ('cafeteria', 'item',)
