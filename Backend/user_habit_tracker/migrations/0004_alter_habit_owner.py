# Generated by Django 5.1.7 on 2025-04-05 21:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("user_habit_tracker", "0003_rename_user_habit_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="habit",
            name="owner",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="habits",
                to="user_habit_tracker.habittrackeruser",
            ),
        ),
    ]
