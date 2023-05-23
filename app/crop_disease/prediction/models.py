from django.db import models

class Prediction(models.Model):
    image = models.ImageField(upload_to='images/')
    result = models.CharField(max_length=100)
