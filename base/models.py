from django.db import models
from django.contrib.auth.models import AbstractUser

class Topic(models.Model):
    name = models.CharField(max_length=100,unique=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    name = models.CharField(max_length=50, null=True)
    email = models.CharField(max_length=50,unique=True, null=True)
    college= models.CharField(max_length=50, null=True)
    city= models.CharField(max_length=50, null=True)
    fields_of_interests=models.ManyToManyField(
        Topic, related_name='topics',blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    




class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=200,null=True, blank=True)
    participants = models.ManyToManyField(
        User, related_name='participants', blank=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Post(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='')
    caption = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)
    topic=models.ForeignKey(Topic, on_delete=models.SET_NULL,null=True)
    city=models.CharField(max_length=50)
    room_id=models.IntegerField(null=True);

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.caption[0:50]
