# coding: utf-8
from django import forms
from django.conf import settings
from django.forms import TextInput
# Jong
from jong.models import Rss
# external lib
import requests


def folder(content):
    children = ()
    for child in content:
        children += ((child['title'], child['title']), )
    return children


def folders():
    res = requests.get("http://127.0.0.1:{}/folders".format(settings.JOPLIN_WEBCLIPPER))
    folders = ()
    from pprint import pprint
    pprint(res.json())
    for content in res.json():
        if 'children' in content:
            folders += folder(content['children'])
        folders += ((content['title'], content['title']),)
    return sorted(folders)


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

    notebook = forms.ChoiceField(choices=folders())
