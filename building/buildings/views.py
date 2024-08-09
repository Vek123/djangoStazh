from rest_framework import viewsets, status, views
from rest_framework.exceptions import APIException
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
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


FEEDBACK_ACCEPTED_MAIL_SUBJECT = _("Ваша заявка принята")
FEEDBACK_ACCEPTED_MAIL_MESSAGE = _(
    "Уважаемый (ая) %(user_name)s. "
    "Ваша заявка была принята в работу. "
    "Мы отправим Вам письмо на этот адрес эл. почты "
    "когда оператор её обработает.\n\n"
    "С уважением, команда %(site_name)s"
)


class FeedbackFormView(views.APIView):
    serializer_class = serializers.FeedbackFormSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.POST)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            send_mail(
                FEEDBACK_ACCEPTED_MAIL_SUBJECT,
                FEEDBACK_ACCEPTED_MAIL_MESSAGE
                % {"user_name": data['name'], "site_name": settings.SITE_NAME},
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[data['email']],
                auth_user=settings.EMAIL_CONFIG["EMAIL_HOST_USER"],
                auth_password=settings.EMAIL_CONFIG["EMAIL_HOST_PASSWORD"],
                fail_silently=True,
            )
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            raise APIException(
                detail=str(e),
                code=status.HTTP_501_NOT_IMPLEMENTED,
            ) from e
