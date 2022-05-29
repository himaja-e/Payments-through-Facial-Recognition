from django.db import models

# Create your models here.
class Student(models.Model):
    name=models.CharField(max_length=30)
    image=models.ImageField(upload_to='uploads/')