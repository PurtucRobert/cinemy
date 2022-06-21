from django.forms import ModelForm
from newsletter.models import Newsletter


class NewsletterForm(ModelForm):
    class Meta:
        model = Newsletter
        exclude = ("user",)
