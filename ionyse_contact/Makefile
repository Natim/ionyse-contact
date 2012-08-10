#######################
# Cmd projet Django   #
#######################

# Local development management
clean:
	find -L . -name "*~" -exec rm -fr {} \;
	find -L . -name "*.pyc" -exec rm -fr {} \;
	find -L . -name ".DS_Store" -exec rm -fr {} \;
	find -L . -name "Thumbs.db" -exec rm -fr {} \;
	find -L . -name "Thumbs.db:encryptable" -exec rm -fr {} \;

runserver:
	python manage.py runserver localhost:8000

cp_settings:
	cp ./settings.py ./settings.py.example

dumpdata:
	python manage.py dumpdata --exclude=admin --exclude=contenttypes --exclude=auth --exclude=sessions --format yaml --indent=4 > ionyse_contact.yaml

syncdb:
	# Flush the database
	python manage.py flushwebsite
        # Create empty databases
	python manage.py syncdb --noinput --migrate
        # Load the fixtures
	# python manage.py createwebsite
	python manage.py loaddata ionyse_contact.yaml
	python manage.py createsuperuser

mail:
	python -m smtpd -n -c DebuggingServer localhost:1025

# Testing suite
test:
	python manage.py test

# Deployment management
collectstatic:
	python manage.py collectstatic

# Virtual Env Management
virtualenv:
	virtualenv --no-site-packages --distribute apps

upgrade: requirements.txt
	pip install -r requirements.txt

requirements:
	pip freeze > requirements.txt
