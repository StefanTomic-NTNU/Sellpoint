# Generated by Django 3.1.6 on 2021-03-25 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertisements', '0009_auto_20210311_1001'),
        ('profiles', '0005_auto_20210223_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='savedAd',
            field=models.ManyToManyField(blank=True, to='advertisements.Advertisement'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_images'),
        ),
    ]