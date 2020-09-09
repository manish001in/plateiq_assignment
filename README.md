Steps to use:

0. cd into the project directory.
1. Create a virtualenv in the directory.
2. Activate the virtualenv using "source venv/bin/activate" considering your virtualenv is called venv.
3. Run "pip install -r requirements.txt"
4. Create a mysql user and database and grant it the privileges for that database as specificed in the settings.py file. 
You may use your own credentials as well.
5. Run python manage.py makemigrations and python manage.py migrate to ensure database tables are created.
6. Run script setup_db.py with command "python setup_db.py"
7. Use as you may.