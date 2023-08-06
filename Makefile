PROJECT_NAME = game
APP_NAME = app

PROJECT_URL = http://127.0.0.1:5000/

open_page:
	xdg-open $(PROJECT_URL)

only_run:
	flask --app $(PROJECT_NAME).$(APP_NAME) run

run: open_page only_run

debug: open_page
	flask --debug --app $(PROJECT_NAME).$(APP_NAME) run 

sandbox_run:
	flask --app sandbox.app run

lint:
	bash lint.sh
