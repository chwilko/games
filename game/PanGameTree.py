from typing import (
    Callable,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    TypeVar,
    Union,
)

import numpy as np


def default_setup_fun(x):
    x[x == 3] = 1.5
    x[x == 4] = 2.5
    return x


def default_translator(x: int) -> str:
    tran = ["9", "10", "J", "Q", "K", "A"]
    return tran[x]


T = TypeVar("T")


def identity(x):
    return x


class Stack(Generic[T]):
    def __init__(self, lt: Optional[List[T]] = None) -> None:
        if lt is None:
            self._stack: List[T] = []
        else:
            self._stack = lt

    def push(self, *args) -> None:
        self._stack.extend(args)

    def peek(self) -> T:
        return self._stack[-1]

    def peekn(self, n: int = 1) -> List[T]:
        return self._stack[-n:]

    def pop(self) -> T:
        return self._stack.pop()

    def popn(self, n: int = 1) -> List[T]:
        ret = self._stack[-n:]
        for _ in range(n):
            self._stack.pop()
        return ret

    def __len__(self) -> int:
        return len(self._stack)

    def __str__(self) -> str:
        return self._stack.__str__()

    def copy(self) -> "Stack":
        return Stack(self._stack.copy())

    def __iter__(self) -> Iterator[T]:
        for i in self._stack:
            yield i

    def __eq__(self, __o) -> bool:
        return self._stack == __o._stack


class Node:
    COST_ARRAY = None
    SETUP_FUN = default_setup_fun
    CARD_TRANSLATOR = identity

    @classmethod
    def gen_cost_array(cls, n=6, cost_fun: Optional[Callable] = None) -> None:
        if cost_fun is None:
            cost_fun = lambda x: 2 ** (n - x - 1)  # noqa
        tmp_cost_array = cost_fun(np.array([range(n)]).T)
        if not tmp_cost_array.shape == (n, 1):
            raise ValueError("cost_fun should stay cls.COST_ARRAY shape")
        cls.COST_ARRAY = tmp_cost_array

    @classmethod
    def gen_setup_fun(cls, setup_fun: Callable) -> None:
        cls.SETUP_FUN = setup_fun

    @classmethod
    def set_card_translator(cls, translator_fun: Callable) -> None:
        cls.CARD_TRANSLATOR = translator_fun

    def __init__(
        self,
        *,
        _round: int,
        params: np.ndarray,
        turn: int,
        stack: Optional[Stack[int]] = None,
    ) -> None:
        self.params = params  # np.array with (2, n) shape
        if stack is None:
            self.stack = Stack[int]()
        else:
            self.stack = stack
        self.round = _round
        self.turn = turn
        self._cost: Optional[float] = None
        self._children: List[Node] = []
        self._trace: Optional[float] = None
        self.children_count = 0

    @property
    def cost(self) -> float:
        if self._cost is not None:
            return self._cost

        cards_sum = self.params.sum(axis=1)

        if cards_sum[0] == 0:
            self._cost = np.inf
            return self._cost
        if cards_sum[1] == 0:
            self._cost = -np.inf
            return self._cost

        cost = Node.SETUP_FUN(self.params.copy()) @ Node.COST_ARRAY
        self._cost = cost[1] - cost[0]
        return self._cost

    def try_set_child(self, new_node: "Node") -> "Node":
        if new_node in self._children:
            return self._children[self._children.index(new_node)]

        self._children.append(new_node)
        self.children_count += 1
        return new_node

    def get_child(self, k: int) -> None:
        self._children[k]

    def children(self) -> Iterator["Node"]:
        for child in self._children:
            yield child

    def has_child(self):
        return len(self._children) > 0

    def is_maximizer(self) -> bool:
        return self.turn == 0

    def set_trace(self) -> float:
        if self.children_count == 0:
            self._trace = self.cost
            return self.cost

        if self.is_maximizer():
            m = max([n.set_trace() for n in self.children()])
        else:
            m = min([n.set_trace() for n in self.children()])

        self._trace = m
        return m

    def __eq__(self, __o) -> bool:
        if self.turn != __o.turn:
            return False
        if not (self.params == __o.params).all():
            return False
        if self.stack != __o.stack:
            return False
        return True

    def __str__(self) -> str:
        ret = str(self.params) + "\n" + str(self.turn) + " | " + str(self.cost) + "\n"
        return ret

    def get_stack(self) -> List[str]:
        return [f"{Node.CARD_TRANSLATOR(card)}" for card in self.stack]

    def get_hand(self, player: int) -> List[str]:
        cards = []
        for number, i in enumerate(self.params[player, :]):
            for _ in range(int(i)):
                cards.append(Node.CARD_TRANSLATOR(number))
        return cards

    def get_diff(self, player, begin) -> Dict[str, Union[str, int]]:
        table = (begin - self.params)[player, :]
        for number, i in enumerate(table):
            if i == 0:
                continue
            if i < 0:
                return {"value": "Draw", "no": -int(table.sum())}
            return {"value": Node.CARD_TRANSLATOR(number), "no": int(i)}
        raise Exception()


