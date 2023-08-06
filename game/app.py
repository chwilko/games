# app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
from .card import Card
from .PanGameTree import PGInitializer

app = Flask(__name__, template_folder="templates", static_folder="static")

def deck_gen(interval=(1, 5)):
    deck = []
    for _ in range(random.randint(*interval)):
        deck.append(
            Card(random.randint(0, 5), random.randint(0, 3)).render_json()["value"]
        )
    return deck

def gen_moves(move_id=0):
    moves = []
    
    for _ in range(random.randint(1+move_id, 2+move_id)):
        moves.append(
            {
                "no": random.randint(1, 4),
                "value": Card(random.randint(0, 5), random.randint(0, 3)).render_json()["value"],
            }
        )
    if random.random() < 0.9:
        moves[-1]["no"] = 3
        moves[-1]["value"] = "draw"
    return moves

@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/pan_game_start", methods=["POST"])
def handle_pan_game_start():
    game_value = int(request.form.get("game_value", 10))
    PGInitializer(game_value)
    return redirect(url_for("pan_game_page"))

@app.route("/main_menu", methods=["POST"])
def go_to_main_menu():
    return redirect(url_for("main_page"))


@app.route("/PAN", methods=["GET", "POST"])
def pan_game_page():
    try:
        if request.method == "POST":
            move_id = int(request.form["move_id"])
            if move_id == -1:
                PGInitializer.reset()
                pg = PGInitializer()
                deck, hand, moves, result = pg.ask_for_move()
            else:
                pg = PGInitializer()
                pg.choose_move(move_id-1)
                deck, hand, moves, result = pg.ask_for_move()
        else:
            pg = PGInitializer()
            deck, hand, moves, result = pg.ask_for_move()

        if result != -1:
            moves = []
        return render_template(
            "pan_page.html", deck=deck, hand=hand, moves=moves, result=result,
        )
    except Exception as e:
        return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run(debug=True)
