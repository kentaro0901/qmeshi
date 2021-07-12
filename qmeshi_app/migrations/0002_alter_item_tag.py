# Generated by Django 3.2.5 on 2021-07-12 13:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qmeshi_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tag', to='qmeshi_app.tag', verbose_name='種類'),
        ),
    ]
