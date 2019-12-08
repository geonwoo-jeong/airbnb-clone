from django import forms


class LoginForms(forms.Form):

    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
