from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Show(models.Model):
  name= models.CharField(max_length=100)
  rating = models.CharField(max_length=100)
  description = models.TextField(max_length=250)
  cast = models.TextField(max_length=250)
  user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name

  def get_absolute_url(self):
    return reverse('detail', kwargs={'show_id': self.id})