# Generated by Django 3.2.16 on 2023-04-27 22:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_eventvisitor_user'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='event',
            options={'permissions': [('can_create_event', 'Can create event')]},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('can_create_post', 'Can create post')]},
        ),
    ]
