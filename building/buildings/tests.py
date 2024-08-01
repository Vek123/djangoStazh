import os
import tempfile

from django.test import TestCase, Client, override_settings
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse

from buildings import models


class BuildingTestCase(TestCase):
    def setUp(self):
        self.building = models.Building.objects.create(
            name="Building",
            year=2012,
            city="City",
            street="Street",
            number=1,
        )
        self.apartment = models.Apartment.objects.create(
            area=10.12,
            rooms=1,
            price=1000000.12,
            floor=1,
            building=models.Building.objects.get(pk=1),
        )

    def test_get_model(self):
        url = reverse("building-list")
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

    def test_get_related_model(self):
        url = reverse("building-apartments", kwargs={"pk": "1"})
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


class ApartmentTestCase(TestCase):
    def setUp(self):
        self.building = models.Building.objects.create(
            name="Building",
            year=2012,
            city="City",
            street="Street",
            number=1,
        )
        self.apartment = models.Apartment.objects.create(
            area=10.12,
            rooms=1,
            price=1000000.12,
            floor=1,
            building=self.building,
        )

    def test_get_model(self):
        url = reverse("apartment-list")
        client = Client()
        response = client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)


@override_settings(MEDIA_ROOT=tempfile.gettempdir())
class ApartmentImageTestCase(TestCase):
    def setUp(self):
        self.building = models.Building.objects.create(
            name="Building",
            year=2012,
            city="City",
            street="Street",
            number=1,
        )
        self.apartment = models.Apartment.objects.create(
            area=10.12,
            rooms=1,
            price=1000000.12,
            floor=1,
            building=self.building,
        )
        self.image_path = "test.jpg"

    def test_save_new_image(self):
        image = models.ApartmentImage.objects.create(
            apartment=self.apartment,
            image=SimpleUploadedFile(self.image_path, b"content"),
        )
        self.assertTrue(os.path.exists(image.image.path))

    def test_replace_existing_image(self):
        image = models.ApartmentImage.objects.create(
            apartment=self.apartment,
            image=SimpleUploadedFile(self.image_path, b"content"),
        )
        image.image = SimpleUploadedFile(self.image_path, b"content")
        image.save()
        self.assertTrue(os.path.exists(image.image.path))
