# Generated by Django 2.2.7 on 2019-11-24 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0023_auto_20191124_1647'),
    ]

    operations = [
        migrations.AddField(
            model_name='ftoftransaction',
            name='Date2',
            field=models.CharField(default='2019-11-25', max_length=25),
        ),
        migrations.AddField(
            model_name='transaction',
            name='Date2',
            field=models.CharField(default='2019-11-25', max_length=25),
        ),
        migrations.AddField(
            model_name='transaction',
            name='Expenditure',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='ftoftransaction',
            name='Tag',
            field=models.CharField(default='Others', max_length=15),
        ),
        migrations.AlterField(
            model_name='groupsmodel',
            name='Tag',
            field=models.CharField(default='Others', max_length=15),
        ),
    ]
