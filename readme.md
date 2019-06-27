# Cinema Reservation App 

## Tech Stack
- Python 3.7
- Django Rest Framework 3.9.4
- Angular 7

## How to  run locally

- Install python 3.7

### Frontend
- Install angular dependencies
    - Follow the oficcial [Setup](https://angular.io/guide/setup-local)
- cd to clientapp folder
- run: `ng serve`
    
the app will run on localhost:4200
    
### Backend
- cd to root folder
- create python virtual environment: `python3 -m venv cinema_env`
- activate the virtual env: `source cinema_env/bin/activate`
- install libs with pip: `pip install -r server/requirements.txt`
- run the server: `python server/manage.py runserver`
    
    
### Access web
 - type localhost:4200 on your browser
