from ratelimit.decorators import ratelimit
from django.shortcuts import render
from django.contrib.auth.models import User
from newsletter.forms import NewsletterForm
from newsletter.models import Newsletter
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from base64 import urlsafe_b64decode
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages


def send_subscription_email(email=None):
    email_message = render_to_string(
        "newsletter/newsletter_email.html", {"user": email}
    )
    email_subject = "You have successfully subscribed to the newsletter !"
    send_mail(
        email_subject,
        email_message,
        settings.CONTACT_EMAIL,
        [email],
    )


def send_newsletter(movie, emails=[]):
    email_message = render_to_string(
        "newsletter/newsletter_movies.html", {"movie": movie}
    )
    email_subject = f"{movie.name} is rolling out!"
    send_mail(
        email_subject,
        email_message,
        settings.CONTACT_EMAIL,
        emails,
    )


@ratelimit(key="ip", rate="2/m", block=True)
def newsletter_page(request):
    if request.method == "GET":
        return render(request, "newsletter/newsletter.html")
    if request.method == "POST":
        form = NewsletterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            current_site = get_current_site(request)
            email_message = render_to_string(
                "newsletter/confirm_subscription.html",
                {
                    "user": email,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(email)),
                },
            )
            email_subject = "Please confirm your subscription to CineMY !"
            send_mail(
                email_subject,
                email_message,
                settings.CONTACT_EMAIL,
                [email],
            )
        messages.success(
            request=request,
            message="An email has been sent in order to confirm the subscription to CineMY",
        )
        return render(request, "newsletter/newsletter.html")


def confirm_subscription(request, uidb64):
    uidb64_padded = uidb64 + "=" * (-len(uidb64) % 4)
    email = force_str(urlsafe_b64decode(uidb64_padded))
    Newsletter.objects.create(email=email)
    send_subscription_email(email=email)
    return HttpResponse("Thank you for subscribing to our cinemas")


@ratelimit(key="ip", rate="2/m", block=True)
def newsletter_registered_user(request, pk):
    user = User.objects.get(pk=pk)
    try:
        Newsletter.objects.get(user=user)
    except Newsletter.DoesNotExist:
        Newsletter.objects.create(user=user, email=user.email)
        send_subscription_email(email=user.email)
        return render(
            request,
            "newsletter/newsletter.html",
            {"message": "Successfully subscribed to the newsletter"},
        )
    else:
        return render(
            request,
            "newsletter/newsletter.html",
            {"message": "You are already subscribed to the newsletter"},
        )
