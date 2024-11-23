# Generated by Django 5.1.3 on 2024-11-18 23:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Editoriales', '0001_initial'),
        ('Libros', '0013_delete_author_delete_users'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libro',
            name='editorial',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Editoriales.editorial', verbose_name='Editorial'),
        ),
    ]