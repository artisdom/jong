# coding: utf-8
import os
# current dir
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

JONG_MD_PATH = BASE_DIR + '/import/'
JONG_DB = BASE_DIR + '/jong/jong.sqlite'

TIME_ZONE = 'Europe/Paris'

# if empty, no import will be done

JOPLIN_BIN_PATH = ""
