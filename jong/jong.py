#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import arrow
import datetime
import feedparser
import glob
import os
import time

# jong
import db
import settings

import pypandoc
from slugify import slugify
import subprocess


def _update_date(id):
    now = arrow.utcnow().to(settings.TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
    query = (db.Rss.update({db.Rss.date_triggered: now}).where(db.Rss.id == id)).execute()


def _get_published(entry):
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


def _get_content(data, which_content):
    """

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


def get_content(entry):
    """

    :param entry:
    :return:
    """
    content = _get_content(entry, 'content')

    if content == '':
        content = _get_content(entry, 'summary_detail')

    if content == '':
        if entry.get('description'):
            content = entry.get('description')

    return content


def get_data(url_to_parse):
    """
    read the data from a given URL or path to a local file
    :param url_to_parse:
    :return:
    """
    data = feedparser.parse(url_to_parse)

    if data.bozo == 1:
        data.entries = ''

    return data


def main():
    """
        get all the triggers that need to be handled
    """
    file_created = False
    for rss in db.Rss.select().where(db.Rss.status == True):
        print("reading {}".format(rss.name))
        date_triggered = arrow.get(rss.date_triggered).to(settings.TIME_ZONE)

        now = arrow.utcnow().to(settings.TIME_ZONE)

        # retrieve the data
        feeds = get_data(rss.url)

        for entry in feeds.entries:
            # entry.*_parsed may be None when the date in a RSS Feed is invalid
            # so will have the "now" date as default
            published = _get_published(entry)

            if published:
                published = arrow.get(str(published)).to(settings.TIME_ZONE)
            # create md file only for unread item (when publish is less than last triggered execution
            if (date_triggered is not None and published is not None and now >= published >= date_triggered) or \
                    (published is not None and now >= published):

                title = slugify(entry.title)
                title = title.strip()
                print("Creating MD file named ", title)
                # create file one by one
                joplin_file = settings.JONG_MD_PATH + '/' + title + '.md'
                with open(joplin_file, 'w') as out:
                    # call pypandoc to convert html to markdown
                    out.write(pypandoc.convert(get_content(entry), 'md', format='html'))
                    file_created = True

        # import all note once created in the folder to import
        if file_created:
            # execution de joplin import + dossier où sont les fichiers MD + nom du dossier DANS joplin
            if settings.JOPLIN_BIN_PATH:
                command1 = '{}/joplin import {} {}'.format(settings.JOPLIN_BIN_PATH,
                                                           settings.JONG_MD_PATH,
                                                           rss.notebook)
                print(command1)
                process1 = subprocess.Popen(command1, stdout=subprocess.PIPE)
                if process1:
                    # si creation ok
                    _update_date(rss.id)
                    # drop file that have been imported
                    filelist = glob.glob(os.path.join(settings.JONG_MD_PATH, "*.md"))
                    for f in filelist:
                        os.remove(f)
            else:
                print("You don't have set the joplin path, then later, you will need to enter yourself\n"
                      "joplin import {} {}".format(settings.JONG_MD_PATH, rss.notebook))
                # no joplin import done, the user will launch the import himself
                _update_date(rss.id)


if __name__ == '__main__':
    main()
