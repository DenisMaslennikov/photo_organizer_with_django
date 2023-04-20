from django import forms
from .models import Image


class AddImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image_name', 'image', 'tags']
        widgets = {
            'image_name': forms.TextInput(attrs={
                'class': 'form-control rounded-0'}),
            'image': forms.FileInput(attrs={
                'class': 'form-control form-control-sm'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-select'}),

        }
