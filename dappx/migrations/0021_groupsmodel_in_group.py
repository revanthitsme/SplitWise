# Generated by Django 2.2.7 on 2019-11-23 15:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0020_auto_20191123_2037'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupsmodel',
            name='in_group',
            field=models.BooleanField(default=True),
        ),
    ]
