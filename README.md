#  JONG: JOplin Notes Generator

## Description

This is a little project to automatically create note in Joplin, by reading RSS Feeds

##  Requirements

* Python 3.6+
* Django 2
* arrow: to handle date comparison
* feedparser: the great lib to handle RSS/Atom file
* pypandoc: file format converted
* asks: async http
* trio: async made easy
* requests: HTTP for Humans

## Installation

```
python3 -m venv jong
cd jong
source bin/activate
git clone https://github.com/foxmask/jong
cd jong
pip install -r requirements.txt
```

## Create the database

```
./manage migrate
```

## Starting the app

```
./manage runserver &
```

## Defining RSS Feeds

access to `http://127.0.0.1:8000/` and add your feeds

## Settings of JONG / Joplin

In the `settings.py` file, just provide the Joplin Webclipper port, eg:
```
# Where is Joplin
# the port used by the webclipper from the menu "Tools > Webclipper option"
JOPLIN_WEBCLIPPER = 41184
```

## Running Jong

run joplin desktop to enable the webclipper service, then 

```
./manage.py run 
``` 

this will display the name of the feed 
Have a look at your Joplin desktop to find your news :)

## Running Tests

run this  
```
./manage.py test -v2 
``` 
