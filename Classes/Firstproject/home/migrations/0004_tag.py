# Generated by Django 4.0.2 on 2022-03-02 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_blog_image_alter_blog_date_alter_blog_desc_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=122, null=True)),
            ],
        ),
    ]
