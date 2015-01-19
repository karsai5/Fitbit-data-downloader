# Fitbit-data-downloader
A python application that will download your daily step count into a csv file.

# Installation
## Virtualenv
Virtualenv is a tool to created isolated Python enviroments, It ensures that
you have the same enviroment used to create the application. It's recommended
that you use it when running the Fitbit-data-dowloader, you can find
instructions on that over
[here](https://virtualenv.pypa.io/en/latest/installation.html).

## Requirements 
*These instructions assume that you have Virtualenv installed.*
Create a venv directory.

```
$ virtualenv env
```

Install the python requirements for the application.

```
$ ./env/bin/pip install -r requirements.txt
```

# Running
## Creating a fitbit App
 - Head over to [https://dev.fitbit.com/apps/new](https://dev.fitbit.com/apps/new)
and create a new fitbit app. 
 - Copy your app's client *key* and *secret* into the appropriate variables in the keys-example.py file.
 - Rename keys-example.py to keys.py

## Downloading your data
Simply run the app using the python executable from inside your virutalenv.

```
$ ./env/bin/python fitbit-downloader.py
```

It should open up a webpage asking for you permission to access data from you
account, select accept and copy the the pin into your terminal. If all goes
well it should download your daily step count since the creation of your account.
