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
  * python3
  * python3-pip
  * python3-virtualenv
  * node
  * npm


## Configuration

* Create directory for your project.

* Clone this repository as `institution-comparer` subdirectory of your project's directory.

* Create `institution-comparer/main/local_settings.py` file and edit
  the file to add project specific settings:

Required:

```python
import os
from pathlib import Path

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

Optional:

```python
...
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

The website should now be available under address: http://localhost:8000


# Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.


# License
[MIT](https://choosealicense.com/licenses/mit/)
