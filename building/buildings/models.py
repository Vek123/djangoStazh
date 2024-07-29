import os

from django.db import models
from django.utils.translation import gettext_lazy as _

from building import settings


# Create your models here.
class Buildings(models.Model):
    name = models.CharField(verbose_name=_("Name"), max_length=100, blank=True)
    year = models.IntegerField(verbose_name=_("Year"))
    city = models.CharField(verbose_name=_("City"), max_length=100)
    street = models.CharField(verbose_name=_("Street"), max_length=100)
    number = models.IntegerField(verbose_name=_("Number"))

    def __str__(self):
        return self.name or f"г.{self.city} ул.{self.street} д.{self.number}"

    class Meta:
        verbose_name = _("Building")
        verbose_name_plural = _("Buildings")


class Apartments(models.Model):
    class RoomsChoices(models.TextChoices):
        ONE = "1", "1",
        TWO = "2", "2",
        THREE = "3", "3",
        FOUR_PLUS = "4+", "4+",
        STUDIO = "Студия", "Студия",

    area = models.DecimalField(verbose_name=_("Area"), max_digits=5,
                               decimal_places=2)
    rooms = models.CharField(verbose_name=_("Rooms"),
                             choices=RoomsChoices.choices,
                             default=RoomsChoices.ONE, max_length=20)
    price = models.DecimalField(verbose_name=_("Price"), max_digits=19,
                                decimal_places=2)
    floor = models.PositiveIntegerField(verbose_name=_("Floor"))
    building = models.ForeignKey(Buildings, related_name="apartments",
                                 verbose_name=_("Building"),
                                 on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.building.__str__()} apartment"

    class Meta:
        verbose_name = _("Apartment")
        verbose_name_plural = _("Apartments")


class ApartmentsImages(models.Model):
    def upload_to(instance, filename):
        return 'images/catalog/%s/%s' % (
            f"{instance.apartment.building.city}"
            f"{instance.apartment.building.street}"
            f"{instance.apartment.building.number}",
            filename)

    apartment = models.ForeignKey(Apartments, related_name="images",
                                  verbose_name=_("Apartment"),
                                  on_delete=models.CASCADE)
    image = models.ImageField(upload_to=upload_to, verbose_name=_("Image"))

    def __str__(self):
        return f"{self.apartment.__str__()} image"

    def delete(self, using=None, keep_parents=False):
        path = (
            f"{settings.MEDIA_ROOT}\\{self.image.name}"
            .replace("/", "\\"))
        if os.path.exists(path):
            os.remove(path)
        super().delete(using=using, keep_parents=keep_parents)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        path = (
            f"{settings.MEDIA_ROOT}\\"
            f"{ApartmentsImages.objects.get(pk=self.pk).image.name}"
            .replace("/", "\\"))
        if os.path.exists(path):
            os.remove(path)
        super().save(force_insert=False, force_update=force_update, using=using,
                     update_fields=update_fields)

    class Meta:
        verbose_name = _("Apartment's image")
        verbose_name_plural = _("Apartment's images")
