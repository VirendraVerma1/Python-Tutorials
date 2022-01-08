from .models import Article
from rest_framework import serializers
from .models import Article
from .models import Face_data
from .models import File


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model=Article
        #fields=['id','title','author']
        fields='__all__'

class FaceSerialier(serializers.ModelSerializer):
    class Meta:
        model=Face_data
        fields=['image_path','image_username','image_user_base_id','image_is_downloaded']

class FileSerializer(serializers.ModelSerializer):
  class Meta():
    model = File
    fields = ('file', 'remark', 'timestamp')

# class ArticleSerializer(serializers.Serializer):
#     title=serializers.CharField(max_length=100)
#     author=serializers.CharField(max_length=100)
#     email=serializers.EmailField(max_length=100)
#     date=serializers.DateTimeField()

#     def create(self,validated_data):
#         return Article.objects.create(validated_data)

#     def update(self, instance, validated_data):
#         instance.title=validated_data.get('title',instance.title)
#         instance.author=validated_data.get('author',instance.author)
#         instance.email=validated_data.get('author',instance.email)
#         instance.date=validated_data.get('author',instance.date)
#         instance.save()
#         return instance
