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


## Building project

* clone this repository
* run `./install.sh` script


## Configuration

Create `./main/local_settings.py` file

Edit the file and add project specific settings:

Required:

```python
...
```

Optional:

```python
...
```


## Contributing
Pull requests are welcome. For major changes, please open an issue first to
discuss what you would like to change.


## License
[MIT](https://choosealicense.com/licenses/mit/)
