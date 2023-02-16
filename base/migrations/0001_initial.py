# Generated by Django 3.2.16 on 2023-02-07 10:38

import base.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(error_messages={'invalid': 'Enter a valid email address.', 'null': 'Email field is required.', 'unique': 'An account with that email already exists. Please login to continue.'}, max_length=127, unique=True, verbose_name='Email')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Full Name')),
                ('avatar', models.ImageField(blank=True, default=base.models.get_default_avatar, null=True, upload_to=base.models.get_user_avatar, verbose_name='Avatar')),
                ('is_email_verified', models.BooleanField(default=base.models.get_email_verified_value, help_text='Designates whether this user is verified or not.', verbose_name='Email Verification Status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active.Unselect this field instead of deleting accounts.', verbose_name='Active Status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='Staff Status')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='Superuser Status')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='Last Login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='Date Joined')),
                ('permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='permission_set', related_query_name='user', to='auth.Permission', verbose_name='Permissions')),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'ordering': ('-date_joined',),
            },
            managers=[
                ('objects', base.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=31, unique=True, verbose_name='Name')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Date Updated')),
                ('permissions', models.ManyToManyField(blank=True, to='auth.Permission', verbose_name='Permissions')),
            ],
            managers=[
                ('objects', base.models.UserTypeManager()),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(editable=False, max_length=256, verbose_name='Token')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Date Created')),
                ('user', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_type',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user_type', to='base.usertype'),
        ),
    ]
