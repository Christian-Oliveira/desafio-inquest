# Generated by Django 3.1.7 on 2021-02-22 01:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='assetsmodel',
            old_name='person_id',
            new_name='person',
        ),
    ]
