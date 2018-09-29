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

## Disabling / Enabling Feeds

if you don't need / want to acces to the web app to deal with the status of the feeds

```
./manage.py switch <id> 
``` 

will display 

```python
./manage.py switch 24
Successfully switched RSS "24"
```

then to check the status

``` ptyhon
./manage.py report
ID    Name                           Triggered              Notebook                       Status Bypass Error?
   28 Gamekult                       2018-08-22 18:27       News                           0      No 
   26 Gameblog                       2018-08-18 14:21       News                           0      Yes
   24 Frandroid                      2018-09-29 19:55       Smartphone                     1      Yes
    5 Python Planet                  2018-09-27 19:00       Python                         1      Yes
   25 Numerama                       2018-09-27 19:00       News                           1      Yes
   29 GithubBlog                     2018-09-25 22:20       Github                         1      No 
   23 Github                         2018-09-20 18:27       Github                         1      No 
    8 Un Odieux Connard              2018-09-20 18:27       Connard                        1      No 
    7 Sam et Max                     2018-09-09 16:00       Python                         1      No 
    9 Django                         2018-08-31 19:00       Django                         1      No 
```

## Running Tests

run this if you want to be sure that everything is fine   
```
./manage.py test -v2 
``` 


## VueJS UI

You can still use JONG with just Django or with VueJS if you prefer.
To do so have a look at the README.md in the frontend folder
