from base64 import urlsafe_b64decode
from django.conf import settings
from django.http import HttpResponse
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
from login.tokens import account_activation_token
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model
from ratelimit.decorators import ratelimit


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
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your CineMY account"
            message = render_to_string(
                "login/acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            send_mail(mail_subject, message, settings.CONTACT_EMAIL, [to_email])
            messages.success(
                request,
                "Please confirm your email address to complete the registration",
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


def activate(request, uidb64, token):
    try:
        uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
        uid = force_str(urlsafe_b64decode(uidb64_padded))
        User = get_user_model()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse(
            "Thank you for your email confirmation. Now you can login your account."
        )
    else:
        return HttpResponse("Activation link is invalid!")


@ratelimit(key="ip", rate="30/m", block=True)
def pre_signup(request):
    if request.method == "POST":
        try:
            validate_email(request.POST["email"])
        except ValidationError:
            messages.error(request, ("Email address is incorrect"))
            return redirect("pre_signup")
        else:
            email = request.POST["email"]
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
