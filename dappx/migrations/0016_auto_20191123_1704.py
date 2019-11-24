# Generated by Django 2.2.7 on 2019-11-23 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dappx', '0015_auto_20191123_1416'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ftoftransaction',
            name='Group',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Groups',
            field=models.CharField(max_length=20),
        ),
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Group', models.CharField(max_length=20)),
                ('Amount', models.IntegerField(default=0)),
                ('Damount', models.IntegerField(default=0)),
                ('Description', models.CharField(max_length=50)),
                ('Tag', models.CharField(max_length=15)),
                ('Member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Member', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]