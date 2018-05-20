#!/usr/bin/env python
# coding: utf-8
"""
    this module load a CVS file into a sqlite database

    Usage:

    >>> from jong import load
    >>> load()
"""
import arrow
import csv
from jong import Rss
from jong import settings


def load():

    print("opening cvs file")

    with open(settings.JONG_CSV_FILE) as csvfile:

        print("reading cvs file")

        fieldnames = ['name', 'notebook', 'url', 'tag', 'status']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            print("importing ... ", row['name'], row['notebook'], row['url'], row['tag'], row['status'])
            status = int(row['status'])

            query = (Rss.select().where(Rss.name == row['name']))
            if query.count() > 0:
                for data in query:
                    data.notebook = row['notebook']
                    data.url = row['url']
                    data.tag = row['tag']
                    data.status = status
                    data.save()
            else:
                my_rss = (Rss
                          .insert(name=row['name'],
                                  notebook=row['notebook'],
                                  url=row['url'],
                                  tag=row['tag'],
                                  status=status,
                                  date_triggered=arrow.utcnow().to(settings.TIME_ZONE))
                          .execute()
                          )

    print("closing cvs file")


if __name__ == '__main__':
    load()
