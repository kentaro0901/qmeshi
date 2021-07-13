from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from django.views.generic.list import ListView

from qmeshi_app.models import Cafeteria, Menu, Item, Impression, Tag
from qmeshi_app.forms import ImpressionForm

import datetime

def menu_list(request):
    """メニュー一覧"""
    today = datetime.date.today()
    weekdays = ['月', '火', '水' , '木', '金', '土', '日']
    date = f'{today.strftime("%m月%d日")}（{weekdays[today.weekday()]}）'
    menues = Menu.objects.all().filter(start_date__lte=today, end_date__gte=today)

    cafeterias = Cafeteria.objects.all().order_by('priority')
    return render(request,'qmeshi_app/menu_list.html', {'date':date, 'cafeterias':cafeterias, 'menues':menues})


def item_list(request):
    """アイテム一覧"""
    tags = Tag.objects.all().order_by('priority')
    items = Item.objects.all().order_by('name')
    return render(request, 'qmeshi_app/item_list.html',  {'tags':tags, 'items': items})         


class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name='impressions'
    template_name='qmeshi_app/impression_list.html'
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        item = get_object_or_404(Item, pk=kwargs['item_id'])
        impressions = item.impressions.all().order_by('id')
        self.object_list = impressions

        context = self.get_context_data(object_list=self.object_list, item=item)    
        return self.render_to_response(context)


def impression_edit(request, item_id, impression_id=None):
    """感想の編集"""
    item = get_object_or_404(Item, pk=item_id) 
    impression = get_object_or_404(Impression, pk=impression_id) if impression_id else Impression()

    if request.method == 'POST':
        form = ImpressionForm(request.POST, instance=impression)
        if form.is_valid():
            impression = form.save(commit=False)
            impression.item = item
            impression.save()
            return redirect('qmeshi_app:impression_list', item_id=item_id)
    else:
        form = ImpressionForm(instance=impression)

    return render(request, 'qmeshi_app/impression_edit.html', dict(form=form, item_id=item_id, impression_id=impression_id))