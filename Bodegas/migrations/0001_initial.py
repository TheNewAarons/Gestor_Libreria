# Generated by Django 5.1.3 on 2024-11-13 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bodega',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.TextField(max_length=200)),
                ('direction', models.TextField(max_length=100)),
                ('tipo_de_contenido', models.CharField(max_length=100)),
                ('capacidad', models.PositiveIntegerField()),
                ('estado', models.PositiveIntegerField()),
                ('nivel_stock', models.PositiveIntegerField()),
                ('tamaño_bodega', models.PositiveIntegerField()),
                ('bodega_origen', models.CharField(blank=True, max_length=100, null=True)),
                ('bodega_destino', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]