from django.contrib.auth.models import User
from django.db import models

from .constants import STATUS


# ----------------------------------------------------------------------------------------------------------------------
# User roles

class RegularUser(models.Model):
    profile = models.OneToOneField(to=User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE)


class Moderator(models.Model):
    profile = models.OneToOneField(to=User, on_delete=models.PROTECT)
    status = models.CharField(max_length=20, choices=STATUS.choices, default=STATUS.ACTIVE)


# ----------------------------------------------------------------------------------------------------------------------
# Image models

class Image(models.Model):
    image = models.ImageField(upload_to='images')
    title = models.CharField(max_length=255)
    hash_tags = models.ManyToManyField(to='HashTag', related_name='images')


class HashTag(models.Model):
    name = models.CharField(max_length=255)
    categories = models.ManyToManyField(to='Category', related_name='hash_tags')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
