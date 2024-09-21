# Generated by Django 5.1.1 on 2024-09-21 14:07

import django.contrib.auth.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Machine_Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(max_length=15)),
                ('capacity', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Review_Reserve',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)])),
                ('description', models.TextField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=255, unique=True)),
                ('phone', models.CharField(max_length=10)),
                ('password', models.TextField()),
                ('role', models.CharField(choices=[('cus', 'customer'), ('stf', 'staff'), ('mgr', 'manager')], default='cus')),
                ('status', models.BooleanField(default=1)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=10)),
                ('cost', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('status_available', models.IntegerField(default=1)),
                ('status_health', models.IntegerField()),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('machine_size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='laundry_model.machine_size')),
            ],
        ),
        migrations.CreateModel(
            name='Reserve_Machine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=6)),
                ('cost', models.IntegerField()),
                ('arrive_at', models.DateTimeField()),
                ('status', models.IntegerField(choices=[(0, 'waiting'), (1, 'workable'), (2, 'working'), (3, 'complete'), (4, 'retrivable')])),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('arrive_arrive', models.DateTimeField(null=True)),
                ('work_at', models.DateTimeField(null=True)),
                ('machine', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='laundry_model.machine')),
                ('machine_size', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='laundry_model.machine_size')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('service', models.ManyToManyField(related_name='reserve_service', to='laundry_model.service')),
            ],
        ),
        migrations.AddField(
            model_name='users',
            name='reserveMachine',
            field=models.ManyToManyField(through='laundry_model.Reserve_Machine', to='laundry_model.machine'),
        ),
    ]
