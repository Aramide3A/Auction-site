# Generated by Django 4.1.1 on 2023-11-27 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_listing_completed_alter_watchlist_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_bid', to=settings.AUTH_USER_MODEL),
        ),
    ]
