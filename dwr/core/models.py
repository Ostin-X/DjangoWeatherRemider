from django.db import models
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True
User._meta.get_field('email').null = False
User._meta.get_field('email').blank = False


class City(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    codename = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    # def get_absolute_url(self):
    #     return reverse('user_detail', kwargs={'pk': self.user.pk})

    class Meta:
        verbose_name = 'Місто'
        verbose_name_plural = 'Міста'
        ordering = ['name']
