from django.db import models
from django.utils import timezone
import hashlib
import uuid

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
    hash = models.CharField(max_length=32, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.generate_hash()
        super().save(*args, **kwargs)
    
    def generate_hash(self):
        while True:
            unique_string = f"{uuid.uuid4()}-{self.name}-{timezone.now()}"
            hash_value = hashlib.md5(unique_string.encode()).hexdigest()[:16]
            if not Scripts.objects.filter(hash=hash_value).exists():
                return hash_value
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

class Templates(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=56)
    author = models.ForeignKey(TelegramUsers, on_delete=models.CASCADE)
    scripts = models.ManyToManyField(Scripts)
    hash = models.CharField(max_length=32, unique=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        if not self.hash:
            self.hash = self.generate_hash()
        super().save(*args, **kwargs)
    
    def generate_hash(self):
        while True:
            unique_string = f"{uuid.uuid4()}-{self.name}-{timezone.now()}"
            hash_value = hashlib.md5(unique_string.encode()).hexdigest()[:16]
            if not Templates.objects.filter(hash=hash_value).exists():
                return hash_value
    
    def __str__(self):
        return self.name
    class Meta:
        ordering = ['-created']

class MainPage(models.Model):
    title = models.CharField(max_length=56)
    text = models.TextField(default=None)
    iframe = models.TextField(default=None)
    def __str__(self):
        return self.title