from django.contrib import admin
from qmeshi_app.models import Menu, Item, Impression, Cafeteria, Tag

# adminに表示したいデータ


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'priority')
    list_display_links = ('name', 'short_name', 'priority')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'cafeteria', 'start_date', 'end_date', 'period', 'item',)  # 一覧
    list_display_links = ('start_date', 'end_date', 'period', 'item',)  # 修正可能
    raw_id_fields = ('cafeteria', 'item',)


class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'name',)
    list_display_links = ('tag', 'name',)
    raw_id_fields = ('tag',)


class ImpressionAdmin(admin.ModelAdmin):
    list_display = ('id', 'item', 'comment',)
    list_display_links = ('comment',)
    raw_id_fields = ('item',)   # 外部キーをプルダウンにしない（データ件数が増加時のタイムアウトを予防）


class CafeteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_name', 'opening_hours', 'table_num', 'priority')
    list_display_links = ('name', 'short_name', 'opening_hours', 'table_num', 'priority')


admin.site.register(Tag, TagAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Impression, ImpressionAdmin)
admin.site.register(Cafeteria, CafeteriaAdmin)
