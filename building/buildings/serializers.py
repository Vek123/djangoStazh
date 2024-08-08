import smtplib

from rest_framework import serializers
from django.core.mail import EmailMessage
from django.conf import settings

from buildings import models


class ApartmentImageSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        image_value = representation.pop("image")
        return image_value

    class Meta:
        model = models.ApartmentImage
        fields = ["image"]


class ApartmentSerializer(serializers.ModelSerializer):
    gallery = ApartmentImageSerializer(source="images", many=True, read_only=True)
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        building = obj.building
        return f"г. {building.city}, ул. {building.street}, д. {building.number}"

    class Meta:
        model = models.Apartment
        fields = ["area", "rooms", "price", "gallery", "floor", "address"]


class BuildingApartmentsSerializer(ApartmentSerializer):
    class Meta:
        model = models.Apartment
        fields = ["area", "rooms", "price", "gallery", "floor"]


class BuildingSerializer(serializers.ModelSerializer):
    address = serializers.SerializerMethodField()

    def get_address(self, obj):
        return {
            "city": obj.city,
            "street": obj.street,
            "number": obj.number,
        }

    class Meta:
        model = models.Building
        fields = ["address", "name", "year"]


class FeedbackFormSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    comment = serializers.CharField()

    def send_email(self):
        if not self.is_valid():
            return {"status": "is not valid"}
        data = self.data
        headers = {'From': f'{settings.SITE_NAME} <{settings.EMAIL_HOST_USER}>'}
        try:
            email = EmailMessage(
                "Ваша заявка принята",
                f"Уважаемый (ая) {data['name']}. Ваша заявка была принята в работу. Мы отправим Вам письмо на этот адрес эл. почты когда оператор её обработает.\n\nС уважением, команда {settings.SITE_NAME}",
                settings.EMAIL_HOST_USER,
                [data['email']],
                headers=headers,
            )
            email.send()
            return {"status": "success"}
        except smtplib.SMTPException as e:
            print(f"Ошибка при отправке письма: {e}")
            return {"status": "error", "message": str(e)}
