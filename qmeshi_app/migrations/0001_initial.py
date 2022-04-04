# Generated by Django 3.2.5 on 2021-09-24 07:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies: list = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cafeteria',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='食堂名')),
                ('short_name', models.CharField(
                    max_length=16, null=True, verbose_name='略記')),
                ('opening_hours', models.CharField(
                    default='-', max_length=128, verbose_name='営業時間')),
                ('table_num', models.IntegerField(
                    null=True, verbose_name='テーブル番号')),
                ('priority', models.IntegerField(default=1, verbose_name='表示優先度')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='アイテム')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='種類')),
                ('short_name', models.CharField(
                    max_length=32, null=True, verbose_name='略記')),
                ('priority', models.IntegerField(default=1, verbose_name='表示優先度')),
            ],
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('period', models.CharField(default='',
                 max_length=16, verbose_name='時間帯')),
                ('cafeteria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='cafeteria', to='qmeshi_app.cafeteria', verbose_name='食堂')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='item', to='qmeshi_app.item', verbose_name='アイテム')),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='tag', to='qmeshi_app.tag', verbose_name='種類'),
        ),
        migrations.CreateModel(
            name='Impression',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.TextField(blank=True,
                 max_length=1024, verbose_name='コメント')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='impressions', to='qmeshi_app.item', verbose_name='アイテム')),
            ],
        ),
    ]
