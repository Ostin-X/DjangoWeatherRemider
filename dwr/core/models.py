from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

from datetime import timedelta
from django.utils import timezone

email_field = User._meta.get_field('email')
email_field._unique = True
email_field.null = False
email_field.blank = False


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=2, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('country_detail', kwargs={'slug': self.code})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Країна'
        verbose_name_plural = 'Країни'
        ordering = ['name']


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, blank=True, null=True)
    codename = models.CharField(max_length=100, unique=True, blank=True, null=True)
    weather_data = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def __str__(self):
        return f'{self.name}.{self.country.code}'

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.codename = f'{self.name.capitalize()}.{self.country.code}'
        self.slug = slugify(f'{self.name}{self.country.code}')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ['name']


class Subscription(models.Model):
    MY_CHOICES = (
        (3600, '1 Hour'),
        (7200, '2 Hours'),
        (10800, '3 Hours'),
        (21600, '6 Hours'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subs')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subs')
    is_active = models.BooleanField(default=True)
    time_period = models.PositiveIntegerField(choices=MY_CHOICES, default=0)
    next_run = models.DateTimeField(blank=True, null=True)
    webhook_url = models.URLField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def update_next_run(self):
        if self.time_period > 0:
            current_time = timezone.now()
            new_next_run = current_time + timedelta(seconds=self.time_period)
            self.next_run = new_next_run
            self.save()

    def __str__(self):
        return f'{self.user} - {self.city}'

    def save(self, *args, **kwargs):
        self.slug = slugify(f'{self.user.username}--{self.city.codename}')
        super().save(*args, **kwargs)

    # def get_absolute_url(self):
    #     return reverse('city_detail', kwargs={'pk': self.user.pk})

    class Meta:
        unique_together = ('user', 'city')
        verbose_name = 'Підписка'
        verbose_name_plural = 'Підписки'
        ordering = ['user', 'city']
