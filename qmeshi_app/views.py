from django.shortcuts import get_object_or_404
from django.views.generic import ListView, TemplateView, CreateView
from django.urls import reverse

from qmeshi_app.models import *

import datetime


class MenuList(TemplateView):
    """今日のメニュー"""
    template_name = 'qmeshi_app/menu_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.datetime.strptime(self.kwargs.get('date'), "%Y-%m-%d").date() if self.kwargs.get('date') else datetime.date.today()
        weekdays = ['月', '火', '水' , '木', '金', '土', '日']
        context['date'] = f'{date.strftime("%m月%d日")}（{weekdays[date.weekday()]}）'
        cafeterias = []
        for cafeteria in Cafeteria.objects.all().order_by('priority'):
            menues = Menu.objects.filter(start_date__lte=date, end_date__gte=date, cafeteria=cafeteria)
            l_menues = menues[:(menues.count()+1)//2]
            r_menues = menues[(menues.count()+1)//2:]
            cafeterias.append({'obj':cafeteria, 'l_menues':l_menues, 'r_menues':r_menues})  
        context['cafeterias'] = cafeterias
        return context


class About(TemplateView):
    """概要"""
    template_name = 'qmeshi_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cafeterias'] = Cafeteria.objects.all().order_by('priority')
        return context



# 以下後回し

class ItemList(ListView):
    """メニュー一覧"""
    context_object_name = 'items'
    template_name = 'qmeshi_app/item_list.html'
    model = Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags'] = Tag.objects.all().order_by('priority')
        return context


class ImpressionList(ListView):
    """感想の一覧"""
    context_object_name='impressions'
    template_name='qmeshi_app/impression_list.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_id'] = self.kwargs.get('item_id')
        return context

    def get_queryset(self):
        queryset = Impression.objects.filter(item=self.kwargs.get('item_id'))
        return queryset


class ImpressionAdd(CreateView):
    """感想の追加"""
    fields = ('comment',)
    model = Impression
    template_name = 'qmeshi_app/impression_add.html'

    def form_valid(self, form):
        form.instance.item = get_object_or_404(Item, pk=self.kwargs.get('item_id'))
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_id'] = self.kwargs.get('item_id')
        return context

    def get_success_url(self):
        return reverse('qmeshi_app:impression_list', kwargs={ 'item_id' : self.kwargs.get('item_id') }) # URL生成してるだけ
