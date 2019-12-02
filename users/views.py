from django.views import View
from django.shortcuts import render


class LoginView(View):
    def get(self, request):
        return render(request, "users/user_login.html")

    def post(self, request):
        pass
