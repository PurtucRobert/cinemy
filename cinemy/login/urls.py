from django.urls import path
from login.viewsets import obtain_auth_token_base64
from login.views import signup, auth, pre_signup
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path("login/", auth, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("pre-signup/", pre_signup, name="pre_signup"),
    path("signup/<slug:uidb64>/", signup, name="signup"),
    path("generate-api-token/", obtain_auth_token_base64),
]
