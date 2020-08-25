import discord
import discordgame as dg


class MadLib(dg.Game):
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
            self.stats['Blanks to Fill ->'] = len([word for word in self.word_blanks if word == '(blank)'])
            # ^^ Updates the Blanks to fill Counter.
            await self.update_layout([[self.lib.format(*self.word_blanks)]])  # Sends the changes to discord.
            if '(blank)' not in self.word_blanks:
                self.stop()
                await player.send(self.lib.format(*self.word_blanks))  # Sends the final MadLib to the channel.
        except ValueError:  # If there's no blank in the list.
            self.stop()
            await player.send(self.lib.format(*self.word_blanks))  # Sends the final MadLib to the channel.
