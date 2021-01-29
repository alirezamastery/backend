from django.db import models

class Changer(models.Model):
    name = models.CharField(max_length=200)
