# coding: utf-8
from django import forms
from django.forms import TextInput
# Jong
from jong.models import Rss
from jong.utils import folders


class RssForm(forms.ModelForm):

    """
        RSS Form
    """
    def __init__(self, *args, **kwargs):
        # Get initial data passed from the view
        super(RssForm, self).__init__(*args, **kwargs)
        self.fields['notebook'].choices = folders()

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

    notebook = forms.ChoiceField()
