#from django.contrib.auth.models import User
from users.models import CustomUser
from django.utils import timezone
from django.urls import reverse 
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.



class Post(models.Model):
	title = models.CharField(max_length=100)	
	image = models.ImageField(blank=True, null=True)
	content = models.TextField()
	location = models.CharField(max_length=100, blank=True, null=True)	
	date_posted = models.DateTimeField(default=timezone.now)
	author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)



	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post-detail', kwargs={'pk': self.pk})


class Measurement(models.Model):
 	location = models.CharField(max_length=200)
 	destination = models.CharField(max_length=200)
 	distance = models.DecimalField(max_digits=10, decimal_places=2)
 	created = models.DateTimeField(auto_now_add=True)


 	def __str__(self):
 		return f"Distance from {self.location} to {self.destination} is {self.distance} miles."