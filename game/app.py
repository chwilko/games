from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Sample data for deck, hand, and moves
deck = [{"value": "Card 1"}, {"value": "Card 2"}, {"value": "Card 3"}]
hand = [{"value": "Card 4"}, {"value": "Card 5"}]
moves = [
    {
        "no": 3,
        "card": {"value": "Move Card 1"},
    },
    {
        "no": 2,
        "card": {"value": "Move Card 2"},
    },
]

@app.route('/')
def index():
    return render_template('index.html')

# Route to handle Ajax request and provide "deck", "hand", and "moves"
@app.route('/get_content', methods=['GET'])
def get_content():
    return jsonify({"deck": render_template('cards.html', cards=deck),
                    "hand": render_template('cards.html', cards=hand),
                    "moves": render_template('moves.html', moves=moves)})


if __name__ == '__main__':
    app.run(debug=True)
