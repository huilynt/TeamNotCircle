# Generated by Django 2.2.7 on 2019-12-28 20:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('todo', '0005_todoitem_delete'),
    ]

    operations = [
        migrations.RenameField(
            model_name='todoitem',
            old_name='delete',
            new_name='deleted',
        ),
    ]
