from django.db import models

# Create your models here.

class user(models.Model):

    username = models.CharField(max_length = 20)
    password = models.CharField(max_length = 20)
    pic = models.ImageField(upload_to='users', default='no_picture.jpg')


    def __str__(self):
        return "Username: " + self.username