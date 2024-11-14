black:
	black ./app ./tests

isort:
	isort ./app ./tests

qa: black isort

install:
	pip install -r requirements.txt

test:
	pytest -v

run:
	uvicorn app.main:app --reload