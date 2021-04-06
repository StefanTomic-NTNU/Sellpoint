[![Gitpod Ready-to-Code](https://img.shields.io/badge/Gitpod-Ready--to--Code-blue?logo=gitpod)](https://gitpod.io/#https://gitlab.stud.idi.ntnu.no/tdt4140/landsby-4/gruppe-61/sellpoint)

A requirements.txt file is a file that lists all of the modules needed for the Django project to work.

The following command will install the packages according to the configuration file requirements.txt.
 ` pip install -r requirements.txt`

To update requirements:
` pip freeze > requirements.txt`

To run the project:
 ` python manage.py runserver`

To activate venv i gitpod: ` source venv/Scripts/activate`

### Kjøre tester
For å kjøre tester og generere report:
` coverage run --source='app-navn-her' manage.py test && coverage report && coverage html`
Reports blir genrert i htmlcov-mappe

#### Superuser
name: admin
password: aR5!?kuRTui

### Delete expired reklame
`python manage.py delete_expired`

