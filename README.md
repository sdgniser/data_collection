# Repository for Data Collection form

Heroku App here: https://dcniser.herokuapp.com/collect/

## Usage:

### Dependencies:
(Check `requirements.txt` for exact versions)

Python Packages:
* `django`
* `psycopg2`
* `Pillow`
* `dj-database-url`
* `gunicorn`
* `whitenoise`

System Dependencies:
* `postgresql` (Tested with `postgresql 12`)

### Setup:

* Create a working folder/directory somewhere and a python virtual enviroment in it. Activate the virtual environment.
* Install the dependencies, via `pip -r requirements.txt`. Install `postgresql` separately.
* Create a database in postgres. Easiest way is to use `pgAdmin` web interface. Make sure to remember the database name, database owner name and the password, you supplied, while setting up postgres.
* `git clone` this repo to the working directory.
* Modify `local_settings_example.py` in `data_collection` with your data and rename the file to `local_settings.py`. Leave `Debug = True`, while testing the app.
* Supply a default_image.jpg in
* `cd` to working directory and run `python manage.py makemigrations` and `python manage.py migrate`.
* Start the server using `python manage.py runserver localhost:8787`. (You can change the port, but change it everywhere ⬇)
* Browse to `localhost:8787` in your browser.
* To open the admin panel, browse to `localhost:8787/admin`

## ToDo:

| ToDo | Status | Notes |
|:---|---:|---|
| Make names uppercase | ✅ | |
| Add garbage collection for orphan images | ✅ | |
| Rename files, during upload - `<app_no>-photo` & `<app_no>-sign` | ✅ | |
| Integrate [signature_pad](https://github.com/szimek/signature_pad) | ✅ | Can use `npm` for this + [Resource](https://stackoverflow.com/questions/34447308/how-to-save-jpeg-binary-data-to-django-imagefield) |
| Setup a Heroku App | ✅ | [Visit here](https://dcniser.herokuapp.com/collect/) |
| Make signing on iPad smoother | ⚙ | |
| Utility to add applications numbers to database | ⚙ | |
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
| `get_` fields have to be set to `read_only` for images to display | ❌ |
| Clicking on Clear POSTs form | ✅ | Fixed with `type="button"` in `<canvas>`
| "The 'sign' attribute has no file associated with it." | ✅ | Have to `save()` directly to `sign` ImageField
| When submitting form, with signature_pad empty => `Form invalid!<ul class="errorlist"><li>raw_sign<ul class="errorlist"><li>This field is required.</li></ul></li></ul>` | ✅ | Used custom validation, if `signature_pad.isEmpty()` |
| When another submission is made for the same `app_no`, the image file for `sign` has gibberish in its name. **Happens alternately**. | ⚙ | |
