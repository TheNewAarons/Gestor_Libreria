# Generated by Django 5.1.4 on 2024-12-17 19:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Bodegas', '0001_initial'),
        ('Libros', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimientoproducto',
            name='producto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Libros.libro'),
        ),
    ]
