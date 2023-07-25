from django import forms
from .models import Card

class CreateCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'description']

class UpdateCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['title', 'description']

