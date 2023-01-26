mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

local:
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l ru
	python3 manage.py makemessages -l uz
	python3 manage.py compilemessages

user:
	python3 manage.py createsuperuser