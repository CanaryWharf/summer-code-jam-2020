# Generated by Django 3.0.8 on 2020-08-02 10:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_remove_threadmessage_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='threadmessage',
            old_name='user',
            new_name='user_id',
        ),
    ]