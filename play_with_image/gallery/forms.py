from django import forms
from image.models import Image
from tag_anything.models import TagCategory


class AddImageForm(forms.ModelForm):

    class Meta:
        model = Image
        fields = ['image_name', 'image', 'tags']
        widgets = {
            'image_name': forms.TextInput(attrs={
                'class': 'form-control rounded-0'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control form-control-sm'
            }),
            'tags': forms.SelectMultiple(attrs={
                'class': 'form-select'
            }),
        }


class AddTags(forms.Form):
    tag = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'class': 'tm-text-primary'
            }),
        empty_value='Введите тег',
        label='Таг'
    )
    category = forms.ModelChoiceField(
        queryset=TagCategory.objects.all(),
        label='Категория',
        widget=forms.Select(attrs={
            'style': 'width:150px; padding:none',
        })
    )
