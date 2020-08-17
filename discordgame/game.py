from typing import Any, List, Union

import discord
from discord.ext.commands import Bot, command

from .boards import Board, BoardError


class GameError(Exception):
    pass


class Game:
    def __init__(self, game_name: str, players: List[discord.User], pass_text_input=False, pass_button_events=False, *args, **kwargs):
        self.game_name = game_name
        self.players = players
        self.needs_text_input = pass_text_input
        self.needs_button_events = pass_button_events
        self._stats = {}

        self.stdin = []

    def read(self):
        while not self.stdin:
            pass
        event, values = self.stdin[0]
        self.stdin.pop()
        return event, values

    def pass_stdin(self, stdin: List[Union[str, dict]]):
        self.stdin.append(stdin)

    def __init_subclass__(*cls, **kwargs):
        print(*cls, kwargs, sep=' -> ')

    def __repr__(self):
        return '<{} name: {}, players: {}, stats: {}>'.format(type(self).__name__, self.game_name, self.players, self._stats)


class GameHost(Bot):
    _game_types = {}
    _game_instances = []

    def __init__(self, command_prefix: str):
        super().__init__(
            command_prefix,
            activity=discord.Activity(
                name='',
                type=discord.ActivityType.listening,
                state='My State',
                details='My Custom Details'
            )
        )

    async def on_command_error(self, context, exception):
        guild = await self.get_guild(710152655141339168)
        channel = await guild.get_channel(710168025940230205)
        channel.send("Exception: {}\nFrom: {}".format(exception, context))
        context.send("Exception: {}\nFrom: {}".format(exception, context))

    async def on_message(self, message):
        for game in self._game_instances:
            game.pass_stdin(['text_input', {message.author: message.content}])

    @command()
    async def play(self, ctx, game_name):
        new_game = [game_name, self._game_types[game_name](player=ctx.author)]
        self._game_instances.append(new_game)

    def add_game(self, game):
        if not issubclass(game, Game) or not issubclass(game, TextGame) or not issubclass(game, GraphicGame):
            raise TypeError('{} does not derive from a Game subclass or class.'.format(game))
        if not hasattr(game, 'game_name'):
            raise AttributeError('{} doesn\'t have a game name.'.format(game))

        self._game_types[game.game_name] = game

    def remove_game(self, game):
        del self._game_types[game]


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


