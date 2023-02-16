from django import forms
from django.contrib.auth import authenticate, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from base.models import User
from base.widgets import CustomFileInput


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=255, widget=forms.EmailInput)
    password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"]
        return email.lower()

    def is_valid(self):
        super().is_valid()
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]
        user = authenticate(email=email, password=password)
        if user:
            return True
        return False


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=127)

    class Meta:
        model = User
        fields = ("avatar", "email", "name", "usertype", "password1", "password2")


class UserUpdateForm(forms.ModelForm):
    avatar = forms.FileField(widget=CustomFileInput)

    class Meta:
        model = User
        fields = ("avatar", "email", "name", "usertype")


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(
        label=_("Old password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "autofocus": True}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validate that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError("Incorrect current password.")
        return old_password

    def clean_new_password2(self):
        password1 = self.cleaned_data.get("new_password1")
        password2 = self.cleaned_data.get("new_password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two passwords didnt match.")
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["new_password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(max_length=127)

    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            user = None
        if not user:
            raise forms.ValidationError("Email not registered in our database.")


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )
    password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError("The two passwords didnt match.")
        password_validation.validate_password(password2, self.user)
        return password2

    def save(self, commit=True):
        password = self.cleaned_data["password1"]
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user