class PanGame:
    @classmethod
    def play(cls, depth=6):
        Node.gen_cost_array()
        Node.set_card_translator(default_translator)
        pg = cls(np.random.randint(0, 2), depth)
        if pg.user != pg.root.turn:
            pg.make_auto_move(depth)
        return pg

    def __init__(
        self,
        user,
        depth,
        initial_params=None,
        *,
        cards_number: int = 6,
        colors_number: int = 4,
    ) -> None:
        self.user = user
        self.depth = depth
        self.cards_number = cards_number
        self.colors_number = colors_number
        if initial_params is None:
            initial_params = self.get_initial_params()
        initial_params[0][0] -= 1
        initial_stack = Stack[int]()
        initial_stack.push(0)
        self.root = Node(_round=0, params=initial_params, turn=1, stack=initial_stack)

    def get_initial_params(self):
        deck = np.array(
            sum(
                [list(range(self.cards_number)) for _ in range(self.colors_number)],
                [],
            )
        )
        np.random.shuffle(deck)
        hands = np.zeros((2, self.cards_number))
        n = self.colors_number * self.cards_number
        for i, el in enumerate(deck):
            hands[2 * i // n][el] += 1
        if hands[0][0] == 0:
            tmp = hands[1, :].copy()
            hands[1, :] = hands[0, :]
            hands[0, :] = tmp
        return hands

    def _move(self, card, number, current_node) -> Node:
        new_stack = current_node.stack.copy()
        new_stack.push(*((card,) * number))

        new_node = Node(
            _round=current_node.round,
            params=current_node.params
            - self._get_mod(
                current_node.turn,
                card,
                number,
            ),
            turn=1 - current_node.turn,
            stack=new_stack,
        )
        return current_node.try_set_child(new_node)

    def moves(self, current_node: Node):
        up_card = current_node.stack.peek()
        for i in range(up_card, self.cards_number):
            if current_node.params[current_node.turn][i] == 4:
                new_node = self._move(i, 4, current_node)
                yield new_node

            if current_node.params[current_node.turn][i] >= 3:
                new_node = self._move(i, 3, current_node)
                yield new_node

            if current_node.params[current_node.turn][i] >= 1:
                new_node = self._move(i, 1, current_node)
                yield new_node
        n = len(current_node.stack) - 1
        if n <= 0:
            return
        n = min(n, 3)
        new_stack = current_node.stack.copy()
        cards = new_stack.popn(n)
        new_node = Node(
            _round=current_node.round,
            params=current_node.params
            + sum([self._get_mod(current_node.turn, k, 1) for k in cards]),
            turn=1 - current_node.turn,
            stack=new_stack,
        )
        new_node = current_node.try_set_child(new_node)
        yield new_node

    def _get_mod(self, player, card, current_cards_number):
        ret = np.zeros((2, self.cards_number))
        ret[player][card] = current_cards_number
        return ret

    def choose_move(self, n: int):
        self.root = list(self.moves(self.root))[n]
        self.make_auto_move(self.depth)

    def make_auto_move(self, depth: int):
        best = self.min_max(depth=depth)
        for child in self.root.children():
            if child._trace == best:
                self.root = child
                return
        print("Woops")

    def ask_for_move(self):
        return (
            self.root.get_stack(),
            self.root.get_hand(self.user),
            [
                move.get_diff(self.user, self.root.params)
                for move in self.moves(self.root)
            ],
            self.check(),
        )

    def check(self):
        ret = self.root.params.sum(axis=1)
        if ret[0] == 0:
            return int(0 == self.user)
        if ret[1] == 0:
            return int(1 == self.user)
        return -1

    def min_max(self, node: Optional[Node] = None, depth: int = 4):
        if node is None:
            node = self.root
        self._min_max(
            node,
            depth,
            -np.inf,
            np.inf,
        )
        node.set_trace()
        return node._trace

    def _min_max(
        self,
        node: Node,
        depth: int,
        alpha: float,
        beta: float,
    ):
        if depth == 0 or node.cost in (-np.inf, np.inf):
            return node.cost
        if node.is_maximizer():
            current_max = -np.inf
            for child_node in self.moves(node):
                next_value = self._min_max(
                    child_node,
                    depth - 1,
                    alpha,
                    beta,
                )
                current_max = max(current_max, next_value)

                alpha = max(alpha, next_value)
                if beta <= alpha:
                    break
            return current_max
        else:
            current_min = np.inf
            for child_node in self.moves(node):
                next_value = self._min_max(
                    child_node,
                    depth - 1,
                    alpha,
                    beta,
                )
                current_min = min(current_min, next_value)
                beta = min(beta, next_value)
                if beta <= alpha:
                    break
            return current_min


class PGInitializer:
    instance = None
    _depth = None

    def __new__(cls, depth: Optional[int] = None):
        if cls.instance is None:  # or hasattr(cls.instance, "pan_game"):
            depth = depth or cls._depth
            if depth is None:
                raise Exception()
            cls.instance = super().__new__(cls)
            cls.instance.__init__(depth)
            cls._depth = depth
        return cls.instance

    def __init__(self, depth) -> None:
        self.pan_game = PanGame.play(depth)

    @classmethod
    def reset(cls):
        cls.instance = None


if __name__ == "__main__":
    PanGame.play(10)
