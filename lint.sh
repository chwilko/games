fill() {
    local text="$1"
    local fill_char="$2"
    local columns=$(tput cols)
    local stars=$(( (columns - ${#text}) / 2  - 1))
    printf '%.s*' $(seq 1 $stars) 
    printf " "
    printf $text
    printf " "
    printf '%.s*' $(seq 1 $stars)
    printf "\n"
}

fill "BLACK" "*"
poetry run black game --exclude="tests/pan_game_testing.py"
fill "ISORT" "*"
poetry run isort game
fill "MYPY" "*"
poetry run mypy game --exclude="tests/pan_game_testing.py" 
fill "FLAKE8" "*"
poetry run flake8 game --exclude="tests/pan_game_testing.py"
