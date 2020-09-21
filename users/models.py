from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=16, blank=False)
    email = models.CharField(max_length=50, blank=True)
