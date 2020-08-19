import discord

from .game import Game


class TextGame(Game):
    def __init__(self, game_name: str, player: discord.User, channel: discord.TextChannel, *args, **kwargs):
        super().__init__(game_name, player, channel, *args, needs_text_input=True, **kwargs)

    def __init_subclass__(*cls, **kwargs):
        print(*cls, kwargs, sep=' -> ')
