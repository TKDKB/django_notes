from django import forms

from registration.models import User


class PasswordResetForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput, label="Пароль")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Повторите пароль")

    def clean(self):
        data = self.cleaned_data
        if data["password1"] != data["password2"]:
            print("bitch")
            raise forms.ValidationError("Пароли не совпадают!")
        print("mf")
        return data

    class Meta:
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "password1": forms.PasswordInput(attrs={"class": "form-control"}),
            "password2": forms.PasswordInput(attrs={"class": "form-control"}),
        }

