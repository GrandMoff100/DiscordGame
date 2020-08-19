from typing import List

import discord
import discordgame as dg

host = dg.GameHost('$')


class MyGame(dg.GraphicGame):
    def __init__(self, players: List[discord.User]):
        self.name = self.__class__.__name__
        self.board = dg.Board(
            self.name,
            [[dg.Graphic(':black_square') for i in range(10)] for i in range(7)],
        )

        super().__init__(self.name, players=players, board=self.board, )


TOKEN = 'NzQzNDg2MzEyMzcxMTkxODg5.XzVXlg.4FaD4aZFAMtxN_LMMSfl9K2abJk'

host.run(TOKEN)
