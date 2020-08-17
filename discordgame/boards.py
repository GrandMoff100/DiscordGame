from typing import Union, List, Any

import discord


class Graphic:
    """

    :img: - can either be a path to an image to use as  discord emoji or can be a built in discord emoji tag e.g. path/to/img or :thumbsup: 
    :is_path: - where the user tells the Graphic to look for the path instead of treating the string as an emoji.
    """
    def __init__(self, src: str, is_path=False):
        self.is_custom_emoji = is_path
        if not is_path:
            self.img = src
        else:
            with open(src, 'rb') as image:
                self.img = image


class Board:
    def __init__(self, title: str, layout: List[List[Graphic]], **fields):
        self._layout = [[]]
        self.layout = layout

        self.title = title
        self.fields = fields

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, new_layout: List[List[Graphic]]):
        """Method for doing something when the layout is updated."""
        pass

    @property
    def width(self):
        return len(self.layout)

    @property
    def height(self):
        return len(self.layout[0])

    def embed(self):
        embed = discord.Embed(title=self.title, description=str(self))

        for field in self.fields.items():
            name, value = field
            embed.add_field(name=name, value=value)

        return embed

    def __str__(self):
        return '\n'.join([''.join(row) for row in self.layout])


class BoardError(Exception):
    pass