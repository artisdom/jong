#!/usr/bin/env python
# coding: utf-8
"""
    News generator for creating joplin notes

    The script use the webclipper service port if activated
    otherwise the 'standard' way, by creating MD file and importing them.

"""
# system lib
from __future__ import unicode_literals
import datetime
import json
import shlex
import subprocess
import time

from django.conf import settings

# external lib
import arrow
import feedparser
import pypandoc
import requests
from slugify import slugify

from jong.models import Rss

from logging import getLogger
# create logger
logger = getLogger('jong.jong')


class Core:

    def _joplin_run(self, import_or_set, **kwargs):
        """
        build the commands to run :
        - joplin import
        - joplin set
        :param import_or_set value import / set
        :param kwargs:
        1) if "import", kwargs contains joplin file and notebook to produce the command
        joplin import /path/to/file.md notebook_name
        2) if "set", kwargs contains title or author or source_url file and the associated value to produce the command
        joplin set article-name title "Article Name"
        joplin set article-name author "JohnDoe"
        joplin set article-name source_url "http://url/to/the/article"
        """
        command1 = settings.JOPLIN_BIN

        if settings.JOPLIN_PROFILE:
            command1 += ' --profile {}'.format(settings.JOPLIN_PROFILE)

        if import_or_set == 'import':
            command1 += ' import {} {}'.format(kwargs['joplin_file'], kwargs['notebook'])
        elif import_or_set == 'set':
            command1 += ' set {note} {what} "{value}"'.format(note=kwargs['note'],
                                                              what=kwargs['what'],
                                                              value=kwargs['value'])

        # this will look like
        # joplin --profile /path/to/profile set note-title title|author|source_url value
        commands_args = shlex.split(command1)
        if settings.DEBUG:
            logger.debug(commands_args)
        try:
            result = subprocess.check_call(commands_args, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            result = e
        return True if result == 0 else False

    def _update_date(self, rss_id):
        """
        update the database table  with the execution date
        :param rss_id: id to update
        :return: nothing
        """
        now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
        Rss.objects.filter(id=rss_id).update(date_triggered=now)

    def _get_published(self, entry):
        """
        get the 'published' attribute
        :param entry:
        :return: datetime
        """
        published = None
        if hasattr(entry, 'published_parsed'):
            if entry.published_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(time.mktime(entry.published_parsed))
        elif hasattr(entry, 'created_parsed'):
            if entry.created_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(time.mktime(entry.created_parsed))
        elif hasattr(entry, 'updated_parsed'):
            if entry.updated_parsed is not None:
                published = datetime.datetime.utcfromtimestamp(time.mktime(entry.updated_parsed))
        return published

    def _get_content(self, data, which_content):
        """
        check which content is present in the Feeds to return the right one
        :param data: feeds content
        :param which_content: one of content/summary_detail/description
        :return:
        """
        content = ''

        if data.get(which_content):
            if isinstance(data.get(which_content), feedparser.FeedParserDict):
                content = data.get(which_content)['value']
            elif not isinstance(data.get(which_content), str):
                if 'value' in data.get(which_content)[0]:
                    content = data.get(which_content)[0].value
            else:
                content = data.get(which_content)

        return content

    def get_content(self, entry):
        """
        which content to return ?
        :param entry:
        :return: the body of the RSS data
        """
        content = self._get_content(entry, 'content')

        if content == '':
            content = self._get_content(entry, 'summary_detail')

        if content == '':
            if entry.get('description'):
                content = entry.get('description')

        return content

    def get_data(self, url_to_parse):
        """
        read the data from a given URL or path to a local file
        :param url_to_parse:
        :return: Feeds if Feeds well formed
        """
        data = feedparser.parse(url_to_parse)
        # if the feeds is not well formed, return no data at all
        if data.bozo == 1:
            data.entries = ''

        return data

    def create_note_content(self, entry, name):
        """
        convert the HTML "body" into Markdown
        :param entry:
        :param name:
        :return:
        """
        # call pypandoc to convert html to markdown
        content = pypandoc.convert(self.get_content(entry), 'md', format='html')
        content += '[Provided by {}]({})'.format(name, entry.link)
        return content

    def get_folders(self):
        """

        :return:
        """
        res = requests.get("http://127.0.0.1:{}/folders".format(settings.JOPLIN_WEBCLIPPER))
        return res.json()

    def create_note(self, entry, rss):
        """
        Post a new note to the JoplinWebcliperServer
        :param entry:
        :param rss:
        :return: boolean
        """
        # get the content of the Feeds
        content = self.create_note_content(entry=entry, name=rss.name)
        # build the json data
        folders = self.get_folders()

        notebook_id = 0
        for folder in folders:
            if folder.get('title') == rss.notebook:
                notebook_id = folder.get('id')
        if notebook_id == 0:
            for folder in folders:
                if 'children' in folder:
                    for child in folder.get('children'):
                        if child.get('title') == rss.notebook:
                            notebook_id = child.get('id')
        data = {'title': entry.title,
                'body': content,
                'parent_id': notebook_id,
                'author': rss.name,
                'source_url': entry.link}
        res = requests.post("http://127.0.0.1:{}/notes".format(settings.JOPLIN_WEBCLIPPER), json=data)
        return True if res.status_code == 200 else False

    def create_note_file(self, entry, rss):
        """

        :param entry:
        :param rss:
        :return:
        """
        result = False
        title = slugify(entry.title)
        title = title.strip()
        logger.debug("Creating MD file named ", title)
        # create file one by one
        joplin_file = settings.JONG_MD_PATH + '/' + title + '.md'
        with open(joplin_file, 'w') as out:
            content = self.create_note_content(name=rss.name, entry=entry)
            out.write(content)

        if settings.JOPLIN_BIN:
            # 1 import file
            msg = "importing news ..."
            if settings.JOPLIN_PROFILE:
                msg = "importing news into profile {} ...".format(settings.JOPLIN_PROFILE)
            logger.debug(msg)
            kwargs = {'joplin_file': joplin_file, 'notebook': rss.notebook}
            result = self._joplin_run('import', **kwargs)
            # set the author, title, source_url
            if result:
                if settings.DEBUG:
                    logger.debug("adjust setting ...")
                self._joplin_run('set', **{'note': title, 'what': 'title', 'value': entry.title})
                self._joplin_run('set', **{'note': title, 'what': 'author', 'value': rss.name})
                self._joplin_run('set', **{'note': title, 'what': 'source_url', 'value': entry.link})

            logger.info("imported")
        return result
