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
from db import Rss


def load():

    print("opening cvs file")

    with open(JONG_CSV_FILE) as csvfile:

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
                                  date_triggered=str(arrow.utcnow().to(TIME_ZONE)))
                          .execute()
                          )

    print("closing cvs file")


if __name__ == '__main__':
    import argparse
    import os

    cwd = os.getcwd()
    parser = argparse.ArgumentParser(description='JOplin Notes Generator: CSV Loader')
    parser.add_argument('--csv-file', dest='csv_file', default=cwd + '/my_feeds.csv',
                        help='path of the csv file')
    parser.add_argument('--db', dest='db', default=cwd + '/db.sqlite3',
                        help='path to the SQLite database')
    parser.add_argument('--timezone', dest='timezone', default='Europe/Paris',
                        help='Time Zone')

    args = parser.parse_args()
    JONG_CSV_FILE = args.csv_file
    JONG_DB = args.db
    TIME_ZONE = args.timezone
    load()
