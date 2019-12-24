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


def github_login(self):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = HttpRequest.build_absolute_uri(
        self, reverse("users:github-callback")
    )

    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&scope=read:user&redirect_uri={redirect_uri}"
    )


def github_callback(request):
    client_id = os.environ.get("GITHUB_ID")
    client_secret = os.environ.get("GITHUB_SECRET")
    code = request.GET.get("code", None)

    if code is not None:
        request = requests.post(
            f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
            headers={"Accept": "application/json"},
        )
        print(request.json())
    else:
        return redirect(reverse("core:home"))


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

