from django.db import models

# データベース用クラス

class Menu(models.Model):
    """メニュー"""
    start_date = models.DateField()
    end_date = models.DateField()
    menu = models.TextField('メニュー', max_length=1024, blank=True)

    def __str__(self):
        return self.menu


class Item(models.Model):
    """アイテム"""
    name = models.CharField('アイテム', max_length=255)

    def __str__(self):
        return self.name


class Impression(models.Model):
    """感想"""
    item = models.ForeignKey(Item, verbose_name='アイテム', related_name='impressions', on_delete=models.CASCADE)
    comment = models.TextField('コメント', max_length=1024, blank=True)

    def __str__(self):
        return self.comment


class Cafeteria(models.Model):
    """食堂"""
    name = models.CharField('食堂名', max_length=255)

    def __str__(self):
        return self.name


# データベース消すの若干手間なので最後にまとめてやる
class Book(models.Model):
    """書籍"""
    name = models.CharField('書籍名', max_length=255)
    publisher = models.CharField('出版社', max_length=255, blank=True)
    page = models.IntegerField('ページ数', blank=True, default=0)

    def __str__(self):
        return self.name
