# Generated by Django 4.0 on 2021-12-12 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api_basic', '0002_face_data_article_images'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='')),
                ('remark', models.CharField(max_length=20)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]