from django.urls import path
from login.views import activate, signup, auth
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", auth, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("signup/", signup, name="signup"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        activate,
        name="activate",
    ),
]
