# Generated by Django 5.1.5 on 2025-03-20 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodboards', '0010_alter_user_speciality'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='/media/profile_images/default.jpg', upload_to='profile_images/'),
        ),
    ]
