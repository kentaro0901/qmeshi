from django.contrib import admin
from qmeshi_app.models import Menu

# adminに表示したいデータ

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'menu',)        #一覧
    list_display_links = ('id', 'start_date', 'end_date', 'menu',)  #修正可能

admin.site.register(Menu, MenuAdmin)