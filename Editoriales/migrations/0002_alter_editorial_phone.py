# Generated by Django 5.1.3 on 2024-11-19 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Editoriales', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='editorial',
            name='phone',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
