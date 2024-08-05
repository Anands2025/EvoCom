# Generated by Django 5.0.7 on 2024-07-30 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Role',
        ),
        migrations.AlterField(
            model_name='userdetails',
            name='role',
            field=models.CharField(blank=True, choices=[('member', 'Member'), ('organizer', 'Event Organizer'), ('community_admin', 'Community Admin')], max_length=30, null=True),
        ),
    ]