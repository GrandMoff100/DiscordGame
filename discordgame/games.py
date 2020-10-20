import asyncio
import os
import threading
from typing import List, AnyStr

import discord
from discord.ext.commands import Bot, command, Cog

from discordgame.errors import GameError

class Game:
    def __init__(
            self,
            name: str,
            layout: List[List[AnyStr]],
            ctx: discord.ext.commands.Context,
            btn_imgs=None,
            needs_text_input=False,
            needs_button_events=False
    ):
        if btn_imgs is None:
            btn_imgs = []

        self.name = name
        self.player = ctx.author
        self.channel = ctx.channel
        self.stopped = False

        self.needs_text_input = needs_text_input
        self.needs_button_events = needs_button_events

        self._btn_imgs = btn_imgs

        self._layout = layout
        self._remote_board = None

    async def initgame(self):
        # Send the first embed.
        self._remote_board = await self.channel.send(embed=await self._updated_embed())

        # Add the buttons.
        for button in self._btn_imgs:
            await self._remote_board.add_reaction(emoji=button)
        
        # Starts a mainloop function designed to be overridden.
        await self.mainloop()

    async def mainloop(self):
        """Designed to be overridden in a child class, used like tkinter mainloops."""
        pass

    async def on_text_event(self, player: discord.User, text: str):
        """Triggered when the player who's playing the game sends a message in the channel the game is in."""
        pass

    async def on_button_event(self, player: discord.User, emoji: str):
        """Triggered when the player who's playing the game pressed a reaction button"""
        pass

    @property
    def layout(self):
        """Unmodifiable layout variable."""
        return self._layout

    async def update_layout(self, new_layout: List[List[AnyStr]]):
        """A frame update function. Updates the remote board."""

        try:
            await self._remote_board.edit(embed=await self._updated_embed(new_layout))
        except AttributeError as err:
            raise SyntaxError('.startgame() wasn\'t called before updating layout.')

    async def _updated_embed(self, layout):
        """Generates an embed from the given layout."""
        lines = []
        for row in self.layout:
            converted_elements = []
            for src in row:
                converted_elements.append(await self.graphic(src))
            lines.append(''.join(converted_elements))

        embed = discord.Embed(
            title=self.name,
            description='\n'.join(lines)
        )
        if self.stats != {}:
            embed.add_field(
                name='Statistics',
                value='\n'.join(['{} {}'.format(item[0], item[1]) for item in self.stats.items()])
            )
        return embed

    async def graphic(self, src: str):
        """Checks for non-existing emoji's and substitues paths with their discord-emoji text."""
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
        """Tells GameHost to not trigger this game's events anymore."""
        self.needs_button_events = False
        self.needs_text_input = False

    def __repr__(self):
        """Representation function of a game object."""
        return '<Game name: {}, players: {}, stats: {}>'.format(
            self.name,
            self.player,
            self.stats
        )


