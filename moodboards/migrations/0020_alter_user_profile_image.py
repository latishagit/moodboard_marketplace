# Generated by Django 5.1.6 on 2025-05-11 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodboards', '0019_message_notification_sent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_image',
            field=models.ImageField(blank=True, default='media/profile_images/default.jpeg', upload_to='profile_images/'),
        ),
    ]
