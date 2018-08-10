# coding: utf-8
from django.conf import settings
# external lib
import requests

"""

   Query the Joplin Webclipper service
   Return the folders

"""


def folder(content):
    """
    get the child folders
    :param content:
    :return:
    """
    children = ()
    for child in content:
        children += ((child['title'], child['title']), )
    return children


def folders():
    """
    get the folders of joplin
    :return: sorted folders
    """
    res = requests.get("http://127.0.0.1:{}/folders".format(settings.JOPLIN_WEBCLIPPER))
    folders = ()
    for content in res.json():
        if 'children' in content:
            folders += folder(content['children'])
        folders += ((content['title'], content['title']),)
    return sorted(folders)


def folders_set():
    """
    get the folders of my joplin installation
    sort them
    :return: sorted folders as expected by VueJS
    """
    import itertools
    sorted_folder = sorted(list(set(itertools.chain.from_iterable(folders()))))
    data = []
    for f in sorted_folder:
        data.append({'text': f, 'value': f})
    return data
