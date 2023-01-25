mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

local:
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l ru
	python3 manage.py makemessages -l uz

compile:
	python3 manage.py compilemessages

create:
	python3 manage.py createsuperuser