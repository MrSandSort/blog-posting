# Generated by Django 5.1.3 on 2024-12-03 23:51

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_blogpost_likes_count'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='likes',
            unique_together={('user', 'post')},
        ),
    ]