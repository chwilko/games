# PAN game
This project is PAN game implementation.
The logic of the game is based on the alpha-beta algorithm.
Flask is responsible for the GUI.

## autors
Bartłomiej Chwiłkowski (github: chwilko)

## license
MIT license


# Usage

## Online
If it is still available, it is at the link:
[chwilko.pythonanywhere](http://chwilko.pythonanywhere.com/)

## Local
### Create env
Create virtual enviroment 
using venv
```bash
python3 -m venv games_env
source games_env/bin/activate
python3 -m pip install -r requirements.txt 
```

or using poetry 
```bash
poetry shell
poetry install
```
### Run
Run app and open browser window using make 
```bash
make run
```

or only run 
```bash
make only_run
```
and open in browser manually
[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

# Structure

game:
- static:
  - card.css -- File css with card style and card container
- templates:
    - main_page.html
    - pan_page.html
    - pan_rules_page.html
- app.py -- Flask app with all backend endpoints
- PanGameTree.py -- Implementation of the algorithm into the bot.
