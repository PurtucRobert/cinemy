from django.urls import path, include, re_path
from login.views import activate, signup, auth

urlpatterns = [
    path("login", auth, name="login"),
    path("signup", signup, name="signup"),
    path(
        "activate/<slug:uidb64>/<slug:token>/",
        activate,
        name="activate",
    ),
]
