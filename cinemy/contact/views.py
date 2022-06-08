from django.conf import settings
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from cinema.models import Cinema
from contact.forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages
from ratelimit.decorators import ratelimit


@ratelimit(key="ip", rate="2/m", block=True)
def contact_page(request):
    if request.method == "GET":
        cinemas = Cinema.objects.all()
        return render(request, "contact/contact.html", {"cinemas": cinemas})
    elif request.method == "POST":
        form = ContactForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            try:
                email_subject = f'New email from: {form.cleaned_data["from_email"]}: {form.cleaned_data["subject"]}'
                email_message = form.cleaned_data["message"]
                send_mail(
                    email_subject,
                    email_message,
                    settings.CONTACT_EMAIL,
                    [settings.CONTACT_EMAIL],
                )
                print(email_subject, email_message)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            return render(request, "contact/contact.html")
        else:
            messages.success(request, ("The form was not completed successfully"))
            return redirect("contact_page")
