# Generated by Django 5.1.6 on 2025-03-19 18:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moodboards', '0005_moodboard_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='category_images/'),
        ),
    ]
