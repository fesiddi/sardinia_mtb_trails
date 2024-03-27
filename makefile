black:
	black ./app ./tests

isort:
	isort ./app ./tests

qa: black isort


run:
	uvicorn app.main:app --reload