class PLAYERS:
    PLAYER = "PLAYER"
    COMPUTER = "COMPUTER"


class ResultsCounter:
    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ResultsCounter, cls).__new__(cls)
            cls.instance.games = {}
        return cls.instance

    def add_point(self, game: str,  who: str):
        self.games[game][who] += 1

    