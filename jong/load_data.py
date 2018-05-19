#!/usr/bin/env python
# coding: utf-8
import csv
from db import Rss

"""
this module load a CVS file into a sqlite database
"""


def main():

    print("opening cvs file")

    with open('my_feeds.csv') as csvfile:

        print("reading cvs file")

        fieldnames = ['name', 'notebook', 'url', 'tag', 'status']
        reader = csv.DictReader(csvfile, fieldnames=fieldnames)
        for row in reader:
            print(row['name'], row['notebook'], row['url'], row['tag'], row['status'])
            status = bool(row['status'])
            # insert or update
            my_rss = (Rss
                      .replace(name=row['name'],
                               notebook=row['notebook'],
                               url=row['url'],
                               tag=row['tag'],
                               status=status)
                      .execute()
                      )
    print("closing cvs file")


if __name__ == '__main__':
    main()
