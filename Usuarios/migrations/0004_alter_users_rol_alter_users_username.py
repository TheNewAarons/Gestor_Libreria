# Generated by Django 5.1.3 on 2024-12-01 03:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Usuarios', '0003_alter_users_options_alter_users_managers_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='rol',
            field=models.CharField(choices=[('Autor', 'Autor'), ('Bodeguero', 'Bodeguero'), ('Jefe de Bodega', 'Jefe de bodega')], default='Bodeguero', max_length=50),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
