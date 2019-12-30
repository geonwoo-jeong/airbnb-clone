import os
import requests
from django.views.generic import FormView
from django.shortcuts import render, redirect, reverse
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login, logout
from . import forms, models
from django.http.request import HttpRequest


class SignUpView(FormView):

    template_name = "users/user_signup.html"
    form_class = forms.SignUpForm
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        form.save()
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        user.verify_email()

        return super().form_valid(form)


class LoginView(FormView):

    template_name = "users/user_login.html"
    form_class = forms.LoginForms
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            login(self.request, user)

        return super().form_valid(form)


def log_out(request):
    logout(request)

    return redirect("core:home")


def complete_verification(request, key):
    try:
        user = models.User.objests.get(email_secret=key)
        user.email_verified = True
        user.email_secret = ""
        user.save()
        # todo: add success message
    except models.User.DoesNotExist:
        # todo: add error message
        pass

    return redirect(reverse("core:home"))


class GithubException(Exception):
    pass


def github_login(self):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = HttpRequest.build_absolute_uri(
        self, reverse("users:github-callback")
    )

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=read:user&redirect_uri={redirect_uri}"
    )


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)

        if code is None:
            return redirect(reverse("core:home"))

        # Get Token

        token_request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        token_json = token_request.json()
        error = token_json.get("error", None)

        if error is not None:
            raise GithubException("Can't get access token")

        # Get Access Token

        access_token = token_json.get("access_token")
        profile_request = requests.get(
            "https://api.github.com/user",
            headers={
                "Authorization": f"token {access_token}",
                "Accept": "application/json",
            },
        )
        profile_json = profile_request.json()
        username = profile_json.get("login", None)

        if username is None:
            raise GithubException("Can't get your profile")

        # Set User Information

        name = profile_json.get("name")
        email = profile_json.get("email")
        bio = profile_json.get("bio")

        try:
            user = models.User.objects.get(email=email)

            if user.login_method != models.User.LOGIN_GITHUB:
                raise GithubException(f"Please log in with: {user.login_method}")

        except models.User.DoesNotExist:
            user = models.User.objects.create(
                email=email,
                first_name=name,
                username=email,
                bio=bio,
                login_method=models.User.LOGIN_GITHUB,
                email_verified=True,
            )
            user.set_unusable_password()
            user.save()

        login(request, user)

        return redirect(reverse("core:home"))

    except GithubException as e:
        print(e)
        return redirect(reverse("users:login"))


# class LoginView(View):
#     def get(self, request):
#         form = forms.LoginForms()

#         return render(request, "users/user_login.html", {"form": form})

#     def post(self, request):
#         form = forms.LoginForms(request.POST)

#         if form.is_valid():
#             email = form.cleaned_data.get("email")
#             password = form.cleaned_data.get("password")
#             user = authenticate(request, username=email, password=password)

#             if user is not None:
#                 login(request, user)

#                 return redirect("core:home")

#         return render(request, "users/user_login.html", {"form": form})

