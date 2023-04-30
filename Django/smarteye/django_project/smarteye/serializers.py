from rest_framework import serializers
from .models import FaceData

class FaceSerialier(serializers.ModelSerializer):
    class Meta:
        model=FaceData
        # fields=['image_path','image_username','image_user_base_id','image_is_downloaded']
        fields='__all__'