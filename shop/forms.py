from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, DateTimeInput, Textarea
from .models import Order


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='Приклад: eg.youremail@gmail.com')

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 'email')


class OrderForm(ModelForm):

    class Meta:
        model = Order
        fields = ('user_name', 'phone')

        widgets = {
            "user_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Фамілія/Ім'я"
            }),
            "phone": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефону'
            }),
        }