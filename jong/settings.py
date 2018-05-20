# coding: utf-8
import os
# current dir
cwd = os.getcwd()

JONG_MD_PATH = cwd + '/import/'
JONG_DB = cwd + '/db.sqlite3'
JONG_CSV_FILE = cwd + '/my_feeds.csv'

TIME_ZONE = 'Europe/Paris'

# if empty, no import will be done
JOPLIN_BIN_PATH = ""

# joplin profile to use - if empty, will use the default path
JOPLIN_PROFILE_PATH = ""
