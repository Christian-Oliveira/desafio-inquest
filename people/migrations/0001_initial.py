# Generated by Django 3.1.7 on 2021-02-20 23:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PeopleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado_em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado_em')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('people_type', models.CharField(choices=[('F', 'FISICA'), ('J', 'JURIDICA')], max_length=1, verbose_name='Tipo')),
                ('name', models.CharField(max_length=150, verbose_name='Nome')),
                ('cpf', models.CharField(blank=True, max_length=11, null=True, verbose_name='CPF')),
                ('cnpj', models.CharField(blank=True, max_length=14, null=True, verbose_name='CNPJ')),
                ('email', models.EmailField(max_length=150, verbose_name='E-mail')),
            ],
            options={
                'verbose_name': 'Pessoa',
                'verbose_name_plural': 'Pessoas',
            },
        ),
    ]
