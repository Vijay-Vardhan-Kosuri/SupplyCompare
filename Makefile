.PHONY: all build start run test lint clean

all: build

build:
	cd frontend && npm install && npm run build
	cd backend && pip install -r requirements.txt

start:
	python main.py runserver

run: start

test:
	cd backend && python manage.py test tests

lint:
	python -m py_compile main.py app.py

clean:
	rm -rf frontend/dist
