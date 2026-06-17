from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Trip, TripPhoto


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Email')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class TripForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    rating_transport = forms.ChoiceField(
        choices=RATING_CHOICES, label='Удобство передвижения',
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    rating_safety = forms.ChoiceField(
        choices=RATING_CHOICES, label='Безопасность',
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    rating_population = forms.ChoiceField(
        choices=RATING_CHOICES, label='Населённость',
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )
    rating_nature = forms.ChoiceField(
        choices=RATING_CHOICES, label='Растительность',
        widget=forms.RadioSelect(attrs={'class': 'btn-check'})
    )

    class Meta:
        model = Trip
        fields = [
            'title', 'description', 'location_name',
            'latitude', 'longitude', 'cost',
            'rating_transport', 'rating_safety',
            'rating_population', 'rating_nature',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'latitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': '55.751244'}),
            'longitude': forms.NumberInput(attrs={'step': 'any', 'placeholder': '37.618423'}),
        }
        labels = {
            'title': 'Название',
            'description': 'Описание',
            'location_name': 'Место',
            'latitude': 'Широта',
            'longitude': 'Долгота',
            'cost': 'Стоимость (руб.)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if not isinstance(field.widget, forms.RadioSelect):
                field.widget.attrs['class'] = 'form-control'


class TripPhotoForm(forms.ModelForm):
    class Meta:
        model = TripPhoto
        fields = ['image', 'caption']
        labels = {
            'image': 'Фотография',
            'caption': 'Подпись к фото',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'