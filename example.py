import os
import discord
from discordgame import Game, GameHost

host = GameHost('*')


class MadLib(Game):
    game_name = 'MadLib'

    def __init__(self, ctx):
        self.word_blanks = ['(blank)'] * 8
        self.lib = 'The {} {}ed across the {} to get to the {} {}. It wanted to get to the {} so it could {} with a {}.'

        super().__init__(self.game_name, [[self.lib.format(*self.word_blanks)]], ctx=ctx, needs_text_input=True)

    async def on_text_event(self, player: discord.User, text: str):
        try:
            next_index = self.word_blanks.index('(blank)')
            self.word_blanks.pop(next_index)
            self.word_blanks.insert(next_index, text)
            self.stats['Blanks to Fill:'] = len([word for word in self.word_blanks if word == '(blank)'])
            print(self.stats)
            await self.update_layout([[self.lib.format(*self.word_blanks)]])
        except ValueError:
            await player.send(self.lib.format(*self.word_blanks))


class Snake(Game):
    game_name = 'Snake'


host.add_game(Snake)
host.add_game(MadLib)
TOKEN = os.getenv('TOKEN')
host.run(TOKEN)
