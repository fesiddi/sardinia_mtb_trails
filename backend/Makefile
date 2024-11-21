black:
	black ./app

isort:
	isort ./app

qa: black isort

install:
	pip install -r requirements.txt

test:
	pytest -v

run:
	uvicorn app.main:app --reload