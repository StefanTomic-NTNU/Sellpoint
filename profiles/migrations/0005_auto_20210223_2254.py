# Generated by Django 3.1.6 on 2021-02-23 21:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20210217_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='profile_images/default.jpg', upload_to='profile_images'),
        ),
    ]