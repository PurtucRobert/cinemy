from base64 import urlsafe_b64decode
from django.conf import settings
from django.shortcuts import redirect, render
from login.forms import SignupForm
from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib import messages
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_str
from ratelimit.decorators import ratelimit
from django.contrib.auth.models import User


@ratelimit(key="ip", rate="30/m", block=True)
def auth(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("front_page")
        else:
            messages.success(request, ("There was an error logging in, try again.."))
            return redirect("login")
    return render(request, "login/login.html")


@ratelimit(key="ip", rate="30/m", block=True)
def signup(request, uidb64):
    uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
    to_email = force_str(urlsafe_b64decode(uidb64_padded))
    if request.method == "POST":
        form = SignupForm(request.POST)
        try:
            user = User.objects.get(email=to_email)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is None and form.is_valid():
            user = form.save()
            message = f"Dear {user.username},\n\nYour account has been created successfully.\n\nKind regards,\nCineMY team"
            send_mail(
                "CineMY account creation was successful",
                message,
                settings.CONTACT_EMAIL,
                [to_email],
            )
            messages.success(
                request,
                "Your account has been created successfully",
            )
        else:
            errors_dict = dict(form.errors)
            for field in errors_dict:
                if type(errors_dict[field] == list):
                    for error in errors_dict[field]:
                        messages.success(request, f"\n - {error}")
                else:
                    messages.success(request, f"\n - {errors_dict[field]}")

    return render(request, "login/register.html", {"email": to_email})


@ratelimit(key="ip", rate="30/m", block=True)
def pre_signup(request):
    if request.method == "POST":
        try:
            email = request.POST["email"]
            validate_email(email)
        except ValidationError:
            messages.error(request, ("Email address is not valid"))
            return redirect("pre_signup")
        else:
            encoded_email = urlsafe_base64_encode(force_bytes(email))
            current_site = get_current_site(request)
            message = render_to_string(
                "login/acc_check_email.html",
                {
                    "user": email,
                    "domain": current_site.domain,
                    "uid": encoded_email,
                },
            )
            send_mail(
                "Continue registration on CineMY",
                message,
                settings.CONTACT_EMAIL,
                [email],
            )
            messages.success(
                request, "Please check your email in order to continue registration "
            )
            return redirect("pre_signup")
    if request.method == "GET":
        return render(request, "login/pre_register.html")
