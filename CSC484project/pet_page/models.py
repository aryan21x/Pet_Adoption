
from django.db import models

class Pet(models.Model):
    pet_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    breed = models.CharField(max_length=255)
    shelter_id = models.IntegerField()
    species = models.CharField(max_length=255)
    age = models.IntegerField(null=True, blank=True)
    adoptered = models.BooleanField(default=False)
    worker_id = models.IntegerField()
    vet_id = models.IntegerField(null=True, blank=True)
    adopt_id = models.IntegerField(null=True, blank=True)
