
class Card:
    COLORS = ["&#9824;", "&#9829;", "&#9827;", "&#9830;"]
    VALUES = ["9", "10", "J", "Q", "K", "A"]

    def __init__(self, value: int, color: int=0) -> None:
        self.value = value
        self.color = color

    def render_json(self) -> dict:
        return {
            "value": Card.VALUES[self.value],
            "color": Card.COLORS[self.color],
        }
