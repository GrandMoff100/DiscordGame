import discord
from discordgame import Game

import time
import random


class Snake(Game):
    game_name = 'Snake'

    def __init__(self, ctx):
        self.dimensions = [10, 5]
        self.direction = 'right'

        self.snake_coord_list = [[0, 0]]

        self.background = ':black_large_square:'
        self.snake = ':white_large_square:'
        self.fruit = ':strawberry:'

        self.field = [[self.background for x in range(self.dimensions[0])] for y in range(self.dimensions[1])]

        for x, y in self.snake_coord_list:
            self.field[y][x] = self.snake

        self.button_triggers = {
            '⬅': self.left,
            '⬆': self.up,
            '⬇': self.down,
            '➡': self.right,
            '🛑': self.stop
        }

        self.stopped = False  # Sets a global boolean to tell `mainloop` when to exit.
        self.speed = 1  # Updates one time per second

        super().__init__(
            self.game_name,
            self.field,
            ctx=ctx,
            buttons=self.button_triggers.keys(),
            needs_button_events=True
        )

    async def generate_fruit(self):
        random_x = random.randint(0, len(self.layout[0]) - 1)
        random_y = random.randint(0, len(self.layout) - 1)

        if self.layout[random_y][random_x] == self.background:
            old_layout = self.layout
            old_layout[random_y][random_x] = self.fruit
            await self.update_layout(old_layout)
        else:
            await self.generate_fruit()

    async def on_button_event(self, player: discord.User, emoji: str):
        if player == self.player:
            self.button_triggers[emoji]()

    async def mainloop(self):
        await self.generate_fruit()
        while not self.stopped:
            await self.update_frame()
            time.sleep(1/self.speed)

    async def update_frame(self):
        snake_head_x, snake_head_y = self.snake_coord_list[0]

        if self.direction == 'up':
            print('Going Up')
            self.snake_coord_list.insert(0, [snake_head_x, snake_head_y + 1])
            self.snake_coord_list.pop(-1)
        elif self.direction == 'down':
            print('Going Down')
            self.snake_coord_list.insert(0, [snake_head_x, snake_head_y - 1])
            self.snake_coord_list.pop(-1)
        elif self.direction == 'left':
            print('Going Left')
            self.snake_coord_list.insert(0, [snake_head_x - 1, snake_head_y])
            self.snake_coord_list.pop(-1)
        elif self.direction == 'right':
            print('Going Right')
            self.snake_coord_list.insert(0, [snake_head_x + 1, snake_head_y])
            self.snake_coord_list.pop(-1)

        old_layout = self.layout
        try:
            for x, y in self.snake_coord_list:
                if old_layout[y][x] == self.fruit:
                    self.grow()
                    await self.generate_fruit()
                old_layout[y][x] = self.snake

            for y in range(len(old_layout)):
                for x in range(len(old_layout[0])):
                    if [x, y] not in self.snake_coord_list and old_layout[y][x] != self.fruit:
                        old_layout[y][x] = self.background

            await self.update_layout(old_layout)
        except IndexError:
            await self.channel.send('You crashed into the wall! :frowning2:')
            self.stop()

    @property
    def size(self):
        return len(self.snake_coord_list)

    def grow(self):
        if self.direction == 'up':
            x, y = self.snake_coord_list[-1]
            self.snake_coord_list.append([x, y - 1])

    def up(self):
        if self.direction not in ['right', 'left']:
            self.direction = 'up'

    def down(self):
        if self.direction not in ['right', 'left']:
            self.direction = 'down'

    def left(self):
        if self.direction not in ['up', 'down']:
            self.direction = 'left'

    def right(self):
        if self.direction not in ['up', 'down']:
            self.direction = 'right'

