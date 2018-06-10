# coding: utf-8
from django import forms
from django.forms import TextInput

# Jong
from jong.models import Rss


class RssForm(forms.ModelForm):

    """
        RSS Form
    """
    class Meta:

        model = Rss
        exclude = ('date_triggered',)
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'url': TextInput(attrs={'class': 'form-control'}),
            'notebook': TextInput(attrs={'class': 'form-control'}),
            'tag': TextInput(attrs={'class': 'form-control'}),
            'status': TextInput(attrs={'class': 'form-control'}),
        }
