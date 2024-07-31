import django_filters
from .models import Building, Apartment


class BuildingFilter(django_filters.FilterSet):
    class Meta:
        model = Building
        fields = {
            "city": ["exact"],
            "name": ["icontains"],
            "year": ["exact", "lt", "lte", "gt", "gte"],
        }


class ApartmentFilter(django_filters.FilterSet):
    rooms = django_filters.ChoiceFilter(choices=Apartment.RoomsChoices)

    class Meta:
        model = Apartment
        fields = {
            "area": ["exact", "lt", "lte", "gt", "gte"],
            "price": ["exact", "lt", "lte", "gt", "gte"],
            "floor": ["exact"],
        }
