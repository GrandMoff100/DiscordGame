from typing import List, Dict
import os

import discord

from .game import Game, GameError


class GraphicGame(Game):
    def __init__(self, game_name: str, player: discord.User, channel: discord.TextChannel, screen: List[List[str]],
                 buttons: Dict[str: str], stats=None, **kwargs):
        super().__init__(game_name, player, channel, pass_button_events=True)

        if stats is None:
            stats = {}

        self.buttons = buttons
        self._stats = stats
        self._screen = screen
        self._game_msg = None

    def __init_subclass__(*cls, **kwargs):
        # print(*cls, kwargs, sep=' -> ')
        pass

    @property
    def screen(self):
        return self._screen

    @screen.setter
    def screen(self, new_screen: List[List[str]]):
        self._screen = new_screen
        self.update_embed(self.channel)

    @property
    def width(self):
        return len(self.screen)

    @property
    def height(self):
        return len(self.screen[0])

    def embed(self, **stats):
        embed = discord.Embed(
            title=self.game_name,
            description='\n'.join([''.join([self.graphic(square) for square in row]) for row in self.screen])
        )

        for field in stats.items():
            name, value = field
            embed.add_field(name=name, value=value)

        return embed

    async def update_embed(self, channel):
        if self._game_msg is None:
            self._game_msg = await channel.send(embed=self.embed())
        else:
            await self._game_msg.edit(embed=self.embed())

    def graphic(self, src: str):
        if not os.path.exists(src):
            img = src
        else:
            name = src.split('/')[-1].split('.')[0]
            with open(src, 'rb') as image:
                emoji = await self.channel.guild.create_custom_emoji(name=name, image=image)
            img = ':{}:{}'.format(name, emoji.id)

        return img
