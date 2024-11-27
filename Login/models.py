from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Account(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    profile_picture = models.FileField(upload_to='profile_pictures/', null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    about = models.TextField(blank=True)
    admin = models.BooleanField(default=False)
    verified_email = models.BooleanField(default=False)

    def __str__(self):
        return self.full_name or self.user.username


class Conversation(models.Model):
    participants = models.ManyToManyField(Account)

    def __str__(self):
        return ", ".join([str(participant) for participant in self.participants.all()])


class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE ,null=True)
    sender = models.ForeignKey(Account, on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.sender}: {self.text}"


class Token(models.Model):
    user_id = models.IntegerField()
    code = models.IntegerField(null=True)
    created_at = models.DateTimeField(default=timezone.now)
    email = models.CharField(max_length=40, null=True)

    def __str__(self):
        return str(self.code)
