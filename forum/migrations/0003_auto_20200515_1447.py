# Generated by Django 3.0.4 on 2020-05-15 06:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20200513_1210'),
    ]

    operations = [
        migrations.AddField(
            model_name='plate',
            name='hot',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='plate',
            name='market',
            field=models.IntegerField(default=0),
        ),
    ]