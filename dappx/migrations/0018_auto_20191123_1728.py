# Generated by Django 2.2.7 on 2019-11-23 11:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0017_auto_20191123_1709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='groups',
            old_name='Group_name',
            new_name='Group',
        ),
    ]
