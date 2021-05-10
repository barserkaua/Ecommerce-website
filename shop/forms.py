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
    CHOICE_REGION = {
        ('львівська область', 'Львівська область'),
        ('волиська область', 'Волинська область'),
        ('тернопільська область', 'Тернопільська область'),
        ('рівненська область', 'Рівненська область'),
    }

    CHOICE_SHIPPING = {
        ('самовивіз', 'Самовивіз'),
        ('нова пошта', 'Нова пошта'),
        ('укрпошта', 'Укрпошта'),
    }

    CHOICE_PAYMENT = {
        ('готівка', 'Готівка'),
        ('на карточку', 'На карточку'),
    }

    user_name = forms.CharField(label="Прізвище/Ім'я", max_length=100, required=True)
    email = forms.EmailField(max_length=250, help_text='Приклад: eg.youremail@gmail.com')
    phone = forms.IntegerField()
    region = forms.ChoiceField(choices=CHOICE_REGION)
    shipping = forms.ChoiceField(choices=CHOICE_SHIPPING)
    payment = forms.ChoiceField(choices=CHOICE_PAYMENT)

    class Meta:
        model = Order
        fields = ('user_name', 'email', 'phone', 'region', 'shipping', 'payment')

        widgets = {
            "user_name": TextInput(attrs={
                'class': 'form-control',
                'placeholder': "Прізвище/Ім'я"
            }),
            "phone": TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефону'
            }),

        }
