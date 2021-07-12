from django.contrib import admin
from qmeshi_app.models import Menu, Item, Impression, Cafeteria, Tag

# adminに表示したいデータ

class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',) 
    list_display_links = ('id', 'name',)

admin.site.register(Tag, TagAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'start_date', 'end_date', 'item',)        #一覧
    list_display_links = ('id', 'start_date', 'end_date', 'item',)  #修正可能
    raw_id_fields = ('cafeteria', 'item',)

admin.site.register(Menu, MenuAdmin)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'name',) 
    list_display_links = ('id', 'tag', 'name',)
    raw_id_fields = ('tag',)

admin.site.register(Item, ItemAdmin)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'comment',)
    list_display_links = ('id', 'comment',)
    raw_id_fields = ('item',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防）


admin.site.register(Impression, ImpressionAdmin)


class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name') 
    list_display_links = ('id', 'name', 'short_name')


admin.site.register(Cafeteria, CafeteriaAdmin)

