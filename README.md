# Institution Comparer

Standalone website solution built for displaying rankings of various institutions.


# Functionalities

* ranking table allowing to compare institutions by scores divided between
  categories and criteria
* criteria description page
* details page for each institution
* editable static content powered with [Django CMS](https://www.django-cms.org)
* institution data import from CSV files
* simple blog
* simple contact form


# Installation

This procedure describes how to run this project in development mode on your local machine.

To setup for production environment please follow:
[Deploying Django](https://docs.djangoproject.com/en/3.2/howto/deployment/).


## Prerequisites

* Linux environment
* required system packages:
  * `python3`
  * `python3-pip`
  * `python3-virtualenv`
  * `node`
  * `npm`


## Configuration

* Create directory for your project.

* Clone this repository as `institution-comparer` subdirectory of your project's directory.

* Create `institution-comparer/main/local_settings.py` file and edit
  the file to add project specific settings:

Required:

```python
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Optional:

```python
DEBUG = True  # Turn it off in production

PROJECT_TITLE = 'Title of your project'

# For e-mail related settings follow:
# https://docs.djangoproject.com/en/3.2/ref/settings/#email-backend

POLICY_CATEGORY_SLUGS = [
  'category-1', 'category-2', 'category-3'
  # These are slug names of the policy categories which should to be
  # created by the admin panel at:
  # http://localhost:8000/admin/comparer/policycategory/add/
  # They are hardcoded due to performance reasons.
]
INSTITUTION_NAME = 'Kind of the institution your ranking is about'

GA_MEASUREMENT_ID = 'Your GoogleAnalytics ID'

ADOBE_FONT_ID = 'Font link id generated via https://fonts.adobe.com/'

```


## Building project

Run script:
```bash
institution-comparer/install.sh
```


## Running development server

Run script:
```bash
institution-comparer/run.sh runserver 8000
```

The website should now be running at: http://localhost:8000


## Content editing tools and the admin panel

To add or edit contents and access the admin panel you have to create
superuser account. To do this run:
```bash
institution-comparer/run.sh createsuperuser
```
And follow the instructions.
You can then login by adding `?edit` suffix to the URL:
http://localhost:8000/?edit


## Importing data

Policy and institution data can be imported via admin panel from CSV files.
This feature is located under admin panel at http://localhost:8000/admin/comparer/institution/
under following links:

* Import institutions from CSV
* Import policies from CSV
* Import logo from ZIP

Data format of the import files is undocumented yet. Please contact me if you need more details.


# Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.


# License
[MIT](https://choosealicense.com/licenses/mit/)
