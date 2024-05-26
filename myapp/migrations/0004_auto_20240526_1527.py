# Generated by Django 3.2.25 on 2024-05-26 12:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20240525_0014'),
    ]

    operations = [
        migrations.AddField(
            model_name='flat',
            name='district',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='flat',
            name='metro',
            field=models.CharField(default='', max_length=100),
        ),
        migrations.AddField(
            model_name='flat',
            name='rooms',
            field=models.IntegerField(default=0),
        ),
    ]