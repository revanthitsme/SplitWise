# Generated by Django 2.2.7 on 2019-11-24 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dappx', '0022_auto_20191123_2252'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Button_name', models.CharField(max_length=25)),
                ('Group_name', models.CharField(max_length=20)),
                ('Donor', models.CharField(max_length=20)),
                ('Receivers_list', models.CharField(max_length=200)),
                ('Amount', models.FloatField(default=0)),
                ('Description', models.CharField(max_length=50)),
                ('Time', models.DateTimeField(auto_now_add=True)),
                ('Tag', models.CharField(default='other', max_length=15)),
            ],
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