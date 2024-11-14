# Generated by Django 5.1.3 on 2024-11-13 23:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bodegas', '0002_alter_bodega_capacidad_alter_bodega_estado_and_more'),
        ('Libros', '0007_alter_libro_portada'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bodega',
            name='nivel_stock',
            field=models.IntegerField(default=0),
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
    ]