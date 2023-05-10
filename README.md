You should first create a virtual environment:

```console
$ python -m venv venv
$ sourcepath venv/Scripts/activate
```

Install the pinned dependencies from `requirements.txt`:

```console
(venv) $ python -m pip install -r requirements.txt
```

Then, navigate into the `SmartPOSApi/` folder:

```console
(venv) $ cd SmartPOSApi
(venv) $ python app.py
```

To see your home page, visit `http://127.0.0.1:8000`. 
You can find the Swagger UI API documentation on `http://127.0.0.1:8000/api/ui`.

### Optional: Build the Database

You can build a SQLite database with content by following the commands below.

Navigate into the `SmartPOSApi/` folder:

```console
(venv) $ python build_database.py
```

This will delete any existing database and create a new database named `smartpos.db` that you can use with your project.
