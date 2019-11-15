# Generated by Django 2.2.7 on 2019-11-14 19:15

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0010_auto_20191114_1734'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='Receiver',
        ),
        migrations.AddField(
            model_name='transaction',
            name='Receivers',
            field=django_mysql.models.ListCharField(models.CharField(max_length=18), default=[], max_length=198, size=10),
        ),
    ]