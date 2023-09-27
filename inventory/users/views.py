from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, redirect
from django.views.generic import DetailView, RedirectView, UpdateView, View
# social authentication
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.twitter.views import TwitterOAuthAdapter
from dj_rest_auth.social_serializers import TwitterLoginSerializer
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
#
from django.contrib.auth import authenticate, login
from .serializers import *
from .forms import *
#
#
User = get_user_model()


# custom user registration view
class CustomRegisterUser(View):
    def get(self, request):
        form = CustomRegisterForm()
        return render(request, 'account/signup.html', {'form': form})

    def post(self, request):
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            print(form.cleaned_data.get('groups'))
            form.save()
            user = authenticate(email=email, password=raw_password)
            login(request, user)
            user.created_by = user
            user.save()
            # return to add company page
            return redirect('add_company')
        else:
            return render(request, 'account/signup.html', {'form': form})


class CustomUserPermissionView(View):
    def get(self, request):
        return render(request, 'account/permission.html', {})

    def post(self, request):
        user = request.user
        user.is_active = True
        user.save()
        return redirect('home')


class AddCompanyView(View):
    def get(self, request):
        permission_form = CustomUserPermissionForm()
        form = CompanyForm()
        user_preference_form = UserPreferenceForm()
        return render(request, 'account/add_company.html', {
            'form': form,
            "user_preference_form": user_preference_form,
            "permission_form": permission_form,
        })

    def post(self, request):
        form = CompanyForm(request.POST)
        user_preference_form = UserPreferenceForm(request.POST)
        permission_form = CustomUserPermissionForm(request.POST)
        user = User.objects.get(email=request.user.email)
        if form.is_valid() and user_preference_form.is_valid() and permission_form.is_valid():
            for i in permission_form.cleaned_data.get('groups'):
                user.groups.add(i.id)
            user.save()
            form.save(commit=False)
            form.instance.owner = request.user
            form.save()
            user_preference_form.save(commit=False)
            user_preference_form.instance.user = request.user
            user_preference_form.instance.company = form.instance
            user_preference_form.save()

            return redirect('admin:index')
        else:
            return render(request, 'account/add_company.html', {'form': form})


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter


class GoogleLogin(SocialLoginView):  # if you want to use Implicit Grant, use this
    adapter_class = GoogleOAuth2Adapter


class TwitterLogin(SocialLoginView):
    serializer_class = TwitterLoginSerializer
    adapter_class = TwitterOAuthAdapter


class UserDetailView(LoginRequiredMixin, DetailView):

    model = User
    slug_field = "email"
    slug_url_kwarg = "email"

    def get_queryset(self):
        return User.objects.get(email=self.request.user)

    def get_object(self):
        return self.request.user


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):

    model = User
    fields = ["first_name", "last_name", "email", "phone", "image"]
    success_message = _("Information successfully updated")

    def get_success_url(self):
        assert (
            self.request.user.is_authenticated
        )  # for mypy to know that the user is authenticated
        return self.request.user.get_absolute_url()

    def get_object(self):
        return self.request.user


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):

    permanent = False

    def get_redirect_url(self):
        if CompanyUser.objects.filter(user=self.request.user).exists():
            return reverse("admin:index")
        return reverse("add_company")


user_redirect_view = UserRedirectView.as_view()


class GroupViewSet(ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [AllowAny]
