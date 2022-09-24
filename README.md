# Repository for Data Collection form

<!-- W10 messing up ps schema - Heroku Demo here: https://dcniser.herokuapp.com/collect/ -->
**NOTE**: The intended platform for this site is touchscreen tablets, in particular Safari on iPad with the stylus (Pencil). Also, the AJAX-validation code can be found in the `ajax-validate` branch.

## Dependencies:
* Python Packages:
  * `dj-database-url==0.5.0`
  * `Django==3.2.8`
  * `gunicorn==20.1.0`
  * `numpy==1.21.2`
  * `opencv-python==4.5.3.56`
  * `Pillow==8.3.2`
  * `psycopg2==2.9.1`
  * `psycopg2-binary==2.9.1`
  * `whitenoise==5.3.0`

* System Dependencies:
  * `postgresql` (Developed with `postgreSQL 12`)
  * `postgresql-doc-12` or `libpq-dev`


## How to install & run the webapp?
* Get the code.
  1. `git clone https://github.com/sdgniser/data_collection.git`
  2. `cd data_collection`
* Install postgres.
  1. `sudo apt install postgresql-12`
  2. `sudo apt install postgresql-doc-12` (Necessary for `psycopg2`). If `psycopg2` still gives trouble, try `sudo apt install libpq-dev`.
  3. `sudo service postgresql restart`
  * For windows, follow the instructions at https://www.postgresql.org/download/.
* Create database. Replace `<*>` with actual names. And don't forget the `;` for SQL commands.
  1. `sudo -u postgres psql`
  2. `CREATE DATABASE <DB_NAME>;`
  3. `CREATE USER <DB_USER> WITH PASSWORD '<DB_PWD>';`
  4. `GRANT ALL PRIVILEGES ON DATABASE <DB_NAME> TO <DB_USER>;`
  5. `\q`
  * For Windows, the easiest way is to use the `pgAdmin` web interface. Look it up in Start Menu. Make sure to remember the database name, database owner/user name and the password, you supplied, while creating the database.
* Create virtual environment & install Python dependencies.
  1. `python -m venv data_venv`
  2. `source data_venv/bin/activate`
  3. `pip install -r requirements.txt`
* Edit `./data_collection/settings.py`:
  * Fill the DB name, DB user name and DB password, in the `DATABASES` setting. Alternatively, set them as environment variables - `DB_NAME`, `DB_USER` and `DB_PWD`.
  * Leave `Debug = True`, while testing the app.
* Migrate & serve the webapp.
  1. `python manage.py makemigrations`
  2. `python manage.py migrate`
  3. `python manage.py createsuperuser`. Supply desired username, mail and password.
  4. `python manage.py collectstatic`
  5. `sudo ufw allow 3456`
  6. `python manage.py runserver localhost:3456`
  7. Open a browser window and browse to [localhost:3456/collect].
* Notes:
  * In case there are database errors, it is possible, the migration has failed. Try these commands:
    1. `python manage.py makemigrations collect`
    2. `python manage.py makemigrations`
    3. `python manage.py migrate collect` 
    4. `python manage.py migrate`
  * To deploy the webapp using gunicorn and nginx, follow the instructions given [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-django-with-postgres-nginx-and-gunicorn-on-ubuntu-16-04). You will have to edit some fields in `./gunicorn/gunicorn.conf.py` and set up `nginx`.


## How does this work?

The webapp stores user-supplied data, that includes an application number, name, blood-group, photo and signature (using the Signature Pad). Multiple submissions can be made against the same application number, for example, to upload a better photo or sign, as the older names are overwritten and older images are automatically deleted from the system.

### In case you encounter any problems, please open an issue at https://github.com/sdgniser/data_collection/issues/new.
