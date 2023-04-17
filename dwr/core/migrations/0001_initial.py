# Generated by Django 4.2 on 2023-04-16 13:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('code', models.CharField(max_length=2, unique=True)),
            ],
            options={
                'verbose_name': 'Країна',
                'verbose_name_plural': 'Країни',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('codename', models.CharField(blank=True, max_length=100, null=True, unique=True)),
                ('weather_data', models.TextField(blank=True, null=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('country', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.country')),
            ],
            options={
                'verbose_name': 'Місто',
                'verbose_name_plural': 'Міста',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('time_period', models.IntegerField(choices=[(4, 'Four'), (8, 'Eight'), (12, 'Twelve')], default=0)),
                ('weather_data', models.TextField(blank=True, null=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to='core.city')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subs', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Підписка',
                'verbose_name_plural': 'Підписки',
                'ordering': ['user'],
                'unique_together': {('user', 'city')},
            },
        ),
    ]
