import os
import discord
from discordgame import Game, GameHost

host = GameHost('*')


class MadLib(Game):
    game_name = 'MadLib'

    def __init__(self, ctx):
        # Creates a list of blanks
        self.word_blanks = ['(blank)'] * 8
        # Assign a MadLib string to a variable.
        self.lib = 'The {} {}ed across the {} to get to the {} {}. It wanted to get to the {} so it could {} with a {}.'
        # Initialize the Parent Game class with the MadLib specific values.
        super().__init__(self.game_name, [[self.lib.format(*self.word_blanks)]], ctx=ctx, needs_text_input=True)

    # Define events to be triggered on a user's message event.
    async def on_text_event(self, player: discord.User, text: str):
        try:
            next_index = self.word_blanks.index('(blank)')  # Finds the left-most blank in the list.
            self.word_blanks.pop(next_index)  # Pops that blank from the list.
            self.word_blanks.insert(next_index, text)  # Inserts the user's word into the said blank.
            self.stats['Blanks to Fill:'] = len([word for word in self.word_blanks if word == '(blank)'])
            # ^^ Updates the Blanks to fill Counter.
            await self.update_layout([[self.lib.format(*self.word_blanks)]]) # Sends the changes to discord.
        except ValueError:  # If there's no blank in the list.
            await player.send(self.lib.format(*self.word_blanks))  # Sends the final MadLib to the channel.


class Snake(Game):
    game_name = 'Snake'

    def __init__(self, ctx):
        self.dimensions = [10, 5]
        self.direction = 'right'

        self.snake_coords = [[]]
        self.field = [[':black_square:' for x in range(self.dimensions[0])] for y in range(self.dimensions[1])]
        self.button_triggers = {
            '': self.up,
            ' ': self.down,
            '  ': self.left,
            '   ': self.right
        }

        super().__init__(self.game_name, self.field, ctx=ctx, needs_button_events=True)

    async def on_button_event(self, player: discord.User, emoji: str):
        if player == self.player:
            self.button_triggers[emoji]()

    def mainloop(self):
        pass

    def up(self):
        pass

    def down(self):
        pass

    def left(self):
        pass

    def right(self):
        pass

# Add our Games to the GameHost so users can play them.
host.add_game(Snake)
host.add_game(MadLib)

# Add run the GameHost.
TOKEN = os.getenv('TOKEN')
host.run(TOKEN)
