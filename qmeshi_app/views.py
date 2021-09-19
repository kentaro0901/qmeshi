from django.shortcuts import render, get_object_or_404, redirect
#from django.http import HttpResponse
from django.views.generic import ListView, TemplateView, UpdateView, CreateView
from django.urls import reverse

from qmeshi_app.models import Cafeteria, Menu, Item, Impression, Tag
from qmeshi_app.forms import ImpressionForm

import datetime


class MenuList(TemplateView):
    """今日のメニュー"""
    template_name = 'qmeshi_app/menu_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = datetime.date.today()
        weekdays = ['月', '火', '水' , '木', '金', '土', '日']
        context['date'] = f'{today.strftime("%m月%d日")}（{weekdays[today.weekday()]}）'
        context['menues'] = Menu.objects.filter(start_date__lte=today, end_date__gte=today)
        context['cafeterias'] = Cafeteria.objects.all().order_by('priority')
        return context


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
    model = Impression

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['item_id'] = self.kwargs.get('item_id')
        return context


class ImpressionAdd(CreateView):
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
        return reverse('qmeshi_app:impression_list', kwargs={ 'item_id' : self.kwargs.get('item_id') })
