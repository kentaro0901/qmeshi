# Generated by Django 3.2.5 on 2021-07-15 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0010_cafeteria_opening_hours'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='period',
            field=models.CharField(default='', max_length=16, verbose_name='時間帯'),
        ),
    ]