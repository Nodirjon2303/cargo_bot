# Generated by Django 3.2.9 on 2021-11-21 12:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bot', '0002_auto_20211121_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cargo',
            name='image',
        ),
    ]
