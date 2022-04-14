import datetime
import sys

from django.http import HttpResponseServerError
from django.shortcuts import redirect
from django.views import debug
from django.views.decorators.csrf import requires_csrf_token
from django.views.generic import TemplateView

from qmeshi_app.models import Cafeteria, Menu


def default(request):
    return redirect('qmeshi_app:menu_list')


class MenuList(TemplateView):
    """今日のメニュー"""
    template_name = 'qmeshi_app/menu_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date = datetime.datetime.strptime(self.kwargs.get('date'), "%Y-%m-%d").date() if self.kwargs.get('date') else datetime.date.today()
        weekdays = ['月', '火', '水', '木', '金', '土', '日']
        context['date_str'] = f'{date.strftime("%m月%d日")}（{weekdays[date.weekday()]}）'
        context['date_current'] = date.strftime('%Y-%m-%d')
        context['date_prev'] = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        context['date_next'] = (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
        cafeterias = Cafeteria.objects.all().order_by('priority')
        cafeterias_with_menues = []
        for cafeteria in cafeterias:
            menues = Menu.objects.filter(start_date__lte=date, end_date__gte=date, cafeteria=cafeteria)
            menues_left = menues[:(menues.count()+1)//2]
            menues_right = menues[(menues.count()+1)//2:]
            cafeterias_with_menues.append({'cafeteria': cafeteria, 'menues_left': menues_left, 'menues_right': menues_right})
        context['cafeterias'] = cafeterias
        context['cafeterias_with_menues'] = cafeterias_with_menues
        return context


class About(TemplateView):
    """概要"""
    template_name = 'qmeshi_app/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cafeterias'] = Cafeteria.objects.all().order_by('priority')
        return context


# 本番環境でサーバーエラーの詳細を表示する関数
# 表示する場合はqmeshi/url.pyのコメントアウトをはずす
@requires_csrf_token
def my_customized_server_error(request, template_name='500.html'):
    error_html = debug.technical_500_response(request, *sys.exc_info()).content
    return HttpResponseServerError(error_html)
