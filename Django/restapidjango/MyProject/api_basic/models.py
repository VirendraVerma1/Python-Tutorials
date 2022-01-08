from django.db import models
from django.db.models.base import ModelState

# Create your models here.

class Article(models.Model):
    title=models.CharField(max_length=100)
    author=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    images=models.TextField(default='null')
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Face_data(models.Model):
    image_user_id=models.AutoField(primary_key=True)
    image_path=models.FileField(blank=False, null=False)
    image_username=models.TextField()
    image_user_base_id=models.IntegerField()
    image_is_downloaded=models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)
