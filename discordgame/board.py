import discord, os
from typing import List, AnyStr


class Board(discord.Message):
    def __init__(self, title: str, layout: List[List[AnyStr]], stats: dict, color=discord.Color.green(), **kwargs):
        super().__init__(**kwargs)

        self._title = title
        self._layout = layout
        self.color = color
        self._stats = stats

    @property
    def stats(self):
        return self._stats

    @stats.setter
    def stats(self, new_stats: dict):
        self._stats = new_stats
        await self.edit(embed=self.construct_embed())

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, new_layout: List[List[AnyStr]]):
        self._layout = new_layout
        await self.edit(embed=self.construct_embed())

    def construct_embed(self):
        embed = discord.Embed(
            title=self._title,
            description='\n'.join([''.join([self.graphic(src) for src in row]) for row in self.layout])
        )
        for stat in self.stats.items():
            embed.add_field(name=stat[0], value=stat[1])
        return embed

    def graphic(self, src: str):
        if not os.path.exists(src):
            img = src
        else:
            name = src.split('/')[-1].split('.')[0]
            with open(src, 'rb') as image:
                emoji = await self.channel.guild.create_custom_emoji(name=name, image=image)
            img = ':{}:{}'.format(name, emoji.id)

        return img
