# Generated by Django 5.1.2 on 2024-11-23 01:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Libros', '0018_libro_camtidad_alter_libro_portada_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='libro',
            old_name='camtidad',
            new_name='cantidad',
        ),
    ]
