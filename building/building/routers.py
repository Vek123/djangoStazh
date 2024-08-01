from rest_framework import routers

from buildings.views import *


router = routers.DefaultRouter()
router.register(r"buildings", BuildingModelViewSet)
router.register(r"apartments", ApartmentModelViewSet)
