mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
	python3 manage.py ram

ram:
	python3 manage.py ram

faker:
	python3 manage.py loaddata role
	python3 manage.py create -c 2 -b 5 -course 5 -r 10 -hd 10 -u 10 -a 10 -li 10 -l 10 -gr 10

admin:
	python3 manage.py createsuperuser --noinput

remig:
	make unmig
	make mig
	make admin
	make faker

search_index:
	python3 manage.py search_index --rebuild
