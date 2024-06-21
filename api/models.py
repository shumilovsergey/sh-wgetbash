from django.db import models
from django.utils import timezone

class TelegramUsers(models.Model):
    session_id = models.CharField(max_length=56, unique=True)
    tg_id = models.CharField(max_length=56, default="no-auth")
    name = models.CharField(max_length=56, default="no-auth")
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.tg_id
    class Meta:
        ordering = ['-created']

class Scripts(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56)
    author = models.CharField(max_length=56, default="no-auth")
    followers = models.ManyToManyField(TelegramUsers)
    text = models.TextField(default=None)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

class Templates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56)
    author = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE)
    scripts = models.ManyToManyField(Scripts)
    created = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

class MainPage(models.Model):
    title = models.CharField(max_length=56)
    text = models.TextField(default=None)
    youtube_id = models.CharField(max_length=56, default="jfKfPfyJRdk")
    def __str__(self):
        return self.title