# Generated by Django 3.1.7 on 2021-02-22 01:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('people', '0007_auto_20210222_0106'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssetsModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado_em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Atualizado_em')),
                ('active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('assets_type', models.CharField(choices=[('INT', 'INTANGIVEIS'), ('MOV', 'MOVEIS'), ('IMO', 'IMOVEIS')], max_length=3, verbose_name='Tipo de Ativo')),
                ('code', models.PositiveSmallIntegerField(verbose_name='Código')),
                ('description', models.TextField(verbose_name='Descrição')),
                ('acquisition_form', models.CharField(choices=[('COM', 'COMPRADO'), ('DOA', 'DOADO'), ('HER', 'HERDADO')], max_length=3, verbose_name='Forma de Aquisição')),
                ('acquisition_value', models.DecimalField(blank=True, decimal_places=2, max_digits=16, null=True, verbose_name='Valor de Aquisição')),
                ('localization', models.CharField(blank=True, max_length=100, null=True, verbose_name='Localização')),
                ('person_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='people.peoplemodel')),
            ],
            options={
                'verbose_name': 'Ativo',
                'verbose_name_plural': 'Ativos',
            },
        ),
    ]