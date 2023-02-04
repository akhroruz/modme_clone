mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

remig:
	make unmig
	make mig

local:
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l ru
	python3 manage.py makemessages -l uz
	python3 manage.py compilemessages

admin:
	python3 manage.py createsuperuser --phone 931001010

load:
	python3 manage.py loaddata role

create:
	python3 manage.py create -c 5 -b 8 -course 5 -r 10 -hd 10

setup:
	pip install -r requirements.txt

poetry:
	curl -sSL https://install.python-poetry.org | python3 -
