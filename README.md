# Item Catalogue Application

An application that provides a list of items within a variety of categories as well as provides a user registration and authentication system. Registered users will have the ability to post, edit and delete their own items.

**Note:** This is a solution to project 4 of the [Udacity Full-Stack Web Developer Nanodegree Program][1] based on the courses [Full Stack Foundations (ud088)][2], [Authentication and Authorization (ud330)][3] and [Designing RESTful APIs (ud388)][4].

Installing Development Pre-Requisites
-------------------------------------

+ Install [Python 3.5+][5]
+ Install [python-dotenv 0.6+][6]
+ Install [SQLAlchemy 1.1.13+][7]
+ Install [Flask 0.12+][8]
+ Install [oauth2client 4.1.0+][9]
+ Install any **one** of the following database & their respective database drivers
    * Install [PostgreSQL 9.2+][10] & [psycopg2][11]
    * Install [Mysql][12] & [MySQL-python][13]
    * Install [Sqlite][14]

Installing The Project for Development / Testing on Linux
---------------------------------------------------------

+ Clone the repository:

    ```shell
    $ git clone git@github.com:rishi-ramawat/FSND_P4-Item_Catalog_Application.git
    $ cd FSND_P4-Item_Catalog_Application
    ```

+ Initialize the project:

    ```shell
    $ bin/init_project
    ```

    * This shell script will create an `.env` file for you.
    * It will also install/upgrade all the required python packages for running this app.
    * **Note**: You might have to run this command with `sudo` as it tries to upgrade python packages.

+ Review `.env` and configure any required variables.
    * Make sure you have correct database credentials in the `.env` file before trying to run the project.

Installing The Project for Development / Testing on Windows
-----------------------------------------------------------

+ Clone the repo
+ Visit the folder where you have cloned the repo
    * Make a copy `.env.example` and name it as `.env`
    * Make sure all the required variables are present & initialized in `.env`
+ Make sure you have all the development pre-requisite packages installed.
    * You can run `pip3 install -U -r requirements.txt` to install/upgrade them automatically.

Setting Up The `.env` File
--------------------------

+ Setting up the database credentials:
    * If you are using [PostgreSQL][10] do the following:
        - Make sure the `DB_CONNECTION` variable is set to `pgsql` in the `.env` file.
        - Make sure the `DB_PORT` variable is set to `5432` or on whichever port [PostgreSQL][10] is running on your system.
        - Make sure all the other database credentials are initialized with proper values.
    * If you are using [Mysql][12] do the following:
        - Make sure the `DB_CONNECTION` variable is set to `mysql` in the `.env` file.
        - Make sure the `DB_PORT` variable is set to `3306` or on whichever port [Mysql][12] is running on your system.
        - Make sure all the other database credentials are initialized with proper values.
    * If you are using [Sqlite][14] do the following:
        - Make sure the `DB_CONNECTION` variable is set to `sqlite` in the `.env` file.
        - `DB_USERNAME`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT` variables can be ignored in this case.
    * Make sure `DB_DATABASE` variable is not empty and is set to `item_catalogue`.
+ Setup Google OAuth
    * Get OAuth Credentials
        + Go to https://console.developers.google.com/apis/credentials
        + Click `Create a Project`
        + Click `Credentials` > `Oauth Consent Screen`
        + Save after entering the following:
            - Product Name: `Item Catalogue`
            - Homepage URL: `http://localhost:8000`
        + Click `Create Credentials` > `OAuth Client ID`
        + Enter the following after selecting `Web Application`:
            - Name: `Item Catalogue`
            - Authorized Javascript Origins: `http://localhost:8000`
            - Authorized Redirect URIs: `http://localhost:8000`
        + Click `Create` when done
        + Click `Item Catalogue`
        + Obtain the `Client ID` & `Client secret`
    * Set the Google Oauth Credentials in the `.env` file
        * Initialize the variable `GOOGLE_CLIENT_ID` in the `.env` file with the `Client ID` obtained from in the prevoius step.
        * Initialize the variable `GOOGLE_CLIENT_SECRET` in the `.env` file with the `Client secret` obtained from in the prevoius step.
