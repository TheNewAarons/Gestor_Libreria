# Generated by Django 5.1.3 on 2024-11-12 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Libros', '0003_libro_tipo_alter_libro_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='libro',
            name='editorial',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='libro',
            name='tamano',
            field=models.CharField(max_length=200, null=True),
        ),
    ]