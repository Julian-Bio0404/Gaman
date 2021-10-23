# Generated by Django 3.2.8 on 2021-10-23 21:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Club',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date time on which the was updated.', verbose_name='updated at')),
                ('slugname', models.SlugField(unique=40)),
                ('about', models.TextField(blank=True, help_text='write something about you')),
                ('official_web', models.URLField(blank=True, help_text='Web site')),
                ('photo', models.ImageField(blank=True, help_text='Club photo', null=True, upload_to='sports/clubs/photos%Y/%m/%d/')),
                ('cover_photo', models.ImageField(blank=True, help_text='Club cover photo', null=True, upload_to='sports/clubs/cover_photos/%Y/%m/%d/')),
                ('city', models.CharField(blank=True, help_text='State of the origin', max_length=60)),
            ],
            options={
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date time on which the was updated.', verbose_name='updated at')),
                ('slugname', models.SlugField(unique=40)),
                ('about', models.TextField(blank=True, help_text='write something about you')),
                ('official_web', models.URLField(blank=True, help_text='Web site')),
                ('photo', models.ImageField(blank=True, help_text='league photo', null=True, upload_to='sports/leagues/photos%Y/%m/%d/')),
                ('cover_photo', models.ImageField(blank=True, help_text='league cover photo', null=True, upload_to='sports/leagues/cover_photos/%Y/%m/%d/')),
                ('country', models.CharField(blank=True, help_text='Country of the league', max_length=60)),
                ('state', models.CharField(blank=True, help_text='State of the origin', max_length=60)),
                ('sport', models.CharField(blank=True, help_text='sport of the origin', max_length=60)),
            ],
            options={
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, help_text='Date time on which the was created.', verbose_name='created at')),
                ('updated', models.DateTimeField(auto_now=True, help_text='Date time on which the was updated.', verbose_name='updated at')),
                ('active', models.BooleanField(default=True)),
                ('club', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sports.club')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created', '-updated'],
                'get_latest_by': 'created',
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='club',
            name='members',
            field=models.ManyToManyField(related_name='members', through='sports.Member', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='club',
            name='trainer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
