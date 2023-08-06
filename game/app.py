# app.py
from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
from .card import Card  # Assuming card.py contains the Card class

app = Flask(__name__, template_folder="templates", static_folder="static")

def deck_gen(interval=(1, 5)):
    deck = []
    for _ in range(random.randint(*interval)):
        deck.append(
            Card(random.randint(0, 5), random.randint(0, 3)).render_json()
        )
    return deck

def gen_moves(move_id=0):
    moves = []
    
    for _ in range(random.randint(1+move_id, 2+move_id)):
        moves.append(
            {
                "no": random.randint(1, 4),
                "card": Card(random.randint(0, 5), random.randint(0, 3)).render_json(),
            }
        )
    if random.random() < 0.9:
        moves[-1]["no"] = 3
        moves[-1]["card"]["value"] = "draw"
    return moves

@app.route("/")
def main_page():
    return render_template("main_page.html")

@app.route("/button_click", methods=["POST"])
def handle_button_click():
    return redirect(url_for("pan_game_page"))

@app.route("/PAN", methods=["GET", "POST"])
def pan_game_page():
    if request.method == "POST":
        move_id = int(request.form["move_id"])
        moves = gen_moves(move_id)
    else:
        moves = gen_moves()

    deck = deck_gen()
    hand = deck_gen()
    return render_template("pan_page.html", deck=deck, hand=hand, moves=moves)

if __name__ == "__main__":
    app.run(debug=True)
