from django.db import models
from django.db.models.base import ModelState
# Create your models here.

class SmartEyeData(models.Model):
    image_path=models.FileField(blank=False, null=False)
    image_encoded=models.TextField(blank=False, null=False)
    image_username=models.TextField()
    image_user_base_id=models.IntegerField()
    image_is_downloaded=models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)

class FaceData(models.Model):
    image_path=models.FileField(upload_to='images/',blank=False, null=False)
    image_encoded=models.TextField(blank=False, null=False)
    image_username=models.TextField()
    image_user_base_id=models.IntegerField()
    image_is_downloaded=models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)