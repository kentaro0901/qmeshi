# Generated by Django 3.2.5 on 2021-07-12 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0004_alter_item_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='cafeteria',
            name='short_name',
            field=models.CharField(max_length=16, null=True, verbose_name='略記'),
        ),
    ]
