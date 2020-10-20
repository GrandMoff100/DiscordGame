import asyncio
import os
import threading
from typing import List, AnyStr

import discord
from discord.ext.commands import Bot, command, Cog

from discordgame.errors import GameError
from discordgame.games import Game


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

    async def on_message(self, message):
        """Triggered when a user sends a message in channel that the can see."""
        if message.author != self.user:
            await self.process_commands(message)
            prefix = await self.get_prefix(message)
            # If it's not a command trigger the on_text_event all registered game's requiring text events.
            if not message.content.startswith(prefix):
                for game in self._game_instances:
                    if game.needs_text_input:
                        await game.on_text_event(message.author, message.content)

    async def on_reaction_add(self, reaction, user):
        """Triggered whenever a user add's a reaction to a message in the GameHost's cache."""
        if user != self.user:
            # Triggers the on_button event for games that the user is playing that need button events.
            for game in self._game_instances:
                if game.needs_button_events and game.player == user:
                    await game.on_button_event(user, reaction)
            # Removes the reaction to tell the user that it's been pressed.
            await reaction.message.remove_reaction(reaction, user)

    async def on_command_error(self, context, exception):
        """Triggered whenever an error happens in a game and sends the error to where it happened."""
        await context.message.channel.send(
            "```Exception: {}\n\nFrom: <User {}> in #{} from the <{}>```".format(
                exception,
                context.message.author,
                context.message.channel,
                context.message.channel.guild
            ))

    def add_game(self, game):
        """Let's the user register games to GameHost to "host"."""
        if not issubclass(game, Game):
            raise TypeError('{} does not derive from a Game subclass or class.'.format(game))
        if not hasattr(game, 'name'):
            raise AttributeError('{} doesn\'t have a game name.'.format(game))

        # Adds it global gameHost registry.
        self._game_types[game.name] = game

    async def remove_game(self, game):
        """Removes the game class from the global game registry."""
        del self._game_types[game]

    async def play_game(self, game: str, ctx: discord.ext.commands.Context):
        """Create's a new instance of the game class from the game registry and calls it init method to run async fuction outside of __init__."""
        new_game = self._game_types[game](ctx=ctx)
        await new_game.initgame()
        self._game_instances.append(new_game)


"""The Cog that add's game management commands to passed GameHost."""
class Commands(Cog):
    def __init__(self, bot: GameHost):
        self.bot = bot

    @command(help="Play a Game.")
    async def play(self, ctx, game: str):
        try:
            await self.bot.play_game(game, ctx=ctx)
            await ctx.send('You are playing {}!'.format(game))
        except KeyError:
            await ctx.send("I'm sorry to tell you this but that game can't be played.")

    @command(help="Forcefully stops all games of that type you're playing.")
    async def stop(self, ctx, game: str):
        for game_instance in self.bot._game_instances:
            if game_instance.player == ctx.author and game_instance.name == game:
                game_instance.needs_text_input = False
                game_instance.needs_button_events = False

        alive_games = []
        for game_instance in self.bot._game_instances:
            if game_instance.needs_text_input or game_instance.needs_button_events:
                alive_games.append(game_instance)

        self.bot._game_instances = alive_games
        ctx.send('You have quit all of your {} games!'.format(game))

    @command(help='Lists the Games that this Bot has available.')
    async def games(self, ctx):
        games, count = "My Games:\n", 1
        for game in self.bot._game_types:
            games += '{}. {}\n'.format(count, game)
            count += 1
        games = '```\n{}```'.format(games)
        await ctx.send(games)
