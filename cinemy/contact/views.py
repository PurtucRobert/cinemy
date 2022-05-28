from django.conf import settings
from django.http import BadHeaderError, HttpResponse
from django.shortcuts import redirect, render
from contact.forms import ContactForm
from django.core.mail import send_mail
from django.contrib import messages


def contact_page(request):
    if request.method == "GET":
        return render(request, "contact/contact.html")
    elif request.method == "POST":
        form = ContactForm(request.POST)
        print(form)
        if form.is_valid():
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
