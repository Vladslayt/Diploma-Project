# Generated by Django 3.2.25 on 2024-05-26 12:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_auto_20240526_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flat',
            old_name='metro',
            new_name='underground',
        ),
    ]
