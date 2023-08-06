from flask import Flask, render_template, jsonify, request, redirect, url_for
import random
from .card import Card

app = Flask(__name__)

def deck_gen(interval = (1, 5)):
    deck = []
    for _ in range(random.randint(*interval)):
        deck.append(
            Card(random.randint(0,5), random.randint(0,3)).render_json()
        )
    return deck

def gen_moves():
    moves = []
    for _ in range(random.randint(1, 5)):
        moves.append(
            {
                "no": random.randint(1, 4),
                "card": Card(random.randint(0,5), random.randint(0,3)).render_json(),
            }
        )
    if random.random() < 0.9:
        moves[-1]["no"] = 3
        moves[-1]["card"]["value"]= "draw"
    return moves


@app.route("/")
def main_page():
    return render_template(
        ["game", "templates", "main_page.html"]
    )


@app.route("/button_click", methods=["POST"])
def handle_button_click():
    return redirect(url_for("pan_game_page"))


@app.route('/PAN')
def pan_game_page():
    deck = deck_gen()
    hand = deck_gen()
    moves = gen_moves()
    return render_template(
        ["game", "templates", "pan_page.html"],
        deck=deck,
        hand=hand,
        ms=moves,
    )


@app.route('/new_buttons', methods=['POST'])
def new_buttons():
    data = request.get_json()
    count = data['count']
    buttons_html = ''
    for num in range(count):
        buttons_html += f'<button class="number-button" data-count="{num + 1}">{num + 1}</button>'
    return jsonify({'buttons_html': buttons_html})
