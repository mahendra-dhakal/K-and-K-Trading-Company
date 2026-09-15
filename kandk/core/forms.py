from django import forms

from .models import Enquiry


class EnquiryForm(forms.ModelForm):
    # Honeypot field: real visitors never see or fill this in (hidden via CSS).
    # Bots that auto-fill every field will trip it, and the view silently
    # drops the submission without saving it.
    website = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"autocomplete": "off", "tabindex": "-1"}),
    )

    class Meta:
        model = Enquiry
        fields = ["full_name", "email", "phone_number", "company", "subject", "message"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name", "class": "form-control"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@company.com", "class": "form-control"}),
            "phone_number": forms.TextInput(attrs={"placeholder": "+977 98X XXX XXXX", "class": "form-control"}),
            "company": forms.TextInput(attrs={"placeholder": "Company name (optional)", "class": "form-control"}),
            "subject": forms.TextInput(attrs={"placeholder": "How can we help?", "class": "form-control"}),
            "message": forms.Textarea(
                attrs={"placeholder": "Tell us a bit about your enquiry...", "class": "form-control", "rows": 5}
            ),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website")
        if value:
            raise forms.ValidationError("Spam detected.")
        return value

    def clean_full_name(self):
        value = self.cleaned_data.get("full_name", "").strip()
        if len(value) < 2:
            raise forms.ValidationError("Please enter your full name.")
        return value

    def clean_message(self):
        value = self.cleaned_data.get("message", "").strip()
        if len(value) < 10:
            raise forms.ValidationError("Please provide a few more details in your message.")
        return value
