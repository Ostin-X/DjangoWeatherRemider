from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

User._meta.get_field('email')._unique = True
User._meta.get_field('email').null = False
User._meta.get_field('email').blank = False


class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=2, unique=True)
    slug = models.SlugField(max_length=255, unique=True, blank=True, null=True)

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
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

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
        (4, 'Four'),
        (8, 'Eight'),
        (12, 'Twelve'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subs')
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='subs')
    is_active = models.BooleanField(default=True)
    time_period = models.IntegerField(choices=MY_CHOICES, default=0)
    # weather_data = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

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
