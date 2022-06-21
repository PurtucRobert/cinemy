from django.urls import path
from newsletter.views import (
    newsletter_page,
    newsletter_registered_user,
    confirm_subscription,
)


urlpatterns = [
    path("", newsletter_page, name="newsletter_page"),
    path(
        "registered_user/<pk>/",
        newsletter_registered_user,
        name="newsletter_registered_user",
    ),
    path(
        "confirm_subscription/<slug:uidb64>/",
        confirm_subscription,
        name="confirm_subscription",
    ),
]
