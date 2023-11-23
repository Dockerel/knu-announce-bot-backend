# Generated by Django 4.2.7 on 2023-11-23 13:22

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Info",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "info_type",
                    models.CharField(
                        choices=[
                            ("general", "General"),
                            ("bachelor", "Bachelor"),
                            ("scholarship", "Scholarship"),
                            ("simcom", "Simcom"),
                            ("glsob", "Glsob"),
                            ("incom", "Incom"),
                            ("graduate", "Graduate"),
                            ("contract", "Contract"),
                        ],
                        max_length=100,
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("href", models.CharField(max_length=100)),
                ("date", models.CharField(max_length=12)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
