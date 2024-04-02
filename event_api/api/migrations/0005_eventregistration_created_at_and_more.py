# Generated by Django 5.0.3 on 2024-04-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0004_eventregistration"),
    ]

    operations = [
        migrations.AddField(
            model_name="eventregistration",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name="eventregistration",
            name="updated_at",
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]