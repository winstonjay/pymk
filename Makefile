

serve:
	flask run

set_app:
	export FLASK_APP=pymk; export FLASK_ENV=development

makeenv:
	virtualenv --python=python3.6 env

requirements:
	pip install -r requirements