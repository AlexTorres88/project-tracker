# Project tracker application

This application serves the purpose of tracking projects. It was done in fastapi using postgresql as the database. 

## Model relationship

To be able to use this app, first you need to understand the data models and their relationships, which look like this:

<img width="799" alt="Screen Shot 2022-12-16 at 1 13 08" src="https://user-images.githubusercontent.com/62902131/208034339-79cb5614-bf92-40ce-bd5b-ae93809f1050.png">

To create a project, you need a user to own it, and to create an update you need it to belong to a project. You get the gist of it. 

## Usage 

First of all, make sure that you create a .env file with the same variables located in the .example.env file in this repository and fill them out with the corresponding values, after that, you're ready to run it. 

When running the application, just adding the postgresql db string should be enough and the code should take care of creating the tables in the db. If it doesn't, you can follow the data models above or the ones defined in the models.py file to create the tables by yourself. 

You can run this application in two ways:

1. With docker
2. In your local environment

### Docker

I recommend running in with docker if you have that installed, as the only commands you need to run in the parent directory are:

    docker-compose build && docker-compose up
    
### Locally
    
If you're running it locally, you'll first want to make sure you're inside a virtual env by doing:

    python3 -m venv /path/to/new/virtual/environment
    
And then running:
    
    source path_of_venv/bin/activate
    
After this, you should run:

    pip install -r requirements.txt

Now for the last command, do:

    uvicorn app.main:app --reload
    
And you're all set, ready to use the app.

Once the app is running, you'll find it easier to use by going to the docs route where the app is running on:
* docker should be http://127.0.0:3000/docs
* local should be http://127.0.0.1:8000/docs

In here, you can easily test out the application's endpoints, just make sure you're logged in by clicking the authorize button in the upper right corner (you'll need to create a user for this)

<img width="1391" alt="Screen Shot 2022-12-16 at 1 08 38" src="https://user-images.githubusercontent.com/62902131/208033794-83148017-e444-4cb9-ac4b-cb70a125811c.png">
