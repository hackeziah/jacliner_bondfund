# Generated by Django 3.0.4 on 2020-03-21 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bond_fund', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='userno',
            field=models.CharField(max_length=255, verbose_name='User No'),
        ),
    ]
