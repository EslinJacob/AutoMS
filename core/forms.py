from django import forms
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm
)
from django.contrib.auth.models import User

from .models import EmployeeProfile


class SignUpForm(UserCreationForm):
    # This class renders the signup form
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'employee_type',
            'password1',
            'password2',
        )

    employee_type = forms.CharField(
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'Enter type of user: ',
            }
        )
    )


class LoginForm(AuthenticationForm):
    # This class renders the form for logging in a user

    username = forms.CharField(
        widget=forms.TextInput(
            attrs= {
                'placeholder': 'Enter your Username',
            }
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs= {
                'placeholder': 'Enter your password',
            }
        )
    )


class EditUserForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = ("username", "email",)



class EditProfileForm(forms.ModelForm):
    
    class Meta:
        model = EmployeeProfile
        fields = ("employee_type",)
