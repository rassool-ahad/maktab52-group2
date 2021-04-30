from typing import Literal, Union, Optional, List


class _Player:
    def __init__(self, name: str, sign: Literal['x', 'o']) -> None:
        self.name = name
        self.sign = sign


class _XOTable:

    def __init__(self):
        self.xo_map = {k: None for k in range(1, 10)}  # {1:x, 2: None, 3: o, ...}

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

    def mark_update(self, cell_no, sign: str):
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
        super().__init__()
        self.player1, self.player2, self.table = player1, player2, _XOTable()

    def _calculate_result(self) -> str:
        win_list = ["123", "456", "789", "147", "258", "369", "159", "357"]
        for item in win_list:
            value_list = [self.table.xo_map[int(index)] for index in item if self.table.xo_map[int(index)]]
            if "".join(value_list) == "xxx" or "".join(value_list) == "ooo":
                return "".join(value_list)[0]  # change true and false to player sign
        return ""  # bool(empty str) == False

    def mark(self, cell_no, player: Union[_Player, Literal['x', 'o'], int]):
        if not 1 <= cell_no <= 9:  # condition is reversed!
            raise self.InvalidCellError(cell_no, "cell number is invalid")
        if player == "x" or player == "o" or player == "X" or player == "O":
            player = self.player1 if self.player1.sign == player.lower() else self.player2  # lower sign player
        elif player == '1' or player == '2': #number 1 & 2 must be string because may be xo
            player = self.player1 if player == '1' else self.player2
        elif player == self.player1.name or player == self.player2.name: #get player with name
            player = self.player1 if player == self.player1.name else self.player2
        else:
            raise self.InvalidPlayer(player, "invalid player")
        self.table.mark_update(cell_no, player.sign)  # table is self attribute so table change to self.table
        print(self.table)

    def winner(self):  # -> Optional[_Player]:
        res = self._calculate_result()  # res = 'x' or res = 'o' or res = ''
        # if not res and None in self.table.xo_map.values():  # check winner before end game round raise Exception
        #     raise self.UnFinishedGameError("The Game has not Finished yet!...")
        if res:  # if res != ''
            return self.player1 if res == self.player1.sign else self.player2  # find winner player sign
        elif not res and None not in self.table.xo_map.values():
            return None
        return False


player1_name = input("Please Enter Your Name:")
player1_sign = input("Please Enter Your Sign:").lower()
player1 = _Player(player1_name, player1_sign)
player2_name = input("Please Enter Your Name:")
player2_sign = 'o' if player1_sign == 'x' else 'x'  # auto sign for player2
player2 = _Player(player2_name, player2_sign)  # player1_name to player2_name

winner_dict = {player1: 0, player2: 0}
game: List[any] = [None for i in range(3)]
for game_round in range(3):
    game[game_round], winner = _XOGame(player1, player2), False  # winner before loop must defined
    turn_player = player1
    while winner == False:  # winner is None and not equal players
        turn = input(f"Please Enter A Cell Number and Your Mark(Just Cell Number for {turn_player.name} turn):")
        try: #get cell number and player
            num, sign = turn.split(" ")
        except: #get just cell number for suggested player
            num = turn
            sign = turn_player.sign
        try:  # handeling exceptions in mark method
            game[game_round].mark(int(num), sign)  # cell_no must be integer not string
            if ' ' not in turn: turn_player = player1 if turn_player == player2 else player2 #change turn if current turn
        except:
            print('\nTry Again...!\n')

        try:  # winner = player1 or player2
            winner = game[game_round].winner()
        except:
            pass  # handeling UnFinishedGameError and winner is None yet

    if isinstance(winner, _Player):
        winner_dict[winner] += 1
        print(f"\n{game_round + 1}th Round finished. This Round Winner Is {winner.name}\n")

    if winner is None:
        print(f"\n{game_round + 1}th Round finished. This Round Is A Tie\n")

winner_dict_values = list(winner_dict.values())
if winner_dict_values[0] != winner_dict_values[1]:
    winner_dict_reverse = {v: k for k, v in winner_dict.items()}
    print(f"The Winner IS: {winner_dict_reverse[sorted(winner_dict_reverse.keys())[1]].name}")  # print player.name
else:
    print("This Game Is A Tie")
