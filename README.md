# JONG: JOplin Note Generator

## Description

This is a little project to automatically create note in Joplin, by reading RSS Feeds

## Requirements

* Python 3+
* peewee: for the database
* arrow: to handle date comparison
* feedparser: the great lib to handle RSS/Atom file
* pypandoc: file format converted

## Installation

```
python3 -m venv jong
cd jong
source bin/activate
git clone https://github.com/foxmask/jong
cd jong
python setup.py install
cd ..
```

## Defining RSS Feeds

Put you Feeds in a CSV file named `my_feeds.csv`

```csv
"foxmask","blog","https://foxmask.net/feeds/all.rss.xml","",1
"sam et max","blog","http://sametmax.com/feed/","",1
``` 
where:

* first column: a name of the feeds
* second column: the joplin folder name where the notes of that feeds will be stored
* third column: the Feeds URL
* fourth column: the joplin tag you want to associate for that feeds
* fifth column: the status, 1 active , 0 not active. Thus you can add many feeds and when you want to disable one of the ; set this column to 0

## Loading Feeds

launch

```
jong-load
```

this will read `my_feeds.csv` and:

if the data does not exist, it creates it
if the data already exists, it updates it. Thus for existing handled Feeds, the date of the last handling is still in the database 

## Settings 

in the `settings.py` file, you can set those parms :

```python  
JONG_MD_PATH = cwd + '/import/'
JONG_DB = cwd + '/db.sqlite3'
JONG_CSV_FILE = cwd + '/my_feeds.csv'

TIME_ZONE = 'Europe/Paris'

# if empty, no import will be done

JOPLIN_BIN_PATH = ""

# joplin profile to use - if empty, will use the default path
JOPLIN_PROFILE_PATH = ""
```

* `JONG_MD_PATH` is the path where to create the markdown file to import
* `JONG_CSV_FILE` the path of the CSV file
* `TIME_ZONE` is your own timezone
* `JOPLIN_PROFILE_PATH` 
* `JOPLIN_BIN_PATH` is the path where to find Joplin. If not set, the import of markdown will not be triggered by joplin_notegen.
Then you can launch the import by yourself with :

```
jopline import <value of JONG_MD_PATH settings> <folder_name>  
```

## Running Jong

it runs in 2 steps.

One for grabbing the content of each RSS/Atom Feeds
One for creating the markdown file associated 

One optional, to import that file in joplin. This one will be done if you have set JOPLIN_BIN_PATH
Otherwise, the markdown file will be created, and you could import them later when you want by yourself. 

so launch:
```
jong-run
``` 

Enjoy!