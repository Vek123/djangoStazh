from rest_framework import serializers

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
