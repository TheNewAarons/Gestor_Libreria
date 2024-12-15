# Generated by Django 5.1.4 on 2024-12-12 04:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Libros', '0019_rename_camtidad_libro_cantidad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200, unique=True)),
                ('direction', models.CharField(max_length=100, unique=True)),
                ('tipo_de_contenido', models.CharField(max_length=100)),
                ('capacidad', models.PositiveIntegerField(blank=True, null=True)),
                ('estado', models.CharField(choices=[('VA', 'Vacio'), ('OC', 'Ocupado'), ('MT', 'Mantenimiento')], default='BA', max_length=2)),
                ('nivel_stock', models.IntegerField(default=0)),
                ('tamaño_bodega', models.PositiveIntegerField(blank=True, null=True)),
                ('bodega_origen', models.CharField(blank=True, max_length=100, null=True)),
                ('bodega_destino', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='ProductoBodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.IntegerField()),
                ('bodega', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bodegas.bodega')),
                ('producto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libros.libro')),
            ],
        ),
        migrations.AddField(
            model_name='bodega',
            name='productos',
            field=models.ManyToManyField(through='Bodegas.ProductoBodega', to='Libros.libro'),
        ),
    ]
