# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-27 05:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import gestion_de_produits.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChemicalSubstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cas', models.CharField(max_length=200, unique=True, verbose_name='CAS number')),
                ('chemical_formulas', models.CharField(max_length=2000, verbose_name='Chemical formula')),
                ('mention', models.IntegerField(choices=[(0, 'Warning'), (1, 'Danger')], default=0, verbose_name='mention')),
            ],
            options={
                'verbose_name_plural': 'chemical substances',
                'verbose_name': 'chemical substance',
            },
        ),
        migrations.CreateModel(
            name='ChemicalSubstanceName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name or synonym')),
                ('product_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='names', to='gestion_de_produits.ChemicalSubstance')),
            ],
        ),
        migrations.CreateModel(
            name='FDS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, verbose_name='name')),
                ('reference', models.CharField(blank=True, max_length=60, verbose_name='ref number')),
                ('date', models.DateField(blank=True, null=True, verbose_name='update date')),
                ('file', models.FileField(blank=True, null=True, upload_to='fds-pdf/')),
            ],
            options={
                'verbose_name_plural': 'FDS',
                'verbose_name': 'FDS',
            },
        ),
        migrations.CreateModel(
            name='Hazard',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('fr_description', models.TextField(blank=True)),
                ('en_description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Hazard',
                'verbose_name': 'Hazard',
            },
            bases=(models.Model, gestion_de_produits.models.TranslatedFieldMixin),
        ),
        migrations.CreateModel(
            name='ManipulationProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('description', models.CharField(blank=True, max_length=20000)),
                ('protocol', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'manipulation protocols',
                'verbose_name': 'manipulation protocol',
            },
        ),
        migrations.CreateModel(
            name='Manufacturer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='name')),
                ('web_site', models.URLField(blank=True, verbose_name='web site')),
                ('phone', models.CharField(blank=True, max_length=60, verbose_name='phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail')),
            ],
            options={
                'verbose_name_plural': 'manufacturers',
                'verbose_name': 'manufacturer',
            },
        ),
        migrations.CreateModel(
            name='PackagingProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='name')),
                ('manufacturer_reference', models.CharField(blank=True, max_length=200, verbose_name="manufacturer's reference")),
                ('form', models.IntegerField(choices=[(0, 'liquid'), (1, 'tablet'), (2, 'capsule'), (3, 'powder')], default=0, verbose_name='forms')),
                ('packaging', models.CharField(blank=True, max_length=200, verbose_name='Packaging')),
                ('fds_exact', models.BooleanField(default=False, verbose_name='is exact FDS')),
                ('temperature_min', models.IntegerField(verbose_name='minimum temperature (Celsius degree)')),
                ('temperature_max', models.IntegerField(verbose_name='maximum temperature (Celsius degree)')),
                ('ventilated_cupboard', models.BooleanField(verbose_name='ventilated cupboard')),
                ('air', models.BooleanField(verbose_name='air sensitive')),
                ('moisture', models.BooleanField(verbose_name='moisture sensitive')),
                ('light', models.BooleanField(verbose_name='light sensitive')),
                ('gloves', models.CharField(blank=True, max_length=200, verbose_name='protective gloves')),
                ('protection', models.CharField(blank=True, max_length=200, verbose_name='protection')),
                ('target_organ', models.CharField(blank=True, max_length=200, verbose_name='target organ')),
                ('polluant', models.BooleanField(default=False, verbose_name='polluant')),
                ('isolate_can', models.BooleanField(default=False, verbose_name='isolate can')),
                ('specific_transport', models.BooleanField(default=False, verbose_name='specific transport')),
                ('cas', models.ManyToManyField(blank=True, to='gestion_de_produits.ChemicalSubstance')),
                ('fds', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.FDS')),
                ('hazard', models.ManyToManyField(blank=True, to='gestion_de_produits.Hazard')),
            ],
            options={
                'verbose_name_plural': 'brands and packaging',
                'verbose_name': 'brand and packaging',
            },
        ),
        migrations.CreateModel(
            name='Pictogram',
            fields=[
                ('name', models.CharField(max_length=5, primary_key=True, serialize=False)),
                ('picture', models.ImageField(blank=True, null=True, upload_to='pictogram/')),
                ('fr_description', models.TextField(blank=True)),
                ('en_description', models.TextField(blank=True)),
                ('fr_note', models.TextField(blank=True)),
                ('en_note', models.TextField(blank=True)),
            ],
            bases=(models.Model, gestion_de_produits.models.TranslatedFieldMixin),
        ),
        migrations.CreateModel(
            name='Preventive',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
                ('fr_description', models.TextField(blank=True)),
                ('en_description', models.TextField(blank=True)),
            ],
            options={
                'verbose_name_plural': 'Preventive',
                'verbose_name': 'Preventive',
            },
            bases=(models.Model, gestion_de_produits.models.TranslatedFieldMixin),
        ),
        migrations.CreateModel(
            name='ProductClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
            ],
            options={
                'verbose_name_plural': 'product groups',
                'verbose_name': 'product group',
            },
        ),
        migrations.CreateModel(
            name='Storage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storage_name', models.CharField(max_length=200, verbose_name='stockage')),
                ('laboratory_name', models.CharField(max_length=200, verbose_name='laboratory name')),
                ('floor', models.CharField(max_length=20, verbose_name='floor')),
                ('room', models.CharField(max_length=40, verbose_name='room')),
                ('storage_description', models.TextField(blank=True, verbose_name='description')),
                ('temperature_min', models.IntegerField(verbose_name='minimum temperature (Celsius degree)')),
                ('temperature_max', models.IntegerField(verbose_name='maximum temperature (Celsius degree)')),
                ('ventilated_cupboard', models.BooleanField(verbose_name='ventilated cupboard')),
                ('air', models.BooleanField(verbose_name='protect from air')),
                ('moisture', models.BooleanField(verbose_name='protect from moisture')),
                ('light', models.BooleanField(verbose_name='protect from light')),
            ],
            options={
                'verbose_name_plural': 'stockages',
                'verbose_name': 'stockage',
            },
        ),
        migrations.CreateModel(
            name='StoredChemicalProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=200, null=True, unique=True, verbose_name="numéro d'inventaire")),
                ('date_of_purchase', models.DateField(blank=True, null=True, verbose_name='date of purchase')),
                ('expiration_date', models.DateField(blank=True, null=True, verbose_name='expiration date')),
                ('done_date', models.DateField(blank=True, null=True, verbose_name='done date')),
                ('destroy_date', models.DateField(blank=True, null=True, verbose_name='destroy date')),
                ('packaging_product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.PackagingProduct')),
                ('storage_area', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.Storage')),
            ],
            options={
                'verbose_name_plural': 'products purchased',
                'verbose_name': 'product purchased',
            },
        ),
        migrations.AlterUniqueTogether(
            name='storage',
            unique_together=set([('storage_name', 'laboratory_name', 'floor')]),
        ),
        migrations.AddField(
            model_name='packagingproduct',
            name='incompatible_product',
            field=models.ManyToManyField(blank=True, to='gestion_de_produits.ProductClass'),
        ),
        migrations.AddField(
            model_name='packagingproduct',
            name='manipulation_protocol',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.ManipulationProtocol'),
        ),
        migrations.AddField(
            model_name='packagingproduct',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.Manufacturer'),
        ),
        migrations.AddField(
            model_name='packagingproduct',
            name='preventive',
            field=models.ManyToManyField(blank=True, to='gestion_de_produits.Preventive'),
        ),
        migrations.AddField(
            model_name='fds',
            name='manufacturer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gestion_de_produits.Manufacturer'),
        ),
        migrations.AddField(
            model_name='chemicalsubstance',
            name='classification',
            field=models.ManyToManyField(blank=True, to='gestion_de_produits.ProductClass'),
        ),
        migrations.AddField(
            model_name='chemicalsubstance',
            name='pictogram',
            field=models.ManyToManyField(blank=True, to='gestion_de_produits.Pictogram'),
        ),
    ]
