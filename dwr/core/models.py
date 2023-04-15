from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

User._meta.get_field('email')._unique = True
User._meta.get_field('email').null = False
User._meta.get_field('email').blank = False


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    codename = models.CharField(max_length=100, unique=True, blank=True, null=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('city_detail', kwargs={'slug': self.slug})

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
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    time_period = models.IntegerField(choices=MY_CHOICES, default=0)
    weather_data = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user} - {self.city}'

    # def get_absolute_url(self):
    #     return reverse('city_detail', kwargs={'pk': self.user.pk})

    class Meta:
        unique_together = ('user', 'city')
        verbose_name = 'Підписка'
        verbose_name_plural = 'Підписки'
        ordering = ['user']
