from django.views import View
from django.shortcuts import render
from . import forms


class LoginView(View):
    def get(self, request):
        form = forms.LoginForms()
        return render(request, "users/user_login.html", {"form": form})

    def post(self, request):
        form = forms.LoginForms(request.POST)
        print(form)
