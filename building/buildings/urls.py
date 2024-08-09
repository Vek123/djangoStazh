from django.urls import path

from buildings.views import FeedbackFormView

urlpatterns = [
    path("feedback/", FeedbackFormView.as_view(), name="feedbackForm"),
]
