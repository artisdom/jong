#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
import arrow
# django
from django.conf import settings
from django.core.management.base import BaseCommand

# jong
from jong.models import Rss
from jong.core import Core

import requests

from logging import getLogger
# create logger
logger = getLogger('jong.jong')


class Command(BaseCommand):

    help = 'Publish joplin note'

    def handle(self, *args, **options):
        """
            get all the triggers that need to be handled
        """

        res = requests.get('http://127.0.0.1:{}/ping'.format(settings.JOPLIN_WEBCLIPPER))
        if res.text == 'JoplinClipperServer':
            core = Core()
            from django.db import connection
            connection.close()
            data = Rss.objects.filter(status=True)
            file_created = False
            for rss in data:
                file_created = False
                logger.info("reading {}".format(rss.name))
                date_triggered = arrow.get(rss.date_triggered).to(settings.TIME_ZONE)

                now = arrow.utcnow().to(settings.TIME_ZONE)

                # retrieve the data
                feeds = core.get_data(rss.url)

                for entry in feeds.entries:
                    # entry.*_parsed may be None when the date in a RSS Feed is invalid
                    # so will have the "now" date as default
                    published = core._get_published(entry)

                    if published:
                        published = arrow.get(str(published)).to(settings.TIME_ZONE)
                    # create md file only for unread item (when publish is less than last triggered execution
                    if date_triggered is not None and published is not None and now >= published >= date_triggered:

                        if settings.JOPLIN_WEBCLIPPER:
                            file_created = core.create_note(entry, rss)
                        else:
                            file_created = core.create_note_file(entry, rss)

            # lets update the date of the handling
            if file_created:

                if settings.JOPLIN_BIN is False:
                    logger.info("You don't have set the joplin path, then later, you will need to enter yourself\n"
                                "joplin --profile {} import {} {}".format(settings.JOPLIN_PROFILE,
                                                                          settings.JONG_MD_PATH,
                                                                          rss.notebook))

                core._update_date(rss.id)
            else:
                logger.info("no feeds grabbed")
        else:
            logger.info('Check "Tools > Webcliper options"  if the service is enable')


