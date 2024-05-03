# Installation project

## Installation

```bash
$ git clone
$ cd

# Install dependencies
poetry install
```

## Configuration

```bash
# set postgresql database data to settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': '<database_name>',
        'USER' : '<user>',
        'PASSWORD' : '<password>',
        'HOST' : '<host>', # default: 'localhost'
        'PORT' : '<port>', # default: '5432'
    }
```

## Usage

```bash
$ poetry shell # Activate virtual environment
$ python manage.py runserver # Run server
```

## To run tasks

```bash
$ python manage.py parsing_task # Run parsing task 
```