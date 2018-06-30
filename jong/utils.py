# coding: utf-8
from django.conf import settings
# external lib
import requests

"""

   Query the Joplin Webclipper service
   Return the folders
   
"""


def folder(content):
    children = ()
    for child in content:
        children += ((child['title'], child['title']), )
    return children


def folders():
    res = requests.get("http://127.0.0.1:{}/folders".format(settings.JOPLIN_WEBCLIPPER))
    folders = ()
    for content in res.json():
        if 'children' in content:
            folders += folder(content['children'])
        folders += ((content['title'], content['title']),)
    return sorted(folders)
