# Generated by Django 3.2.5 on 2021-07-10 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('menu', models.TextField(blank=True, verbose_name='メニュー')),
            ],
        ),
    ]
