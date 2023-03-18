# Sellpoint

This is the final delivery for group 61 in TDT4140 - Software Development at NTNU, spring 2021. It is an online marketplace built using Django. One may register a user and then publish items on the website. Items are searchable, orderable, filterable and paginated. After looking at the details of an item, it is possible to contact the user who posted it. 

<img width="578" alt="bilde" src="https://user-images.githubusercontent.com/56115181/226106317-b698f141-2a87-4c90-a77f-d8fc749b03df.PNG">

[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://gitlab.stud.idi.ntnu.no/tdt4140/landsby-4/gruppe-61/sellpoint)

## Running the website

A requirements.txt file is a file that lists all of the modules needed for the Django project to work.

The following command will install the packages according to the configuration file requirements.txt.
 ` pip install -r requirements.txt`

To update requirements:
` pip freeze > requirements.txt`

To run the project:
 ` python manage.py runserver`

To activate venv i gitpod: ` source venv/Scripts/activate`

## Running Tests
To run tests and generate reports:
` coverage run --source='app-name-here' manage.py test && coverage report && coverage html`
Reports are generated in the htmlcov directory

#### Superuser
name: admin
password: aR5!?kuRTui

### Delete expired reklame
`python manage.py delete_expired`

