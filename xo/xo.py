from typing import Literal, Union, Optional


class _Player:
    def __init__(self, name: str, sign: Literal['x', 'o']) -> None:
        self.name = name
        self.sign = sign


class _XOTable:
    xo_map = {k: None for k in range(1, 10)}  # {1:x, 2: None, 3: o, ...}

    def __str__(self):
        map = self.xo_map
        return """
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
|  {}  |  {}  |  {}  |
 -----------------
""".format(*[map[i] if map[i] else i for i in map])

    def mark(self, cell_no, sign: str):
        assert isinstance(cell_no, int) and 1 <= cell_no <= 9, "Enter a valid cell no [1, 9]"
        assert not self.xo_map[cell_no], "Cell is filled"
        sign = str(sign).lower()
        assert sign in 'xo', 'Invalid sign' + sign
        self.xo_map[cell_no] = sign


class _XOGame(_XOTable):
    class UnFinishedGameError(Exception):
        "winner: zamani raise mishe k, bazi tamoom nashode bahe, vali winner() ..."
        pass

    class FinishedGameError(Exception):
        "mark: dar zamin k bazi tamoom shde ..."
        pass

    class InvalidCellError(Exception):
        "mark: Che por bashe, che addesh eshtabah bashe va ..."
        pass

    class InvalidPlayer(Exception):
        "mark: palyere voroodi eshtebah bashad!!!"
        pass

    def __init__(self, player1: _Player, player2: _Player) -> None:
        self.player1, self.player2, self.table = player1, player2, _XOTable()
        self.scores, self.rounds = {self.player1: 0, self.player2: 0}, 0

    def _calculate_result(self):
        win_list = ["123", "456", "789", "147", "258", "369", "159", "357"]
        for item in win_list:
            value_list = [self.xo_map[int(index)] for index in item if self.xo_map[int(index)]]
            if "".join(value_list) == "xxx" or "".join(value_list) == "ooo":
                return True
        return False

    def mark(self, cell_no, player: Union[_Player, Literal['x', 'o'], int]):
        if 1 > cell_no > 9:
            raise self.InvalidCellError(cell_no, "cell number is invalid")
        if player == "x" or player == "o" or player == "X" or player == "O":
            player = self.player1 if self.player1.sign == player else self.player2
        elif player == 0 or player == 1:
            player = self.player1 if player == 0 else self.player2
        elif isinstance(player, _Player) is False:
            raise self.InvalidPlayer("player1", "invalid player")
        table = _XOTable()
        table.mark(cell_no, player.sign)
        print(table)

    def winner(self) -> Optional[_Player]:
        if None in self.table.xo_map.values() or self.rounds < 5:
            raise self.UnFinishedGameError("The Game has not Finished yet!...")
        if len(set(self.scores.values())) != 1:
            return self.player1 if self.scores[self.player1] > self.scores[self.player2] else self.player2

player1_name = input("Please Enter Your Name:")
player1_sign = input("Please Enter Your Sign:")
player1 = _Player(player1_name, player1_sign)
player2_name = input("Please Enter Your Name:")
player2_sign = input("Please Enter Your Sign:")
player2 = _Player(player1_name, player2_sign)

winner_dict = {player1: 0, player2: 0}
for i in range(3):
    game = _XOGame(player1, player2)
    while winner != False:
        turn = input("Please Enter A Cell Number and Your Mark:")
        num, sign = turn.split(" ")
        game.mark(num, sign)
        winner = game.winner()
    if isinstance(winner, _Player):
        winner_dict[winner] += 1

winner_dict_reverse = {v: k for k, v in winner_dict.items()}
print(f"The Winner IS: {winner_dict_reverse[sorted(winner_dict_reverse.keys())[0]]}")