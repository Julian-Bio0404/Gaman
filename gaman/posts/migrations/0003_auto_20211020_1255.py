# Generated by Django 3.2.8 on 2021-10-20 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'get_latest_by': 'created', 'ordering': ['-created', '-updated']},
        ),
        migrations.AlterModelOptions(
            name='principalcomment',
            options={'ordering': ['-reactions', 'created']},
        ),
    ]
