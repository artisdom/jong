#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand, CommandError
# jong
from jong.models import Rss
# std lib
from logging import getLogger
# create logger
logger = getLogger('jong.jong')


class Command(BaseCommand):

    help = 'Switch the status of a given Rss Feed. On if off or Off if On'

    def add_arguments(self, parser):
        parser.add_argument(dest='id', nargs='+', help='id of the feed to switch the status')

    def handle(self, *args, **options):
        for rss_id in options['id']:
            try:
                rss = Rss.objects.get(pk=rss_id)
            except Rss.DoesNotExist:
                raise CommandError('Rss "%s" does not exist' % rss_id)

            rss.status = not rss.status
            rss.save()

            self.stdout.write(self.style.SUCCESS('Successfully switched RSS "%s"' % rss_id))
