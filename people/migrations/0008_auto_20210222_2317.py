# Generated by Django 3.1.7 on 2021-02-22 23:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0007_auto_20210222_0106'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='peoplemodel',
            options={'ordering': ['name'], 'verbose_name': 'Pessoa', 'verbose_name_plural': 'Pessoas'},
        ),
    ]
