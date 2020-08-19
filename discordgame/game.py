from typing import List, Union
import asyncio

import discord
from discord.ext.commands import Bot, command, Cog


class GameError(Exception):
    pass


class Game:
    def __init__(self, game_name: str, player: discord.User, channel, pass_text_input=False, pass_button_events=False,
                 *args, **kwargs):
        self.game_name = game_name
        self.player = player
        self.channel = channel

        self.needs_text_input = pass_text_input
        self.needs_button_events = pass_button_events

        self._stats = {}

    def on_text_event(self, player: discord.User, text: str):
        pass

    def on_button_event(self, player: discord.User, emoji: str):
        pass

    def __repr__(self):
        return '<{} name: {}, players: {}, stats: {}>'.format(type(self).__name__, self.game_name, self.player, self._stats)


class GameHost(Bot):
    _game_types = {}
    _game_instances = []

    def __init__(self, command_prefix: str):
        super().__init__(
            command_prefix,
            activity=discord.Activity(
                name='Your Games',
                type=discord.ActivityType.watching
            ))

        self.add_cog(Commands(self))

    @asyncio.coroutine
    def on_message(self, message):
        if message.author != self.user:
            for game in self._game_instances:
                if game.needs_text_input:
                    game.on_text_event(message.author, message.content)
            yield from self.process_commands(message)

    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            for game in self._game_instances:
                if game.needs_button_events:
                    game.on_button_event(user, reaction)

    async def on_command_error(self, context, exception):
        guild = self.get_guild(710152655141339168)
        channel = guild.get_channel(710168025940230205)
        await channel.send(
            "```Exception: {}\nFrom: <User {}> in #{} from the <{}>```".format(
                exception,
                context.message.author,
                context.message.channel,
                context.message.channel.guild))

    async def on_ready(self):
        guild = self.get_guild(710152655141339168)
        channel = guild.get_channel(710168025940230205)
        print(*[' '.join([item[0], repr(item[1])]) for item in self.all_commands.items()], sep='\n')
        await channel.send(
            '**I am ready as {}**\n    Serving __{}__ servers.\n**Servers:**\n{}'.format(
                self.user,
                len(self.guilds),
                '\n'.join(
                    ['- ' + guild.name for guild in self.guilds]
                )
            )
        )

    def add_game(self, game):
        if not issubclass(game, Game):
            raise TypeError('{} does not derive from a Game subclass or class.'.format(game))
        if not hasattr(game, 'game_name'):
            raise AttributeError('{} doesn\'t have a game name.'.format(game))

        self._game_types[game.game_name] = game

    def remove_game(self, game):
        del self._game_types[game]

    def play_game(self, game: str, player: discord.User, location: discord.Guild):
        new_game = self._game_types[game](player=player, location=location)
        self._game_instances.append(new_game)


class Commands(Cog):
    def __init__(self, bot: GameHost):
        self.bot = bot

    @command(help="Play a Game.")
    async def play(self, ctx, game: str):
        self.bot.play_game(game, ctx.author, ctx.channel.guild)
        # await ctx.send('You are playing {}!'.format(game))
