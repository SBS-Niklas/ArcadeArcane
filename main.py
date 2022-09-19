from datetime import time
from random import randint, random, randrange
from time import sleep
from turtledemo.minimal_hanoi import play

from PIL import Image

import arcade
import arcade.gui
import singleton

WIDTH = 1250
HEIGHT = 750
SPRITE_SCALING = 0.5
TITLE = "ArcaneArcadeGames"

class SingletonClass(object):
  def __new__(cls):
    if not hasattr(cls, 'instance'):
      cls.instance = super(SingletonClass, cls).__new__(cls)
    return cls.instance
    musicPlayer = music.play()
    Score = 0

class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        music = arcade.load_sound("Hauptmenü.wav")
        musikTest.musicPlayer = music.play()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.WHITE)

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        self.v_box = arcade.gui.UIBoxLayout()

        start_snake_button = arcade.gui.UIFlatButton(text="Start Snake", width=200)
        self.v_box.add(start_snake_button.with_space_around(bottom=20))

        start_lauf_button = arcade.gui.UIFlatButton(text="Start Laufmännchen/in", width=200)
        self.v_box.add(start_lauf_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton(text="Close", width=200)
        self.v_box.add(quit_button.with_space_around(bottom=20))

        test = arcade.gui.UITextArea(text="Press ESC in any Game for Menü",width=240, text_color= arcade.color.BLACK)
        self.v_box.add(test.with_space_around(bottom=20))

        start_snake_button.on_click = self.on_click_snake
        start_lauf_button.on_click = self.on_click_lauf
        quit_button.on_click = self.on_click_quit


        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_click_quit(self,event):
        arcade.close_window()

    def on_click_lauf(self, event):
        musikTest.musicPlayer.pause()
        self.clear()
        self.manager.disable()
        game = LaufGameView()
        self.window.show_view(game)


    def on_click_snake(self, event):
        musikTest.musicPlayer.pause()
        self.manager.disable()
        game = SnakeView()
        self.window.show_view(game)

class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()


    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        test = arcade.gui.UITextArea(text="Score: " + str(SingletonClass.Score), width=200, text_color=arcade.color.BLACK, font_size=30 )
        self.v_box.add(test.with_space_around(bottom=20))

        haupt_button = arcade.gui.UIFlatButton(text="Hauptmenü", width=200)
        self.v_box.add(haupt_button.with_space_around(bottom=20))

        replay_button = arcade.gui.UIFlatButton(text="New Game", width=200)
        self.v_box.add(replay_button.with_space_around(bottom=20))

        replay_button.on_click = self.replay_button
        haupt_button.on_click = self.hauptmenue_button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def replay_button(self,event):
        musikTest.musicPlayer.pause()
        arcade.set_background_color(arcade.color.WHITE)
        game = SnakeView()
        self.window.show_view(game)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def hauptmenue_button(self,event):
        musikTest.musicPlayer.pause()
        game = MenuView()
        self.window.show_view(game)

class SnakeView(arcade.View):
    def __init__(self):
        super().__init__()

        music = arcade.load_sound("SnakeMusic.wav")
        musikTest.musicPlayer = music.play()
        self.score = 0

        self.moved = None
        self.snake_image = arcade.Sprite("Snake.png",image_height=50,image_width=50)
        self.snake_coords = []
        self.snake_move_x = 0
        self.snake_move_y = 20

        self.head_image = arcade.Sprite("SnakeHead.png",image_height=50,image_width=50)
        self.snake_head = None
        self.new_head_position = None
        self.direction = [0,1]

        self.food_image = arcade.Sprite("Snake.png",image_height=50,image_width=50)
        self.food = None
        self.food_coords = []

        self.gameOn = False

        self.snake_coords_collision = []



    def setup(self):
        self.snake_coords = [[400,400],[400,350],[400,300]]
        self.snake_head = self.snake_coords[0]

        self.food_coords = [randrange(50,1200,50),randrange(50,700,50)]

        self.gameOn = True

    def on_draw(self):
        if self.gameOn == False:
            self.setup()

        self.clear()
        arcade.start_render()
        self.head_image.center_x = self.snake_coords[0][0]
        self.head_image.center_y = self.snake_coords[0][1]
        self.head_image.draw()

        self.food_image.center_x = self.food_coords[0]
        self.food_image.center_y = self.food_coords[1]
        self.food_image.draw()


        for x,y in self.snake_coords[1:]:
            self.snake_image.center_x = x;self.snake_image.center_y = y
            self.snake_image.draw()

            arcade.draw_text("Score:" + str(self.score) ,20,HEIGHT - 20,arcade.color.BLACK)

    def game_over(self):
        SingletonClass.Score = self.score
        game = GameOverView()
        self.window.show_view(game)

    def update(self,delta_time):
        if self.snake_head == self.food_coords:
            self.score += 1
            Score = self.score
            self.food_coords = [randrange(50,1200,50),randrange(50,700,50)]
            self.snake_coords.append(self.snake_coords[-1][0]+50)

        if self.moved:
            for i in range(2,len(self.snake_coords)):
                 if self.snake_head == self.snake_coords[i]:
                    sleep(1);self.game_over()
            if self.snake_head[0] < 50:
                sleep(1);self.game_over()
            elif self.snake_head[0] > WIDTH - 50:
                sleep(1);self.game_over()
            elif self.snake_head[1] < 50:
                sleep(1),self.game_over()
            elif self.snake_head[1] > HEIGHT -50:
                sleep(1),self.game_over()
            else:
                self.snake_head = self.snake_coords[0]
                self.new_head_position = [self.snake_head[0] + self.snake_move_x, self.snake_head[1] + self.snake_move_y]
                self.snake_coords = [self.new_head_position] + self.snake_coords[:-1]


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.D or key == arcade.key.A or  key == arcade.key.W:
            self.moved = True
        if key == arcade.key.D and self.direction[0] != -1:
            self.snake_move_x = 50
            self.snake_move_y = 0
            self. direction = [1,0]

        if key == arcade.key.A and self.direction[0] != 1:
            self.snake_move_x = -50
            self.snake_move_y = 0
            self. direction = [-1,0]

        if key == arcade.key.W and self.direction[1] != -1:
            self.snake_move_x = 0
            self.snake_move_y = 50
            self.direction = [0, 1]

        if key == arcade.key.S and self.direction[1] != 1:
            self.snake_move_x = 0
            self.snake_move_y = -50
            self.direction = [0, -1]

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

    def gameOver(self):
        game = GameOverView()
        self.window.show_view(game)

class LaufGameView(arcade.View):
    def __init__(self):
        super().__init__()


        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

        music = arcade.load_sound("LaufGame.wav")
        musikTest.musicPlayer = music.play()

    def on_show_view(self):
        arcade.set_background_color(arcade.color.AMAZON)

    def on_draw(self):
        self.clear()
        # Draw all the sprites.
        self.player_sprite.draw()

    def on_update(self, delta_time):
        # Call update on all sprites
        self.player_sprite.update()

        # Bounce off the edges
        if self.player_sprite.left < 0 or self.player_sprite.right > WIDTH:
            self.player_sprite.change_x *= -1
        if self.player_sprite.bottom < 0 or self.player_sprite.top > HEIGHT:
            self.player_sprite.change_y *= -1

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view


    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UIBoxLayout()

        resume_button = arcade.gui.UIFlatButton(text="Resume", width=200)
        self.v_box.add(resume_button.with_space_around(bottom=20))

        haupt_button = arcade.gui.UIFlatButton(text="Hauptmenü", width=200)
        self.v_box.add(haupt_button.with_space_around(bottom=20))

        mute_button = arcade.gui.UIFlatButton(text="Mute", width=200)
        self.v_box.add(mute_button.with_space_around(bottom=20))

        haupt_button.on_click = self.hauptmenue_button
        resume_button.on_click = self.resume_button

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def resume_button(self, event):
        arcade.set_background_color(arcade.color.WHITE)
        self.window.show_view(self.game_view)

    def hauptmenue_button(self,event):
        musikTest.musicPlayer.pause()
        game = MenuView()
        self.window.show_view(game)
    def on_draw(self):
        self.clear()
        self.manager.draw()


    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)

def main():
    window = arcade.Window(WIDTH, HEIGHT,TITLE,fullscreen=False,update_rate=0.08)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    musikTest = SingletonClass()
    main()