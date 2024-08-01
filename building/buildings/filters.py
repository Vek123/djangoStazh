import django_filters

from buildings import models


class BuildingFilter(django_filters.FilterSet):
    class Meta:
        model = models.Building
        fields = {
            "city": ["exact"],
            "name": ["icontains"],
            "year": ["exact", "lt", "lte", "gt", "gte"],
        }


class ApartmentFilter(django_filters.FilterSet):
    rooms = django_filters.ChoiceFilter(choices=models.Apartment.RoomsChoices)

    class Meta:
        model = models.Apartment
        fields = {
            "area": ["exact", "lt", "lte", "gt", "gte"],
            "price": ["exact", "lt", "lte", "gt", "gte"],
            "floor": ["exact"],
        }
