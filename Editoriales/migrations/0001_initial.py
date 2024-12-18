# Generated by Django 5.1.4 on 2024-12-18 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Editorial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('address', models.CharField(max_length=100, unique=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True, unique=True)),
            ],
        ),
    ]