#!/usr/bin/env python
# coding: utf-8
"""
    News generator for creating joplin notes

    Usage:

    >>> from jong import main
    >>> main()
"""
# system lib
from __future__ import unicode_literals
import argparse
import datetime
import os
import shlex
import subprocess
import time

# external lib
import arrow
import feedparser
import pypandoc
from slugify import slugify

# jong
from db import Rss


__all__ = ['main']


def _joplin_run(import_or_set, **kwargs):
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
    command1 = JOPLIN_BIN

    if JOPLIN_PROFILE:
        command1 += ' --profile {}'.format(JOPLIN_PROFILE)

    if import_or_set == 'import':
        command1 += ' import {} {}'.format(kwargs['joplin_file'], kwargs['notebook'])
    elif import_or_set == 'set':
        command1 += ' set {note} {what} "{value}"'.format(note=kwargs['note'],
                                                          what=kwargs['what'],
                                                          value=kwargs['value'])

    # this will look like
    # joplin --profile /path/to/profile set note-title title|author|source_url value
    commands_args = shlex.split(command1)
    if DEBUG:
        print(commands_args)
    try:
        result = subprocess.check_call(commands_args, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError as e:
        result = e
    return True if result == 0 else False


def _update_date(rss_id):
    """
    update the database table  with the execution date
    :param rss_id: id to update
    :return: nothing
    """
    now = arrow.utcnow().to(TIME_ZONE).format('YYYY-MM-DD HH:mm:ssZZ')
    query = (Rss.update({Rss.date_triggered: now}).where(Rss.id == rss_id)).execute()


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


def get_content(entry):
    """
    which content to return ?
    :param entry:
    :return: the body of the RSS data
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
    :return: Feeds if Feeds well formed
    """
    data = feedparser.parse(url_to_parse)
    # if the feeds is not well formed, return no data at all
    if data.bozo == 1:
        data.entries = ''

    return data


def main():
    """
        Get the activated Feeds
    """
    print("starting ...")

    for rss in Rss.select().where(Rss.status == True):
        file_created = False
        print("reading {}".format(rss.name))
        date_triggered = arrow.get(rss.date_triggered).to(TIME_ZONE)

        now = arrow.utcnow().to(TIME_ZONE)

        # retrieve the data
        feeds = get_data(rss.url)

        for entry in feeds.entries:
            # entry.*_parsed may be None when the date in a RSS Feed is invalid
            # so will have the "now" date as default
            published = _get_published(entry)

            if published:
                published = arrow.get(str(published)).to(TIME_ZONE)
            # create md file only for unread item (when publish is less than last triggered execution
            if date_triggered is not None and published is not None and now >= published >= date_triggered:

                title = slugify(entry.title)
                title = title.strip()
                print("Creating MD file named ", title)
                # create file one by one
                joplin_file = JONG_MD_PATH + '/' + title + '.md'
                with open(joplin_file, 'w') as out:
                    # call pypandoc to convert html to markdown
                    content = pypandoc.convert(get_content(entry), 'md', format='html')
                    content += '[Provided by {}]({})'.format(rss.name, entry.link)
                    out.write(content)

                if JOPLIN_BIN:
                    # 1 import file
                    msg = "importing news ..."
                    if JOPLIN_PROFILE:
                        msg = "importing news into profile {} ...".format(JOPLIN_PROFILE)
                    print(msg)
                    kwargs = {'joplin_file': joplin_file, 'notebook': rss.notebook}
                    result = _joplin_run('import', **kwargs)
                    # set the author, title, source_url
                    if result:
                        if DEBUG:
                            print("adjust setting ...")
                        _joplin_run('set', **{'note': title, 'what': 'title', 'value': entry.title})
                        _joplin_run('set', **{'note': title, 'what': 'author', 'value': rss.name})
                        _joplin_run('set', **{'note': title, 'what': 'source_url', 'value': entry.link})

                    file_created = True
                    print("imported")
        # lets update the date of the handling
        if file_created:

            if JOPLIN_BIN is False:
                print("You don't have set the joplin path, then later, you will need to enter yourself\n"
                      "joplin --profile {} import {} {}".format(JOPLIN_PROFILE, JONG_MD_PATH, rss.notebook))

            _update_date(rss.id)
        else:
            print("no feeds grabbed")


if __name__ == '__main__':
    from pathlib import Path

    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description='JOplin Notes Generator')
    parser.add_argument('--settings', dest='settings', default=cwd + '/settings.py',
                        help='path of the settings of jong')
    parser.add_argument('--joplin-profile', dest='profile', default='',
                        help='joplin path to the profile')
    parser.add_argument('--joplin-bin', dest='bin', default='/usr/bin/joplin',
                        help='default path to the joplin program - default value "/usr/bin/joplin"')
    parser.add_argument('--jong-md-path', dest='jong_md_path', default=cwd + '/import',
                        help='path to store markdown files generated by jong - default value ' + cwd + '/import')
    parser.add_argument('--jong-csv-file', dest='jong_csv_file', default=cwd + '/my_feeds.csv',
                        help='path to my_feeds.csv file - default value ' + cwd + '/my_feeds.csv')
    parser.add_argument('--timezone', dest='timezone', default='Europe/Paris',
                        help='Time Zone - default value "Europe/Paris"')
    parser.add_argument('--debug', dest='debug', default=False,
                        help='running in debug mode')
    args = parser.parse_args()

    my_file = Path(args.bin)

    # settings
    JOPLIN_BIN = args.bin if my_file.is_file() else ''
    DEBUG = args.debug
    JOPLIN_PROFILE = args.profile
    JONG_MD_PATH = args.jong_md_path
    JONG_CSV_FILE = args.jong_csv_file
    TIME_ZONE = args.timezone

    main()
