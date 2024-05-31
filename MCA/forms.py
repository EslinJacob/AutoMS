from django import forms
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm


class CustomPasswordResetForm(PasswordResetForm):
    # This class renders the form initiating password reset

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Provide your Email ID',
            }
        )
    )


class CustomSetPasswordForm(SetPasswordForm):
    # This class renders the form for setting new password

    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Enter new password',
            }
        )
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'placeholder': 'Confirm new password',
            }
        )
    )