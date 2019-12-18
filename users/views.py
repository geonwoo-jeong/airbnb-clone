from django.views import View
from django.shortcuts import render, redirect, reverse
from django.contrib.auth import authenticate, login, logout
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForms()

        return render(request, "users/user_login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForms(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=email, password=password)

            if user is not None:
                login(request, user)

                return redirect("core:home")

        return render(request, "users/user_login.html", {"form": form})


def log_out(request):
    logout(request)

    return redirect("core:home")

