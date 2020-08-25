# DiscordGame
*DiscordGame is a Python Framework for making Games 
from simple mini games like Tic Tac Toe 
to full-fledge Dungeon and Dragon campaigns inside Discord.*

## Getting Started
### Installation
```shell script
$ pip install discordgame
```
Or clone the repo

```shell script
$ git clone https://github.com/GrandMoff100/DiscordGame
```

and run
```shell script
$ python setup.py install
```

### Usage
DiscordGame is structured like this. 
Whenever a trigger event like a reaction (called a button) or a new message is sent while a game is active, 
those events are passed to all games that are registered to a GameHost object. 
As you can see here with the on_text_event and on_button_event...
```python
import discordgame as dg


```

> Here's a couple of examples to help you get the gist of how this framework works...

- *A Simple MadLib made with ``discordgame``:*
```python
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
```

- *A Cool Snake Game made with ``discordgame``:*


### More Features


## Testing and Issues
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We welcome any new insights and issues with this framework.
To make an issue, head over to the issues page on our repository -> https://github.com/GrandMoff100/DiscordGame and open a new issue.
We look forward working on fixing any bugs or issues that we might have missed.

## Contribution
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;We'd love for you to Contribute! New features and optimizations are welcome! 
Just fork the Repository and make the changes and then make a pull request with your improvements.
If you make enough improvements, consistently we'll add you as a contributor.
