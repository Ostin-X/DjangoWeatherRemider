# Generated by Django 4.2 on 2023-04-24 09:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_country_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name': 'Країна', 'verbose_name_plural': 'Країни'},
        ),
        migrations.AlterModelOptions(
            name='subscription',
            options={'ordering': ['user', 'city'], 'verbose_name': 'Підписка', 'verbose_name_plural': 'Підписки'},
        ),
    ]