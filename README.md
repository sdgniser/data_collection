# Repository for Data Collection form

Heroku App here: https://dcniser.herokuapp.com/collect/

## Dependencies:
(Check `requirements.txt` for exact versions)

* Python Packages:
  * `django`
  * `psycopg2`
  * `Pillow`
  * `dj-database-url`
  * `gunicorn`
  * `whitenoise`

* System Dependencies:
  * `postgresql` (Developed with `postgresql 12`)


## How to install the app?

### Setup:
1. Create a folder/directory to store the repo and `cd` to it.
2. Create and activate a python virtual enviroment.
3. Open a terminal windows and run `git clone https://github.com/sdgniser/data_collection.git` in this folder.
4. `cd` to the **working directory** (`data_collection` folder, that is at the same level as `manage.py`).
5. [Install `postgresql`](https://www.postgresql.org/download/).
6. Install the python dependencies, via `pip -r ./requirements.txt`.
7. Create a database in postgres. Easiest way is to use `pgAdmin` web interface. Make sure to remember the database name, database owner/user name and the password, you supplied, while setting up postgres.
8. Edit `./data_collection/settings.py`:
   * Fill the DB name, DB user name and DB password, in the `DATABASES` setting. Alternatively, set them as environment variables - `DB_NAME`, `DB_USER` and `DB_PWD`.
   * Leave `Debug = True`, while testing the app.

9.  Run `python manage.py makemigrations` and `python manage.py migrate` in the terminal.
10. Start the server using `python manage.py runserver localhost:8787`. (You can change the port, but change it everywhere ⬇)
11. Browse to [localhost:8787](localhost:8787) in your browser.
12. [Create an admin/superuser](https://docs.djangoproject.com/en/3.0/intro/tutorial02/#creating-an-admin-user)
13. To open the admin site, browse to [localhost:8787/admin](localhost:8787/admin).

### Loading data (Application Numbers) into the Database:

You can use the `admin` site to add applicants, but it's a tedious process to add them one-by-one. Follow these steps to add a bunch of them at once:

1. `cd` to **working directory**.
2. Edit `./collect/fixtures/App_No.csv` with new Application Numbers (column-wise, below "pk") and save it.
3. Run `python data_import.py` in the terminal. This will create a `App_No.json` file in `./collect/fixtures/`.
4. Run `python manage.py loaddata App_No.json --app collect` in the terminal. You should get a `Installed {N} object(s) from 1 fixture(s)` message, where `{N}` denotes the number of application numbers in `App_No.csv`. This means, the data has been loaded into the database. If any errors are encountered at this step, check [below](#how-does-this-work).
Now, that the data has been loaded, browse to [localhost:8787](localhost:8787) and use the app. Read below for usage instructions.


## How does this work?

The application numbers are preloaded into the database, using `data_loader.py`. The webapp sets "default-name" as the applicant name and `default.png` as photo and signature for all application numbers. The user has to supply an application number, name, photo and signature, from the Signature Pad. The app verifies, if the application number exists in the database and then modifies the name, photo and signature against it, in the database. Multiple submissions can be made against the same application number, for example, to upload a better photo or sign, as the older names are overwritten and older images are automatically deleted from the system.


## Notes:

### On Design:
* Only the Application Numbers need to be preloaded into the database, using `data_loader.py` utility or `/admin` site.
* All fields are required in the form.
* The max length of the application number is currently set to 10, while Applicant Name length is capped at 100 characters.
* The photograph is supposed to be taken through the device camera, on the spot.
* The admin panel shows the application numbers, names, photos and signs for all applicants.
* Photo and Sign are set to `read_only` in the admin panel. As such, only application numbers and names can be modified from there. The data collection process will have to be redone for changing Photo and Sign. This is not a framework restriction. It's been designed this way.

### On Loading Data (Application Numbers):
* `pk` (Primary Key) denotes the application number, in `App_No.csv` and `App_No.json`.
* Loading same data multiple times will only refresh the data, without errors or warnings.
* If there are any errors, open `\collect\fixtures\App_No.json` and ensure, that the encoding is `UTF-8`. Any good text editor allows for changing file encoding easily.
* To view all the application numbers, in the database, in a serializable format (here, JSON), run `python manage.py dumpdata collect.applicant >> App_No_Dump.json --indent 4`. This will dump all `Applicant` data into a `App_No_Dump.json` file in the **working directory**. Note that, the encoding may not be `UTF-8`. So, if you want to make manual modifications to this file and then use `loaddata` with this file, make sure to save the file in `UTF-8` encoding.


## ToDo:

| ToDo | Status | Notes |
|:---|---:|---|
| Make names uppercase | ✅ | |
| Add garbage collection for orphan images | ✅ | |
| Rename files, during upload - `<app_no>-photo` & `<app_no>-sign` | ✅ | |
| Integrate [signature_pad](https://github.com/szimek/signature_pad) | ✅ | Replaced with Bezier Interpolated Sign Pad: [Resource](https://github.com/thread-pond/signature-pad) |
| Setup a Heroku App | ✅ | [Visit here](https://dcniser.herokuapp.com/collect/) |
| Make signing on iPad smoother | ✅ | Checkout `smoother` branch |
| Utility to add applications numbers to database | ✅ | |
| `pip freeze` | ✅ | Check again at the end |
| Write `unittests` | 👀 | At the end |

## Status (Not substitute for `unittests`)

| Functionality | Status |
|:---|---:|
| Form upload | ✅ |
| Media in `/admin` | ✅ |
| Garbage Collection | ✅ |
| Heroku app up | ✅ |

## Feature Requests:

| Feature Requests | Status | Notes |
|:---|---:|---|
| Applicant DetailView should show Applicant `photo` & `sign` in `/admin` | ✅ | Can get cluttered/make admin site slow |
| Make the interface look better | ✅❔ | |

## Issues

| Issues | Status | Notes |
|:---|---:|----|
| Required fields in form | ✅ |
| `app_no` exists error | ✅ |
| No images displayed in `/admin` | ✅ |
| `get_` fields have to be set to `read_only` for images to display | ❌ | Roundabout fix |
| Clicking on Clear POSTs form | ✅ | Fixed with `type="button"` in `<canvas>`
| "The 'sign' attribute has no file associated with it." | ✅ | Have to `save()` directly to `sign` ImageField
| When submitting form, with Signature Pad empty => `Form invalid!<ul class="errorlist"><li>raw_sign<ul class="errorlist"><li>This field is required.</li></ul></li></ul>` | ✅ | Used custom validation, if Signature Pad is empty |
| Bounce + Zoom effects cause issues with Safari on iPad (Pro) | ✅ | Set `position: fixed` on `.card-body` |
| When another submission is made for the same `app_no`, the image file for `sign` has gibberish in its name. | ⚙ | **Happens alternately**, Opened an [Issue](https://github.com/sdgniser/data_collection/issues/1). |
