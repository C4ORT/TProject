from django.db import models
from .choices import GENDER_CHOICE

# Create your models here.

class Table(models.Model):

    name=models.CharField(max_length=15, default='')
    surname=models.CharField(max_length=30, default='')
    lastname=models.CharField(max_length=20, default='')

    status=models.CharField(max_length=40, default='')
    office=models.CharField(max_length=20, default='')
    work_phone=models.CharField(max_length=15, default='')
    cellphone=models.CharField(max_length=15, default='')
    position=models.CharField(max_length=100, default='')
    photo=models.ImageField(upload_to="images/", blank=True, null=True)


class Customer(models.Model):
    name = models.CharField(max_length=15, default='')
    surname=models.CharField(max_length=30, default='')
    lastname=models.CharField(max_length=20, default='')

    gender = models.CharField(choices=GENDER_CHOICE, max_length=1)

    status=models.CharField(max_length=40, default='')
    office=models.CharField(max_length=20, default='')
    work_phone=models.CharField(max_length=15, default='')
    cellphone=models.CharField(max_length=15, default='')
    position=models.CharField(max_length=100, default='')
    photo=models.ImageField(upload_to="images/", blank=True, null=True)

    blob_photo = models.BinaryField()

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} id:{self.id}"





