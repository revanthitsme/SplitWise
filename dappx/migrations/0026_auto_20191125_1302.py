# Generated by Django 2.2.7 on 2019-11-25 07:32

from django.db import migrations, models
import django_mysql.models


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0025_auto_20191125_0341'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='shares',
            field=django_mysql.models.ListCharField(models.CharField(max_length=18), default=[], max_length=198, size=10),
        ),
        migrations.AlterField(
            model_name='activity',
            name='Amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='activity',
            name='Donor',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='ftoftransaction',
            name='Amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ftoftransaction',
            name='Damount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='groupsmodel',
            name='Amount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='groupsmodel',
            name='Damount',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='Amount',
            field=models.FloatField(default=0),
        ),
    ]
