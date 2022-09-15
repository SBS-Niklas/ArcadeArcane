import arcade
import arcade.gui

WIDTH = 800
HEIGHT = 600
SPRITE_SCALING = 0.5
TITLE = "ArcaneArcadeGames"

class MenuView(arcade.View):
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

    def on_click_lauf(self,event):
        self.manager.disable()
        game = LaufGameView()
        self.window.show_view(game)


    def on_click_snake(self, event):
        self.manager.disable()
        game = SnakeView()
        self.window.show_view(game)

class SnakeView(arcade.View):
    def __init__(self):
        super().__init__()
    def on_show_view(self):
        arcade.set_background_color(arcade.color.GREEN)
    def on_draw(self):
        self.clear()

        arcade.draw_text("Ich bin eine Schlage SSSSS",
                         WIDTH / 2,
                         HEIGHT - 100,
                         arcade.color.BLACK,
                         font_size=20,
                         anchor_x="center")

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

class LaufGameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_sprite.velocity = [3, 3]

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
        self.window.show_view(self.game_view)

    def hauptmenue_button(self,event):
        game = MenuView()
        self.window.show_view(game)

    def on_draw(self):
        self.clear()
        self.manager.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)

def main():
    window = arcade.Window(WIDTH, HEIGHT,TITLE,fullscreen=True)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()