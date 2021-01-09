from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text="Required. Inform a valid email address")

    def clean_email(self):
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("Email is already registered")
        return self.cleaned_data["email"]

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2", )
