# Generated by Django 3.2.5 on 2021-07-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0006_delete_book'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='short_name',
            field=models.CharField(max_length=32, null=True, verbose_name='略記'),
        ),
    ]