+ Setup Facebook OAuth
    1. Obtain Facebook OAuth Credentials
        + Go to https://developers.facebook.com/apps
        + Click `+ Add New App`
        + Fill in the form, and click `Create App ID` when done
        + Click `Dashboard` under the main menu
        + Obtain the `App ID`, `App secret` & `API Version` of your app.
    2. Set the Google Oauth Credentials in the `.env` file
        * Initialize the variable `FB_APP_ID` in the `.env` file with the `App ID` obtained from in the prevoius step.
        * Initialize the variable `FB_APP_SECRET` in the `.env` file with the `App secret` obtained from in the prevoius step.
        * Initialize the variable `FB_VERSION` in the `.env` file with the `API Version` obtained from in the prevoius step.
+ Setup `APP_SECRET_KEY` variable in the `.env` with a random string (atleast 9 characters long).
    * `APP_SECRET_KEY` is used by [Flask][8] for cryptographically signing session data.
    * You can use [RANDOM.ORG - Password Generator][15] to generate random strings.
+ Setup User data to be used in DB Seeds
    * Initialize the variable `USER_NAME_FOR_DB_SEEDS` with your name in the `.env` file.
    * Initialize the variable `USER_EMAIL_FOR_DB_SEEDS` with your email used in [Gmail][16] / [Facebook][17]  in the `.env` file.
        - This email will help you login and directly test all the BackOffice functionality that has been implemented in the application.

Setting Up The Database
-----------------------

+ In [PostgreSQL][10] or [Mysql][12] create the `item_catalogue` database.
    * `createdb item_catalogue` command can be used to create the database if [PostgreSQL][10] is installed natively on your system.
    * If you are using [Sqlite][14] you can skip this step.
+ Next, run `python3 app/models.py` to create all the tables in the database.
+ Next, run `python3 app/seeds.py` to add some seed data into the database.

Running the project
-------------------

+ Run the following command to start the web server and serve the application:

    ```shell
    $ python3 app/project.py
    ```

+ Next, visit `http://localhost:8000` in your web browser to view & use the application.

**Note:** Press `Ctrl` + `C` in the terminal if you want to close the local server.

Accessing Web API
-----------------

1. Enter http://localhost:8000/catalogue.json to view all categories & menu items..
2. Enter `http://localhost:8000/catalog.json/<category_slug>` to view all items in the selected category.
    + Example: http://localhost:8000/catalogue.json/cricket
3. Enter `http://localhost:8000/catalog.json/<category_slug>/<menu_item_slug>` to view the selected item.
    + Example: http://localhost:8000/catalogue.json/cricket/cricket_ball

**Note:** `category_slug` & `menu_item_slug` can be found from the [`app/seeds.py`][18] file.

[1]: https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd004 "Udacity Nanodegree: Full Stack Web Developer"
[2]: https://classroom.udacity.com/courses/ud088 "Full Stack Foundations - Udacity"
[3]: https://classroom.udacity.com/courses/ud330 "Authentication and Authorization - Udacity"
[4]: https://classroom.udacity.com/courses/ud388 "Designing RESTful APIs - Udacity"
[5]: https://www.python.org/downloads/ "Download Python"
[6]: https://pypi.python.org/pypi/python-dotenv "python-dotenv"
[7]: https://www.sqlalchemy.org/download.html "Download - SQLAlchemy"
[8]: http://flask.pocoo.org/ "Flask (A Python Microframework)"
[9]: https://pypi.python.org/pypi/oauth2client "oauth2client 4.1.2"
[10]: https://www.postgresql.org/download/ "PostgreSQL: Downloads"
[11]: http://initd.org/psycopg/docs/install.html "Psycopg Documentation"
[12]: https://dev.mysql.com/doc/refman/5.7/en/installing.html "MySQL 5.7 Installing and Upgrading MySQL"
[13]: https://pypi.python.org/pypi/MySQL-python "MySQL-python"
[14]: https://sqlite.org/download.html "SQLite Download Page"
[15]: https://www.random.org/passwords "RANDOM.ORG - Password Generator"
[16]: https://www.google.com/gmail/about/ "Gmail - Free Storage and Email from Google"
[17]: https://www.facebook.com "Facebook"
[18]: https://github.com/rishi-ramawat/FSND_P4-Item_Catalog_Application/blob/master/app/seeds.py "Database Seeds File"
