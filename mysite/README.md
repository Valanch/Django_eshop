# Django Diploma DPO

## Basic installation walkthrough

- Clone the repository
```sh
$ git clone <this project>
```

- Create a virtual environment

- Install dependencies (To install frontend please refer to README.md in the `diploma-frontend` directory)
```sh
$ pip install -r requirements.txt
```
- Once the dependencies are installed - make the necessary migrations from the "mysite" folder
```sh
$ cd mysite
$ python manage.py migrate
```
- Next, create a superuser
```sh
$ python manage.py createsuperuser
```
- Start the server
```sh
$ python manage.py runserver
```
- And navigate to `http://127.0.0.1:8000/`
- Tools to populate the website with everything it needs can be found at `http://127.0.0.1:8000/admin`

## Quick rundown of apps in the project
### diploma-frontend app
Frontend for the website, installation guide is in its own README.md

### accounts app
Profile model. Can be used to further fine-tune user access to the website.

### api app
Collection of functions used by the frontend.

### shopapp app
Models for all the objects related to the marketplace

