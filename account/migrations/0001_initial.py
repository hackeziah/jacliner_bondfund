# Generated by Django 3.0.4 on 2020-03-26 19:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(max_length=60, unique=True, verbose_name='email')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_user', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=50, verbose_name='Company Name')),
                ('description', models.CharField(default='', max_length=50, verbose_name='Company Description')),
                ('trash', models.BooleanField(default=0, verbose_name='Trash')),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_name', models.CharField(max_length=50, verbose_name='Position Name')),
                ('description', models.CharField(default='', max_length=50, verbose_name='Position Description')),
                ('trash', models.BooleanField(default=0, verbose_name='Trash')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('emp_no', models.CharField(max_length=200, unique=True, verbose_name='Employee No')),
                ('first_name', models.CharField(max_length=40, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=40, verbose_name='Last Name')),
                ('mobile_number', models.CharField(blank=True, max_length=10)),
                ('status', models.IntegerField(default='', verbose_name='Status')),
                ('trash', models.BooleanField(default=False, verbose_name='Trash')),
                ('date_created', models.DateTimeField()),
                ('date_modified', models.DateTimeField()),
                ('company_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Company')),
                ('position_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Position')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
    ]
