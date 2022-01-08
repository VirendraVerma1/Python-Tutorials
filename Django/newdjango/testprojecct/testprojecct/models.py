from django.db import models

# Create your models here.
class FaceData(models.Model):
    image_user_id=models.AutoField(primary_key=True)
    image_path=models.TextField()
    image_username=models.TextField()
    image_user_base_id=models.IntegerField()
    image_is_downloaded=models.IntegerField()
    created_on = models.DateTimeField(auto_now_add=True)