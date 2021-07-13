#from django.shortcuts import render

# Create your views here.
import json
from collections import OrderedDict
from django.http import HttpResponse
from qmeshi_app.models import Item


def render_json_response(request, data, status=None):
    """response を JSON で返却"""
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    callback = request.GET.get('callback')
    if not callback:
        callback = request.POST.get('callback')  # POSTでJSONPの場合
    if callback:
        json_str = "%s(%s)" % (callback, json_str)
        response = HttpResponse(json_str, content_type='application/javascript; charset=UTF-8', status=status)
    else:
        response = HttpResponse(json_str, content_type='application/json; charset=UTF-8', status=status)
    return response


def menu_list(request):
    """JSONを返す"""
    items = []
    for item in Item.objects.all().order_by('id'):
        item_dict = OrderedDict([
            ('id', item.id),
            ('name', item.name),
        ])
        items.append(item_dict)

    data = OrderedDict([ ('items', items) ])
    return render_json_response(request, data)