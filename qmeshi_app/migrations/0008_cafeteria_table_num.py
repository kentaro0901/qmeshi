# Generated by Django 3.2.5 on 2021-07-13 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0007_tag_short_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafeteria',
            name='table_num',
            field=models.IntegerField(null=True, verbose_name='テーブル番号'),
        ),
    ]