# Generated by Django 5.0.7 on 2024-07-29 14:08

import buildings.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Apartments",
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
                (
                    "area",
                    models.DecimalField(
                        decimal_places=2, max_digits=5, verbose_name="Area"
                    ),
                ),
                (
                    "rooms",
                    models.CharField(
                        choices=[
                            ("1", "One"),
                            ("2", "Two"),
                            ("3", "Three"),
                            ("4+", "Four Plus"),
                            ("Студия", "Studio"),
                        ],
                        default="1",
                        max_length=20,
                        verbose_name="Rooms",
                    ),
                ),
                (
                    "price",
                    models.DecimalField(
                        decimal_places=2, max_digits=19, verbose_name="Price"
                    ),
                ),
                ("floor", models.PositiveIntegerField(verbose_name="Floor")),
            ],
        ),
        migrations.CreateModel(
            name="Building",
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
                (
                    "name",
                    models.CharField(
                        blank=True, max_length=100, verbose_name="Name"
                    ),
                ),
                ("year", models.IntegerField(verbose_name="Year")),
                ("city", models.CharField(max_length=100, verbose_name="City")),
                (
                    "street",
                    models.CharField(max_length=100, verbose_name="Street"),
                ),
                ("number", models.IntegerField(verbose_name="Number")),
            ],
        ),
        migrations.CreateModel(
            name="ApartmentsImages",
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
                (
                    "image",
                    models.ImageField(
                        upload_to=buildings.models.make_apartment_image_save_path,
                        verbose_name="Image",
                    ),
                ),
                (
                    "apartment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="images",
                        to="buildings.apartments",
                        verbose_name="Apartment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="apartments",
            name="building",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="apartments",
                to="buildings.building",
                verbose_name="Building",
            ),
        ),
    ]
