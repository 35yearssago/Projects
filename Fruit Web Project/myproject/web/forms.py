from django import forms
from .models import Profile, Fruit


class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'First Name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Last Name'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email'
            }),
            'password': forms.PasswordInput(attrs={
                'placeholder': 'Password'
            }),
        }


class FruitModelForm(forms.ModelForm):
    class Meta:
        model = Fruit
        fields = '__all__'

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Fruit Name'
            }),
            'image_url': forms.URLInput(attrs={
                'placeholder': 'Fruit Image URL'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Fruit Description'
            }),
            'nutrition': forms.Textarea(attrs={
                'placeholder': 'Nutrition Info'
            }),
        }
        labels = {
            "image_url": "Image URL"
        }