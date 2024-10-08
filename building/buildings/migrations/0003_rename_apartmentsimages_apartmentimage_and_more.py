# Generated by Django 5.0.7 on 2024-07-31 08:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "buildings",
            "0002_rename_building_buildings_alter_apartments_options_and_more",
        ),
    ]

    operations = [
        migrations.RenameModel(
            old_name="ApartmentsImages",
            new_name="ApartmentImage",
        ),
        migrations.RenameModel(
            old_name="Buildings",
            new_name="Building",
        ),
        migrations.CreateModel(
            name="Apartment",
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
                            ("1", "1"),
                            ("2", "2"),
                            ("3", "3"),
                            ("4+", "4+"),
                            ("STUDIO", "Studio"),
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
                (
                    "building",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="apartments",
                        to="buildings.building",
                        verbose_name="Building",
                    ),
                ),
            ],
            options={
                "verbose_name": "Apartment",
                "verbose_name_plural": "Apartments",
            },
        ),
        migrations.AlterField(
            model_name="apartmentimage",
            name="apartment",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="images",
                to="buildings.apartment",
                verbose_name="Apartment",
            ),
        ),
        migrations.DeleteModel(
            name="Apartments",
        ),
    ]
