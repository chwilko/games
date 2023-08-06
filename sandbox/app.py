from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

# Widok głównej strony
@app.route("/")
def index():
    return render_template("index.html")

# Widok obsługujący żądanie AJAX
@app.route("/ajax_request", methods=["POST"])
def ajax_request():
    # Otrzymujemy dane z przeglądarki
    data_from_browser = request.form.get("data")
    
    # Wykonujemy jakąś logikę (w tym przykładzie, zwrócenie tych samych danych)
    processed_data = data_from_browser
    
    # Zwracamy przetworzone dane jako odpowiedź AJAX
    return jsonify({"result": processed_data})

if __name__ == "__main__":
    app.run(debug=True)
