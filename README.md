#  JONG: JOplin Notes Generator

## Description

This is a little project to automatically create notes in [Joplin](https://github.com/laurent22/joplin), by reading RSS Feeds

##  Requirements

* Python 3.6+
* Django 2
* django-environ: to deal with settings
* arrow: to handle date comparison
* feedparser: the great lib to handle RSS/Atom file
* pypandoc: file format converter
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

this will start the app on this URL `http://127.0.0.1:8000/`

## Defining RSS Feeds

access to `http://127.0.0.1:8000/` and add your feeds

## Settings of JONG / Joplin

Copy `env.sample` file to `.env` and if you want to set different value for the setting
 
```
# Where is Joplin
# the port used by the webclipper from the menu "Tools > Webclipper option"
JOPLIN_WEBCLIPPER = 41184
```

## Running Jong

run joplin desktop to enable the webclipper service, then start JONG by:

```
./manage.py run 
``` 

this will display the name of the feed 
Have a look at your Joplin desktop to find your news :)

## Reporting

run this command

```
./manage.py report 
``` 

to get the list of your feeds to check which one provided articles or not


```shell
Name                           Triggered              Notebook                       Bypass Error?
Python Planet                  2018-07-08 09:00       Python                         Yes
Sam et Max                     2018-07-04 17:00       Python                         No 
Django                         2018-07-04 17:00       Django                         No 
Un Odieux Connard              2018-07-04 17:00       Connard                        No 
foxmask                        2018-06-29 18:01       Projets                        No 
```

this allow you to avoid to start the application and launch the browser, if you do not plan to add a new feed

## Running Tests

run this if you want to be sure that everything is fine   
```
./manage.py test -v2 
``` 
