from django.contrib.auth.forms import UserCreationForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django import forms
from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from inventory.common.models import *


User = get_user_model()


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }


class UserSignupForm(SignupForm):
    """
    Form that will be rendered on a user sign up section/screen.
    Default fields will be added automatically.
    Check UserSocialSignupForm for accounts created from social.
    """


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """


# custom form for user registration
class CustomRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["email", "password1", "password2", "first_name", "last_name", "phone"]


class CustomUserPermissionForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["groups"]


# form to add company
class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['title', 'company_type']


# form to add user preferences
class UserPreferenceForm(forms.ModelForm):
    class Meta:
        model = UserPreference
        fields = ['language', 'currency']
