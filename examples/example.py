import os
from discordgame import GameHost

# Import our example games from 2 other files.
from examples.snake import Snake
from examples.madlib import MadLib

host = GameHost('*')

# Add our Games to the GameHost so users can play them.
host.add_game(Snake)
host.add_game(MadLib)

# Add run the GameHost.
TOKEN = os.getenv('TOKEN')
host.run(TOKEN)
