from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# データベース用クラス
# パラメータの追加は慎重に（特にnon-nullableの追加時とか）
# CASCADE 親が消えたら子も消す
# PROTECT 削除不可


# Tagを消せば全部消える
class Tag(models.Model):
    """種類"""
    name = models.CharField('種類', max_length=32)
    short_name = models.CharField('略記', max_length=32, null=True) #HTMLの属性に使う
    priority = models.IntegerField('表示優先度', default=1)

    def __str__(self):
        return self.name


class Item(models.Model):
    """アイテム"""
    tag = models.ForeignKey(Tag, verbose_name='種類', related_name='tag', on_delete=models.CASCADE, default=1)
    name = models.CharField('アイテム', max_length=64)

    def __str__(self):
        return self.name


class Cafeteria(models.Model):
    """食堂"""
    name = models.CharField('食堂名', max_length=32)
    short_name = models.CharField('略記', max_length=16, null=True)
    opening_hours = models.CharField('営業時間', max_length=128, default='-')
    table_num = models.IntegerField('テーブル番号', null=True)
    priority = models.IntegerField('表示優先度', default=1)

    def __str__(self):
        return self.name


class Menu(models.Model):
    """メニュー"""
    cafeteria = models.ForeignKey(Cafeteria, verbose_name='食堂', related_name='cafeteria', on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    period = models.CharField('時間帯', max_length=16, default='')
    item = models.ForeignKey(Item, verbose_name='アイテム', related_name='item', on_delete=models.CASCADE)

    def __str__(self):
        return self.item.name


class Impression(models.Model):
    """感想"""
    item = models.ForeignKey(Item, verbose_name='アイテム', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField('コメント', max_length=1024, blank=True)
    #score = models.IntegerField('評価', validators=[MinValueValidator(1), MaxValueValidator(5)], default= 3)

    def __str__(self):
        return self.comment
