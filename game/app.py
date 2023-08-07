from flask import Flask, redirect, render_template, request, url_for

from .PanGameTree import GameNotInitializedException, PGInitializer

app = Flask(__name__, template_folder="templates", static_folder="static")


@app.route("/")
def main_page():
    return render_template("main_page.html")


@app.route("/pan_rules")
def pan_rules_page():
    return render_template("pan_rules_page.html")


@app.route("/pan_game_start", methods=["POST"])
def handle_pan_game_start():
    game_value = int(request.form.get("game_value", 10))
    PGInitializer(game_value)
    return redirect(url_for("pan_game_page"))


@app.route("/main_menu", methods=["GET"])
def go_to_main_menu():
    return redirect(url_for("main_page"))


@app.route("/go_to_pan_rules", methods=["GET"])
def go_to_pan_rules():
    return redirect(url_for("main_page"))


@app.route("/PAN", methods=["GET", "POST"])
def pan_game_page():
    try:
        if request.method == "POST":
            move_id = int(request.form["move_id"])
            if move_id == -1:
                PGInitializer.reset()
                pg = PGInitializer().pan_game  # type: ignore
                deck, hand, moves, result = pg.ask_for_move()
            else:
                pg = PGInitializer().pan_game  # type: ignore
                pg.choose_move(move_id - 1)
                deck, hand, moves, result = pg.ask_for_move()
        else:
            pg = PGInitializer().pan_game  # type: ignore
            deck, hand, moves, result = pg.ask_for_move()

        if result != -1:
            moves = []
        return render_template(
            "pan_page.html",
            deck=deck,
            hand=hand,
            moves=moves,
            result=result,
        )
    except GameNotInitializedException:
        return redirect(url_for("main_page"))


if __name__ == "__main__":
    app.run(debug=True)
