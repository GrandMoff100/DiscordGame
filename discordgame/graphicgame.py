from typing import List

import discord

from .boards import BoardError, Board
from .game import Game


class TextGame(Game):
    def __init__(self, game_name: str, players: List[discord.User]):
        super().__init__(game_name, players, needs_text_input=True)

    def __init_subclass__(*cls, **kwargs):
        print(*cls, kwargs, sep=' -> ')


class GraphicGame(Game):
    def __init__(self, game_name: str, players: List[discord.User], board: Board, buttons: list):
        super().__init__(game_name, players, pass_button_events=True)
        self.board = board
        self.buttons = buttons
        self._board = None

    def __init_subclass__(*cls, **kwargs):
        print(*cls, kwargs, sep=' -> ')

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, new_msg):
        pass

    async def create_embed(self, channel):
        if self.msg is None:
            self.msg = await channel.send(embed=self.board.embed())
        else:
            raise BoardError('Board for game {} is already initialized, to update the board edit the self.board'.format(self))
