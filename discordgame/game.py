import asyncio
import os
import threading
from typing import List, AnyStr

import discord
from discord.ext.commands import Bot, command, Cog


class GameError(Exception):
    pass


class Game:
    def __init__(
            self,
            game_name: str,
            layout: List[List[AnyStr]],
            ctx: discord.ext.commands.Context,
            buttons=None,
            needs_text_input=False,
            needs_button_events=False
    ):
        if buttons is None:
            buttons = []

        self.game_name = game_name
        self.player = ctx.author
        self.channel = ctx.channel
        self.stopped = False

        self.needs_text_input = needs_text_input
        self.needs_button_events = needs_button_events

        self._buttons = buttons
        self.stats = {}
        self._layout = layout
        self._remote_board = None

    async def initgame(self):
        self._remote_board = await self.channel.send(embed=await self._updated_embed())
        for button in self._buttons:
            await self._remote_board.add_reaction(emoji=button)
        await self.mainloop()

    async def mainloop(self):
        pass

    async def on_text_event(self, player: discord.User, text: str):
        pass

    async def on_button_event(self, player: discord.User, emoji: str):
        pass

    @property
    def layout(self):
        return self._layout

    async def update_layout(self, new_layout: List[List[AnyStr]]):
        self._layout = new_layout
        try:
            await self._remote_board.edit(embed=await self._updated_embed())
        except AttributeError as err:
            raise SyntaxError('startgame wasn\'t called before updating layout.')

    async def _updated_embed(self):
        lines = []
        for row in self.layout:
            converted_elements = []
            for src in row:
                converted_elements.append(await self.graphic(src))
            lines.append(''.join(converted_elements))

        embed = discord.Embed(
            title=self.game_name,
            description='\n'.join(lines)
        )
        if self.stats != {}:
            embed.add_field(
                name='Statistics',
                value='\n'.join(['{} {}'.format(item[0], item[1]) for item in self.stats.items()])
            )
        return embed

    async def graphic(self, src: str):
        if not os.path.exists(src):
            img = src
        else:
            name = src.split('/')[-1].split('.')[0]
            with open(src, 'rb') as image:
                emoji = await self.channel.guild.create_custom_emoji(
                    name=src.split('/')[-1].split('.')[0],
                    image=image
                )
            img = ':{}:{}'.format(name, emoji.id)
        return img

    def stop(self):
        self.needs_button_events = False
        self.needs_text_input = False

    def __repr__(self):
        return '<Game name: {}, players: {}, stats: {}>'.format(
            self.game_name,
            self.player,
            self.stats
        )


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
        if message.author != self.user:
            await self.process_commands(message)
            prefix = await self.get_prefix(message)
            if not message.content.startswith(prefix):
                for game in self._game_instances:
                    if game.needs_text_input:
                        await game.on_text_event(message.author, message.content)

    async def on_reaction_add(self, reaction, user):
        if user != self.user:
            for game in self._game_instances:
                if game.needs_button_events:
                    await game.on_button_event(user, reaction)
            await reaction.message.remove_reaction(reaction, user)

    '''
    async def on_command_error(self, context, exception):
        guild = self.get_guild(710152655141339168)
        channel = guild.get_channel(710168025940230205)
        await channel.send(
            "```Exception: {}\n\nFrom: <User {}> in #{} from the <{}>```".format(
                exception,
                context.message.author,
                context.message.channel,
                context.message.channel.guild
            ))
    '''

    async def on_ready(self):
        guild = self.get_guild(710152655141339168)
        channel = guild.get_channel(710168025940230205)
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

    async def remove_game(self, game):
        del self._game_types[game]

    async def play_game(self, game: str, ctx: discord.ext.commands.Context):
        new_game = self._game_types[game](ctx=ctx)
        await new_game.initgame()
        self._game_instances.append(new_game)



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
            if game_instance.player == ctx.author and game_instance.game_name == game:
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
