from django import forms


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    name = forms.CharField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    phone_number = forms.CharField(max_length=15)
    city = forms.CharField()
    cinema = forms.CharField()
