from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from buildings.serializers import *
from .filters import *


class ApartmentModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = ApartmentSerializer
    queryset = Apartment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = ApartmentFilter


class BuildingModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BuildingSerializer
    queryset = Building.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = BuildingFilter

    @action(methods=["get"], detail=True)
    def apartments(self, request, pk):
        building = Building.objects.get(pk=pk)
        apartments = building.apartments.all()
        filtered_apartments = ApartmentFilter(request.query_params, queryset=apartments)
        apartmentsSerializer = BuildingApartmentsSerializer
        return Response(
            apartmentsSerializer(
                filtered_apartments.qs, many=True, context={"request": request}
            ).data
        )
