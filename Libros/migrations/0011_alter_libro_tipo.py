# Generated by Django 5.1.3 on 2024-11-15 03:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Libros', '0010_merge_20241113_2218'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='tipo',
            field=models.CharField(choices=[('Libro', 'Libro'), ('Revista', 'Revista'), ('Diccionario', 'Diccionario')], max_length=100, null=True),
        ),
    ]
