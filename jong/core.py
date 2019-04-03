#!/usr/bin/env python
# coding: utf-8
"""
    News generator for creating joplin notes

    The script use the webclipper service port - 
    Enable the service from the menu "Tools > Webclipper option"

    Launch

    python manage.py run

    Have Fun
"""
# std lib
from __future__ import unicode_literals
import datetime
from logging import getLogger
import time
# external lib
import asks
import arrow
import feedparser
import pypandoc
import trio
# django
from django.conf import settings
# project
from jong.models import Rss
# create logger
logger = getLogger('jong.jong')

asks.init('trio')


class Core:

    def _update_date(self, rss_id):
        """
        update the database table  with the execution date
        :param rss_id: id to update
        :return: nothing
        """
        now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
        Rss.objects.filter(id=rss_id).update(date_triggered=now)

    def get_published(self, entry):
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

    async def get_data(self, url_to_parse, bypass_bozo=False):
        """
        read the data from a given URL or path to a local file
        :param url_to_parse:
        :param bypass_bozo: boolean to ignore not well formed Feeds
        :return: Feeds if Feeds well formed
        """
        data = await asks.get(url_to_parse)
        data = feedparser.parse(data.text)
        # if the feeds is not well formed, return no data at all
        if bypass_bozo is False and data.bozo == 1:
            data.entries = ''
            log = f"{url_to_parse}: is not valid. You can tick the checkbox "
            "'Bypass Feeds error ?' to force the process"
            logger.info(log)

        return data

    async def create_note_content(self, entry, name):
        """
        convert the HTML "body" into Markdown
        :param entry:
        :param name:
        :return:
        """
        # call pypandoc to convert html to markdown
        content = pypandoc.convert(self.get_content(entry), settings.PYPANDOC_MARKDOWN, format='html')
        content += '\n[Provided by {}]({})'.format(name, entry.link)
        return content

    async def get_folders(self):
        """
        get the list of all the folders of the joplin profile
        :return:
        """
        res = await asks.get("http://127.0.0.1:{}/folders".format(settings.JOPLIN_WEBCLIPPER))
        return res.json()

    async def create_note(self, entry, rss):
        """
        Post a new note to the JoplinWebclipperServer
        :param entry:
        :param rss:
        :return: boolean
        """
        # get the content of the Feeds
        content = await self.create_note_content(entry=entry, name=rss.name)
        # build the json data
        folders = await self.get_folders()

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
        url = "http://127.0.0.1:{}/notes".format(settings.JOPLIN_WEBCLIPPER)
        res = await asks.post(url, json=data)
        if res.status_code == 200:
            self._update_date(rss.id)
            log = "{}: article added {}".format(rss.name, entry.title)
            logger.info(log)


async def go():

    if settings.JOPLIN_WEBCLIPPER:
        res = await asks.get('http://127.0.0.1:{}/ping'.format(settings.JOPLIN_WEBCLIPPER))
        if res.text == 'JoplinClipperServer':
            core = Core()
            data = Rss.objects.filter(status=True)

            async with trio.open_nursery() as n:

                for rss in data:
                    log = "reading {}".format(rss.name)
                    logger.info(log)
                    date_triggered = arrow.get(rss.date_triggered).to(settings.TIME_ZONE)

                    now = arrow.utcnow().to(settings.TIME_ZONE)

                    # retrieve the data
                    feeds = await core.get_data(rss.url, rss.bypass_bozo)
                    for entry in feeds.entries:
                        # entry.*_parsed may be None when the date in a RSS Feed is invalid
                        # so will have the "now" date as default
                        published = core.get_published(entry)
                        if published:
                            published = arrow.get(str(published)).to(settings.TIME_ZONE)
                        # create md file only for unread item (when publish is less than 
                        # last triggered execution
                        if date_triggered is not None and published is not None \
                        and now >= published >= date_triggered:
                            n.start_soon(core.create_note, entry, rss)
    else:
        logger.info('Check "Tools > Webclipper options"  if the service is enable')
