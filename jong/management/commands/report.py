#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
# jong
from jong.models import Rss
# std lib
from logging import getLogger
# create logger
logger = getLogger('jong.jong')


class Command(BaseCommand):

    help = 'List the handled Feeds'

    def handle(self, *args, **options):
        """
            get all the feeds and publish a note for each of them
        """

        data = Rss.objects.all().order_by('status', '-date_triggered')
        print("{:<5} {:<30} {:<22} {:<30} {:<6} {:<3}".format("ID", "Name", "Triggered", "Notebook", "Status",
                                                              "Bypass Error?"))

        for rss in data:
            bozo = "Yes" if rss.bypass_bozo else "No"
            fill = '      '
            print("{:5} {:<30} {:%Y-%m-%d %H:%M}{} {:<30} {:<6} {:<3}".format(rss.id, rss.name, rss.date_triggered,
                                                                              fill, rss.notebook, rss.status, bozo))
