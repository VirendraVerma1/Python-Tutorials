# Generated by Django 4.0 on 2021-12-09 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FaceData',
            fields=[
                ('image_user_id', models.AutoField(primary_key=True, serialize=False)),
                ('image_path', models.TextField()),
                ('image_username', models.TextField()),
                ('image_user_base_id', models.IntegerField()),
                ('image_is_downloaded', models.IntegerField()),
                ('created_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
