# Vending Machine System

This System mimics the functionality of a vending machine.
It allows users to purchase a single product at a time. 
The User can put in a coins of various denominations to purchase a product. 
The vending machine then deducts the cost of the product from the coins inserted by the user and return the change if any.

The system is built using Django framework.

## How to Set up the Database
The preferred database for this project is PostgreSQL database.
Install Postgres from their official website [Here](https://www.postgresql.org/download/)

Follow the recommended steps to configure the PostgreSQL database.

Create a database with the name ``vending_machine``

## How to Set up the project
Once you have the project locally either by cloning it from the GitHub repository or by obtaining a zip file.

Create a virtual environment in the main directory of the project.

``python3 -m venv venv``

Activate the virtual environment using the following command

For MacOS/ LInux
``source venv/bin/activate``

For Windows
``venv\Scripts\activate``

Once the virtual environment is activated, install the project dependencies using the following command

``pip install -r requirements.txt``

Create a ``.env`` file inside the ``VendingMachine`` app and add configurations for your database.

```
DB_NAME=vending_machine
DB_HOST=localhost
DB_USER=[your_postgres_user]
DB_PASSWORD=[your_postgres_password]
```
CD to the main directory of  your project and run the following command to migrate the database table.

`` python manage.py migrate``

After all migrations have run successfully. Create a superuser to act as the administrator of the entire system using the following command.

``python manage.py createsuperuser``

Follow the steps to create a superuser.

## How to Run the Project

Navigate to the same directory as the ``manage.py`` file.
Run the following command to run the project.

``python manage.py runserver``

Congratulations. You have successfully run the Vending Machine project.

## How to Test

To test the application navigate to the docs folder. There you will find a JSON file with sample requests that can be used to test the application.

You can import the JSON file into postman to create a new collection.

