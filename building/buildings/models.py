import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class Building(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, blank=True)
    year = models.IntegerField(verbose_name=_("Year"))
    city = models.CharField(verbose_name=_("City"), max_length=100)
    street = models.CharField(verbose_name=_("Street"), max_length=100)
    number = models.IntegerField(verbose_name=_("Number"))

    class Meta:
        verbose_name = _("Building")
        verbose_name_plural = _("Buildings")

    def __str__(self):
        return self.name or f"г.{self.city} ул.{self.street} д.{self.number}"


class Apartment(models.Model):
    class RoomsChoices(models.TextChoices):
        ONE = ("1", "1")
        TWO = ("2", "2")
        THREE = ("3", "3")
        FOUR_PLUS = ("4+", "4+")
        STUDIO = ("STUDIO", _("Studio"))

    area = models.DecimalField(
        verbose_name=_("Area"),
        max_digits=5,
        decimal_places=2,
    )
    rooms = models.CharField(
        verbose_name=_("Rooms"),
        choices=RoomsChoices.choices,
        default=RoomsChoices.ONE,
        max_length=20,
    )
    price = models.DecimalField(
        verbose_name=_("Price"),
        max_digits=19,
        decimal_places=2,
    )
    floor = models.PositiveIntegerField(verbose_name=_("Floor"))
    building = models.ForeignKey(
        Building,
        related_name="apartments",
        verbose_name=_("Building"),
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")

    def __str__(self):
        return f"{self.building} apartment"


def make_apartment_image_save_path(instance: "ApartmentImage", filename: str) -> str:
    building = instance.apartment.building
    address_string = f"{building.city} {building.street} {building.number}".strip()
    return "images/apartments/%s/%s" % (address_string, filename)


class ApartmentImage(models.Model):
    apartment = models.ForeignKey(
        Apartment,
        related_name="images",
        verbose_name=_("Apartment"),
        on_delete=models.CASCADE,
    )
    image = models.ImageField(
        upload_to=make_apartment_image_save_path,
        verbose_name=_("Image"),
    )

    def save(
        self,
        force_insert=False,
        force_update=False,
        using=None,
        update_fields=None,
    ):
        try:
            old_version = ApartmentImage.objects.get(pk=self.pk)
            path = old_version.image.path

            if os.path.exists(path) and self.image != old_version.image:
                os.remove(path)
        except ApartmentImage.DoesNotExist:
            pass

        super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using,
            update_fields=update_fields,
        )

    class Meta:
        verbose_name = _("Apartment's image")
        verbose_name_plural = _("Apartment's images")

    def __str__(self):
        return f"{self.apartment} image"


@receiver(pre_delete, sender=ApartmentImage)
def delete_apartment_image(
    sender: ApartmentImage,
    instance: ApartmentImage,
    **kwargs,
) -> None:
    instance.image.delete(False)
