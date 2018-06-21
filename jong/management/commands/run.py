#!/usr/bin/env python
# coding: utf-8
from __future__ import unicode_literals
from django.core.management.base import BaseCommand
# jong
from jong.core import go
# std lib
from logging import getLogger
# external lib
import trio
# create logger
logger = getLogger('jong.jong')


class Command(BaseCommand):

    help = 'Publish joplin note'

    def handle(self, *args, **options):
        """
            get all the feeds and publish a note for each of them
        """
        trio.run(go)
