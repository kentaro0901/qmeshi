from django.contrib import admin
from qmeshi_app.models import Menu, Item, Impression, Cafeteria

# adminに表示したいデータ

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'menu',)        #一覧
    list_display_links = ('id', 'start_date', 'end_date', 'menu',)  #修正可能

admin.site.register(Menu, MenuAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',) 
    list_display_links = ('id', 'name',)


admin.site.register(Item, ItemAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment',)
    list_display_links = ('id', 'comment',)
    raw_id_fields = ('item',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防）


admin.site.register(Impression, ImpressionAdmin)


class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') 
    list_display_links = ('id', 'name',)


admin.site.register(Cafeteria, CafeteriaAdmin)

