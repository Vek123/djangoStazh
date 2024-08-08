import smtplib

from rest_framework import viewsets, status, views
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.http import JsonResponse
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

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
            },
        )
        return Response(apartmentsSerializer.data)


def send_email(data):
    try:
        send_mail(
            _("Ваша заявка принята"),
            _("Уважаемый (ая) %s. Ваша заявка была принята в работу. Мы отправим Вам письмо на этот адрес эл. почты когда оператор её обработает.\n\nС уважением, команда %s")
            % (data['name'], settings.SITE_NAME),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[data['email']],
            fail_silently=True,
        )
        return Response(status=status.HTTP_204_NO_CONTENT)
    except smtplib.SMTPException as e:
        return Response(
            data={"status": "error", "message": str(e)},
            status=status.HTTP_501_NOT_IMPLEMENTED,
            content_type="application/json",
        )


class FeedbackFormView(views.APIView):
    serializer_class = serializers.FeedbackFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        response = send_email(request.POST)

        return response if isinstance(response, Response) else JsonResponse(response)
