from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.views import View
from django.http import JsonResponse

from buildings import serializers, filters, models


class ApartmentModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ApartmentSerializer
    queryset = models.Apartment.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.ApartmentFilter


class BuildingModelViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BuildingSerializer
    queryset = models.Building.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.BuildingFilter

    @action(methods=["get"], detail=True)
    def apartments(self, request, pk):
        building = models.Building.objects.get(pk=pk)
        apartments = building.apartments.all()
        filtered_apartments = filters.ApartmentFilter(
            request.query_params, queryset=apartments
        )
        apartmentsSerializer = serializers.BuildingApartmentsSerializer(
            filtered_apartments.qs,
            many=True,
            context={
                "request": request,
                "format": self.format_kwarg,
                "view": self,
            }
        )
        return Response(apartmentsSerializer.data)


class FeedbackFormView(View):

    def post(self, request, *args, **kwargs):
        form = serializers.FeedbackFormSerializer(data=request.POST)
        response = form.send_email()

        return JsonResponse(response)
