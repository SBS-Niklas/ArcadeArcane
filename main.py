from random import randint, random, randrange
from time import sleep
import arcade.gui
import random
import arcade
from arcade import Window, Section, View, SpriteList, SpriteSolidColor, \
    SpriteCircle, draw_text, draw_line
from arcade.color import BLACK, BLUE, RED, BEAU_BLUE, GRAY, WHITE, PURPLE_PIZZAZZ

WIDTH = 1536
HEIGHT = 864
SPRITE_SCALING = 0.5
MOVEMENT_SPEED = 5
PLAYER_SECTION_WIDTH = 200
PLAYER_PADDLE_SPEED = 10
SPEED = 5
TITLE = "ArcaneArcadeGames"
SCORE = 0
# Fenstergröße
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Ballgröße
BALL_RADIUS = 10

# Geschwindigkeit des Balls
BALL_SPEED = 5

# Größe der Paddles
PADDLE_WIDTH = 20
PADDLE_HEIGHT = 80

# Geschwindigkeit der Paddles
PADDLE_SPEED = 5
max_length_input = 4
lastGame = 0
lastView = 0


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()

        #Abspeicherung der Letzen View für GameOverScreen
        main.lastView = "MenuView"

        #Joysticks erkenne
        joysticks = arcade.get_joysticks()
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.test = self.joystick2.push_handlers(self)
        else:
            # Handle if there are no joysticks.
            print("There are no joysticks, plug in a joystick and run again.")
            self.joystick = None

    def on_show_view(self): #Die Angezeigten GUI Elemente werden erstellt und einem Manager hinzugefügt
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout()
        self.background = arcade.load_texture("Pictures/BackgroundMenü.jpg")

        texture = arcade.load_texture("Pictures/SnakeVorschau.png")
        start_snake_button = arcade.gui.UITextureButton(x=(1536/2) -550, y=(864/2)  -250, height=500, width=500, texture=texture)
        self.v_box.add(start_snake_button.with_space_around(bottom=0))

        texture = arcade.load_texture("Pictures/Pong.png")
        start_pong_button = arcade.gui.UITextureButton(x=(1536/2) +50 , y=(864/2)  -250, height=500, width=500, texture=texture)
        self.v_box.add(start_pong_button.with_space_around(bottom=0))

        '''Nur für Maus steuerung nötig
        start_snake_button.on_click = self.on_click_snake
        start_pong_button.on_click = self.on_click_lauf'''

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def on_draw(self): #Die im Manager Gespeicherten GUI Elemente werden geladen (angezeigt)
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            1536, 864,
                                            self.background)
        self.manager.draw()

    def on_joybutton_press(self, _joystick, button): #Joyticks(Buttons) werden mit den entsprechenden Befehlen verknüpft
        """ Handle button-down event for the joystick """
        if button == 10 and main.lastView == "MenuView":
            game = PongInfoScreen()
            self.window.show_view(game)
        if button == 11 and main.lastView == "MenuView":
            game = SnakeInfoScreen()
            self.window.show_view(game)

    '''Nur für Maussteuerung nötig
    def on_click_lauf(self, event):
        self.clear()
        self.manager.disable()
        game = PongInfoScreen()
        self.window.show_view(game)
    def on_click_snake(self, event):
        self.manager.disable()
        game = SnakeViewZweispieler()
        self.window.show_view(game)'''
class PongInfoScreen(arcade.View):
    def __init__(self):
        super().__init__()

        # Abspeicherung der Letzen View für GameOverScreen
        main.lastView = "PongInfoScreen"

        # Joysticks erkenne
        joysticks = arcade.get_joysticks()
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.test = self.joystick2.push_handlers(self)

    def on_show_view(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout()

        self.background = arcade.load_texture("Pictures/BackgroundMenü.jpg")
        texture = arcade.load_texture("Pictures/Singel.png")
        singelPlayer = arcade.gui.UITextureButton(x=(1536/2) -130, y=764, height=50, width=50, texture=texture)
        self.v_box.add(singelPlayer)
        texture = arcade.load_texture("Pictures/Zwei.png")
        singelPlayer = arcade.gui.UITextureButton(x=(1536 / 2) - 130, y=700, height=50, width=50, texture=texture)
        self.v_box.add(singelPlayer)

        game_Info_Singelplayer = arcade.gui.UILabel(text="Press       for Singelplayer",x=(1536/2)-250 ,y=764, font_size=30,text_color=WHITE)
        self.v_box.add(game_Info_Singelplayer.with_space_around(bottom=20))
        game_Info_Multiplayer = arcade.gui.UILabel(text="Press       for Multiplayer",x= (1536 / 2) -250, y=700, font_size=30,text_color=WHITE)
        self.v_box.add(game_Info_Multiplayer.with_space_around(bottom=20))

        game_Highsocre_Text = arcade.gui.UITextArea(text="HIGESCORE 2PLAYER", x=60, y=150, height=300, width=300, font_size=30)
        self.v_box.add(game_Highsocre_Text)
        game_Highsocre_Text_Singel = arcade.gui.UITextArea(text="HIGESCORE 1PLAYER", x=60, y=550, height=300, width=300,font_size=30)
        self.v_box.add(game_Highsocre_Text)
        self.v_box.add(game_Highsocre_Text_Singel)

        # Einlesen + Anzeigen HighscorePong
        f = open("Scores/ScorePongEinspieler.txt", "r")
        game_Highsocre = arcade.gui.UITextArea(text=f.read(), x=60, y=60, height=300, width=300 ,font_size=30 )
        self.v_box.add(game_Highsocre)
        f = open("Scores/ScorePongZweispieler.txt", "r")
        game_Highsocre = arcade.gui.UITextArea(text=f.read(), x=60, y=450, height=300, width=300, font_size=30)
        self.v_box.add(game_Highsocre)
        f.close()

        game_Steuerung = arcade.gui.UITextArea(text="Steuerung 1Player: \nJoystick UP -> Padel UP \nJoystick Down -> Padel DOWN  \n\n Steuerung 2Player: \n Joystick Right -> Padel Right \n Joystick Left -> Padel Left  " , x=1000 ,y=0 ,height=400,width=600,font_size=25  )
        game_Anleitung = arcade.gui.UITextArea(text="Beschreibung: \nZiel des Spieles ist es den Ball so oft es geht abzuwähren. Erreiche einen Höheren Score um in der Ranglsite angezeit zu werden!!  ",x=1100, y=450, height=400, width=450, font_size=25)
        self.v_box.add(game_Anleitung)
        self.v_box.add(game_Steuerung)

        texture = arcade.load_texture("Pictures/Pong.png")
        start_lauf_button = arcade.gui.UITextureButton(x=450, y=60, height=500, width=500, texture=texture)
        self.v_box.add(start_lauf_button.with_space_around(bottom=0))

        start_lauf_button.on_click = self.on_click_pong

        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box))

    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 4 and main.lastView == "PongInfoScreen":
            game = PongView()
            game.setup()
            self.window.show_view(game)
        if button == 5 and main.lastView == "PongInfoScreen":
            game = PongView()
            game.setup()
            self.window.show_view(game)
    def on_click_pong(self, event):
        self.manager.disable()
        game = PongView()
        game.setup()
        self.window.show_view(game)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)
        self.manager.draw()
class SnakeInfoScreen(arcade.View):
    def __init__(self):
        super().__init__()

        main.lastView = "SnakeInfoScreen"

        joysticks = arcade.get_joysticks()
        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.test = self.joystick2.push_handlers(self)

    def on_show_view(self):
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.v_box = arcade.gui.UILayout()

        self.background = arcade.load_texture("Pictures/BackgroundMenü.jpg")

        game_Info_Singelplayer = arcade.gui.UILabel(text="Press    for Singelplayer",x=(1536/2)-150 ,y=764, font_size=30,text_color=arcade.color.AERO_BLUE)
        self.v_box.add(game_Info_Singelplayer.with_space_around(bottom=20))
        game_Info_Multiplayer = arcade.gui.UILabel(text="Press    for Multiplayer", x=(1536 / 2) - 150, y=700, font_size=30,
                                       text_color=arcade.color.AERO_BLUE)
        self.v_box.add(game_Info_Multiplayer.with_space_around(bottom=20))

        game_Highsocre_Text = arcade.gui.UITextArea(text="HIGSCORE", x=60, y=150, height=300, width=300, font_size=30)
        self.v_box.add(game_Highsocre_Text)

        # Einlesen + Anzeigen HighscorePong
        f = open("Scores/ScorePongEinspieler.txt", "r")
        game_Highsocre = arcade.gui.UITextArea(text=f.read(), x=60, y=60, height=300, width=300 ,font_size=30 )
        self.v_box.add(game_Highsocre)
        print(f.read())
        f.close()

        game_Anleitung = arcade.gui.UITextArea(text="Einspieler: \nJoytick OBEN -> Padel OBEN \nJoystick UNTEN -> Padel UNTEN \n\nMultiplayer: \nJoystick RECHTS -> Padel RECHTS \nJoystick LINKS -> PADEL LINKS" , x=1100 ,y=60 ,height=750,width=400,font_size=25  )

        self.v_box.add(game_Anleitung)

        texture = arcade.load_texture("Pictures/SnakeVorschau.png")
        start_lauf_button = arcade.gui.UITextureButton(x=450, y=60, height=500, width=500, texture=texture)
        self.v_box.add(start_lauf_button.with_space_around(bottom=0))

        start_lauf_button.on_click = self.on_click_snake

        self.manager.add(
            arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.v_box))

    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 5 and main.lastView == "SnakeInfoScreen":
            game = SnakeViewEinspieler()
            self.window.show_view(game)
        if button == 4 and main.lastView == "SnakeInfoScreen":
            game = SnakeViewZweispieler()
            self.window.show_view(game)
    def on_click_snake(self, event):
        self.manager.disable()
        game = SnakeViewZweispieler()
        self.window.show_view(game)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)
        self.manager.draw()
class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_update_rate(0.02)
        self.maus = arcade.SpriteCircle(color=PURPLE_PIZZAZZ, radius=10)
        joysticks = arcade.get_joysticks()

        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.joystick2.push_handlers(self)


        main.lastView = "GameOver"
        width_button = 70
        height_button = 50
        self.drücken = False

        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        arcade.set_background_color(arcade.color.DARK_BLUE_GRAY)

        self.ui_text_label = arcade.gui.UILabel(text='', width=200, height=30, align='center', font_size=20)

        # First Line
        self.firstLineLayout = arcade.gui.UIBoxLayout(vertical=False)

        #self.q_button = arcade.gui.UIFlatButton(text="Q", width=width_button, height=height_button)
        #self.firstLineLayout.children.append(self.q_button)
        #self.q_button.on_click = self.on_click_q
        self.q = SpriteSolidColor(width=width_button, height=height_button , color=WHITE)
        self.q.set_position(20,20)

        w_button = arcade.gui.UIFlatButton(text="W", width=width_button, height=height_button)
        self.firstLineLayout.add(w_button)
        w_button.on_click = self.on_click_w

        e_button = arcade.gui.UIFlatButton(text="E", width=width_button, height=height_button)
        self.firstLineLayout.add(e_button)
        e_button.on_click = self.on_click_e

        r_button = arcade.gui.UIFlatButton(text="R", width=width_button, height=height_button)
        self.firstLineLayout.add(r_button)
        r_button.on_click = self.on_click_r

        t_button = arcade.gui.UIFlatButton(text="T", width=width_button, height=height_button)
        self.firstLineLayout.children.append(t_button)
        t_button.on_click = self.on_click_t

        z_button = arcade.gui.UIFlatButton(text="Z", width=width_button, height=height_button)
        self.firstLineLayout.add(z_button)
        z_button.on_click = self.on_click_z

        u_button = arcade.gui.UIFlatButton(text="U", width=width_button, height=height_button)
        self.firstLineLayout.add(u_button)
        u_button.on_click = self.on_click_u

        i_button = arcade.gui.UIFlatButton(text="I", width=width_button, height=height_button)
        self.firstLineLayout.add(i_button)
        i_button.on_click = self.on_click_i

        o_button = arcade.gui.UIFlatButton(text="O", width=width_button, height=height_button)
        self.firstLineLayout.add(o_button)
        o_button.on_click = self.on_click_o

        p_button = arcade.gui.UIFlatButton(text="P", width=width_button, height=height_button)
        self.firstLineLayout.add(p_button)
        p_button.on_click = self.on_click_p

        # Second Line
        self.secondLineLayout = arcade.gui.UIBoxLayout(vertical=False)

        a_button = arcade.gui.UIFlatButton(text="A", width=width_button, height=height_button)
        self.secondLineLayout.children.append(a_button)
        a_button.on_click = self.on_click_a

        s_button = arcade.gui.UIFlatButton(text="S", width=width_button, height=height_button)
        self.secondLineLayout.children.append(s_button)
        s_button.on_click = self.on_click_s

        d_button = arcade.gui.UIFlatButton(text="D", width=width_button, height=height_button)
        self.secondLineLayout.children.append(d_button)
        d_button.on_click = self.on_click_d

        f_button = arcade.gui.UIFlatButton(text="F", width=width_button, height=height_button)
        self.secondLineLayout.children.append(f_button)
        f_button.on_click = self.on_click_f

        g_button = arcade.gui.UIFlatButton(text="G", width=width_button, height=height_button)
        self.secondLineLayout.children.append(g_button)
        g_button.on_click = self.on_click_g

        h_button = arcade.gui.UIFlatButton(text="H", width=width_button, height=height_button)
        self.secondLineLayout.children.append(h_button)
        h_button.on_click = self.on_click_h

        j_button = arcade.gui.UIFlatButton(text="J", width=width_button, height=height_button)
        self.secondLineLayout.children.append(j_button)
        j_button.on_click = self.on_click_j

        k_button = arcade.gui.UIFlatButton(text="K", width=width_button, height=height_button)
        self.secondLineLayout.children.append(k_button)
        k_button.on_click = self.on_click_k

        l_button = arcade.gui.UIFlatButton(text="L", width=width_button, height=height_button)
        self.secondLineLayout.children.append(l_button)
        l_button.on_click = self.on_click_l

        # Third Line
        self.thirdLineLayout = arcade.gui.UIBoxLayout(vertical=False)

        y_button = arcade.gui.UIFlatButton(text="Y", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(y_button)
        y_button.on_click = self.on_click_y

        x_button = arcade.gui.UIFlatButton(text="X", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(x_button)
        x_button.on_click = self.on_click_x

        c_button = arcade.gui.UIFlatButton(text="C", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(c_button)
        c_button.on_click = self.on_click_c

        v_button = arcade.gui.UIFlatButton(text="V", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(v_button)
        v_button.on_click = self.on_click_v

        b_button = arcade.gui.UIFlatButton(text="B", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(b_button)
        b_button.on_click = self.on_click_b

        n_button = arcade.gui.UIFlatButton(text="N", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(n_button)
        n_button.on_click = self.on_click_n

        m_button = arcade.gui.UIFlatButton(text="M", width=width_button, height=height_button)
        self.thirdLineLayout.children.append(m_button)
        m_button.on_click = self.on_click_m

        # Keyboard Layout
        self.keyboardLayout = arcade.gui.UIBoxLayout()
        self.keyboardLayout.add(self.ui_text_label)
        self.keyboardLayout.add(self.firstLineLayout)
        self.keyboardLayout.add(self.secondLineLayout)
        self.keyboardLayout.add(self.thirdLineLayout.with_space_around(bottom=20))

        haupt_button = arcade.gui.UIFlatButton(text="Mainmenue", width=200)
        self.keyboardLayout.add(haupt_button.with_space_around(bottom=20))

        replay_button = arcade.gui.UIFlatButton(text="New Game", width=200)
        self.keyboardLayout.add(replay_button.with_space_around(bottom=20))

        save_button = arcade.gui.UIFlatButton(text="SAVE", width=200)
        self.keyboardLayout.add(save_button.with_space_around(bottom=20))


        replay_button.on_click = self.replay_button
        haupt_button.on_click = self.hauptmenue_button
        save_button.on_click = self.save_button


        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.keyboardLayout)
        )

    def on_joybutton_press(self, _joystick, button):
        if button == 2:
            self.drücken = True


    def on_click_q(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "Q"
            self.update_text()

    def on_click_w(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "W"
            self.update_text()

    def on_click_e(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "E"
            self.update_text()

    def on_click_r(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "R"
            self.update_text()

    def on_click_t(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "T"
            self.update_text()

    def on_click_z(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "Z"
            self.update_text()

    def on_click_u(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "U"
            self.update_text()

    def on_click_i(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "I"
            self.update_text()

    def on_click_o(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "O"
            self.update_text()

    def on_click_p(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "P"
            self.update_text()

    def on_click_a(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "A"
            self.update_text()

    def on_click_s(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "S"
            self.update_text()

    def on_click_d(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "D"
            self.update_text()

    def on_click_f(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "F"
            self.update_text()

    def on_click_g(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "G"
            self.update_text()

    def on_click_h(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "H"
            self.update_text()

    def on_click_j(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "J"
            self.update_text()

    def on_click_k(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "K"
            self.update_text()

    def on_click_l(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "L"
            self.update_text()

    def on_click_y(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "Y"
            self.update_text()

    def on_click_x(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "X"
            self.update_text()

    def on_click_c(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "C"
            self.update_text()

    def on_click_v(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "V"
            self.update_text()

    def on_click_b(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "B"
            self.update_text()

    def on_click_n(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "N"
            self.update_text()

    def on_click_m(self, event):
        if len(self.ui_text_label.text) < max_length_input:
            self.pressed_key = "M"
            self.update_text()


    def on_update(self, delta_time: float):
        self.center_x = 0
        self.center_y = 0

        if self.joystick:
            # x-axis
            self.change_x = self.joystick.x
            # y-axis
            self.change_y = -self.joystick.y

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x == 1.0:
            print(self.center_x)

        if self.center_x == 1.0:
            self.on_key_press(self, 1)
        if self.center_x == -1.0:
            self.on_key_press(self, 1)
        if self.center_y == 1.0:
            self.on_key_press(self, 1)
        if self.center_y == -1.0:
            self.on_key_press(self, 1)
        if self.center_y != 1.0 and self.center_y != -1.0 and self.center_x != 1.0 and self.center_x != -1.0:
            self.on_key_release(self, 1)

        self.maus.update()

        if self.maus.collides_with_sprite(self.q) and self.drücken == True:
            if len(self.ui_text_label.text) < max_length_input:
                self.pressed_key = "Q"
                self.update_text()
            self.drücken = False

    def on_key_press(self, symbol: int, modifiers: int):

            if self.center_y == -1.0:
                self.maus.change_y = 5
            if self.center_y == 1.0:
                self.maus.change_y = -5
            if self.center_x == -1.0:
                self.maus.change_x = 5
            if self.center_x == 1.0:
                self.maus.change_x = -5

    def on_key_release(self, _symbol: int, _modifiers: int):
            self.maus.stop()


    def update_text(self):
        label_text = self.ui_text_label.text
        self.ui_text_label.text = label_text + self.pressed_key
        print("Name: ", self.ui_text_label.text)

    def on_show_view(self):
        arcade.set_background_color(arcade.color.RED)
        self.background = arcade.load_texture("Pictures/GameOverView.jpg")

    def replay_button(self,event):
        if main.lastGame == 2:
            game = SnakeViewZweispieler()
        if main.lastGame == 3:
            game = PongView()
            game.setup()
        if main.lastGame == 1:
            game = SnakeViewEinspieler()

        self.window.show_view(game)

    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)
        self.manager.draw()
        self.q.draw()
        self.maus.draw()
    def hauptmenue_button(self,event):
        game = MenuView()
        self.window.show_view(game)

    def save_button(self,event):
        print("HALLO")
        if main.lastGame == 1:
            f = open("Scores/ScoreSnakeEinspieler.txt", "a")
        if main.lastGame ==2:
            f = open("Scores/ScoreSnakeZweispieler.txt", "a")
        if main.lastGame == 3:
            f = open("Scores/ScorePongEinspieler.txt", "a")
        if main.lastGame == 4:
            f = open("Scores/ScorePongZweispieler.txt", "a")

        f.write(str(self.ui_text_label.text) + " " + str(main.SCORE) + "\n")
        f.close()
class SnakeViewZweispieler(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_update_rate(0.15)
        joysticks = arcade.get_joysticks()
        self.background = arcade.load_texture("Pictures/GameBackground.png")
        main.lastView = "SnakeViewZweispieler"

        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.joystick2.push_handlers(self)

        self.score = 0

        #SingletonClass.TEST = 1
        self.moved = None
        self.bug = None

        self.snake_image = arcade.Sprite("Pictures/SnakeVorschau.png", image_height=50, image_width=50)
        self.snake_coords = []
        self.snake_move_x = 0
        self.snake_move_y = 20

        self.head_image = arcade.Sprite("Pictures/SnakeHead.png", image_height=50, image_width=50)
        self.snake_head = None
        self.new_head_position = None
        self.direction = [0,1]

        self.food_image = arcade.Sprite("Pictures/SnakeHead.png", image_height=50, image_width=50)
        self.food = None
        self.food_coords = []

        self.gameOn = False

        self.snake_coords_collision = []

        self.moved2 = None
        self.bug2 = None
        self.snake_image2 = arcade.Sprite("Pictures/SnakeVorschau.png", image_height=50, image_width=50)
        self.snake_coords2 = []
        self.snake_move_x2 = 0
        self.snake_move_y2 = 20

        self.head_image2 = arcade.Sprite("Pictures/SnakeVorschau.png", image_height=50, image_width=50)
        self.snake_head2 = None
        self.new_head_position2 = None
        self.direction2 = [0, 1]

        self.food_image2 = arcade.Sprite("Pictures/SnakeVorschau.png", image_height=50, image_width=50)
        self.food2 = None
        self.food_coords2 = []

        self.gameOn = False

        self.snake_coords_collision2 = []
    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 2 and main.lastView == "SnakeViewZweispieler":
            game = PauseView(self)
            self.window.show_view(game)
        if button == 9 and main.lastView == "SnakeViewZweispieler":
            game = PauseView(self)
            self.window.show_view(game)

    def setup(self):
        self.snake_coords = [[400,400],[400,350],[400,300]]
        self.snake_head = self.snake_coords[0]

        self.food_coords = [randrange(50,1200,50),randrange(50,700,50)]
        self.snake_coords2 = [[500, 500], [500, 450], [500, 400]]
        self.snake_head2 = self.snake_coords2[0]

        self.food_coords2 = [randrange(50, 1200, 50), randrange(50, 700, 50)]
        self.gameOn = True

    def on_draw(self):
        self.clear()

        if self.gameOn == False:
            arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)
            self.setup()

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)

        self.head_image.center_x = self.snake_coords[0][0]
        self.head_image.center_y = self.snake_coords[0][1]
        self.head_image.draw()

        self.food_image.center_x = self.food_coords[0]
        self.food_image.center_y = self.food_coords[1]
        self.food_image.draw()

        self.head_image2.center_x = self.snake_coords2[0][0]
        self.head_image2.center_y = self.snake_coords2[0][1]
        self.head_image2.draw()

        self.food_image2.center_x = self.food_coords2[0]
        self.food_image2.center_y = self.food_coords2[1]
        self.food_image2.draw()


        for x,y in self.snake_coords[1:]:
            self.snake_image.center_x = x;self.snake_image.center_y = y
            self.snake_image.draw()
            arcade.draw_text("Score:" + str(self.score) ,10,
                      self.window.height - 40, WHITE, font_size=30)

        for x,y in self.snake_coords2[1:]:
            self.snake_image2.center_x = x ;self.snake_image2.center_y = y
            self.snake_image2.draw()

    def game_over(self):
        main.lastGame = 2
        main.SCORE = self.score
        game = GameOverView()
        self.window.show_view(game)

    def update(self,delta_time):
        self.bug = False
        self.center_x = 0
        self.center_y = 0
        if self.joystick:
            # x-axis
            self.change_x = self.joystick.x
            # y-axis
            self.change_y = -self.joystick.y

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x == 1.0:
            print(self.center_x)

        self.center_x2 = 0
        self.center_y2 = 0
        if self.joystick2:
            # x-axis
            self.change_x2 = self.joystick2.x
            # y-axis
            self.change_y2 = -self.joystick2.y

        self.center_x2 += self.change_x2
        print(self.center_x2)
        self.center_y2 += self.change_y2
        print(self.center_y2)

        if self.center_x2 == 1.0:
            print(self.center_x2)

        if self.snake_head == self.food_coords:
            self.score += 1
            self.food_coords = [randrange(50,1200,50),randrange(50,700,50)]
            self.snake_coords.append(self.snake_coords[-1][0]+50)

        if self.snake_head2 == self.food_coords2:
            self.score += 1
            self.food_coords2 = [randrange(50,1200,50),randrange(50,700,50)]
            self.snake_coords2.append(self.snake_coords2[-1][0]+50)

        if self.center_x == 1.0:
            self.on_key_press(self,1)
        if self.center_x == -1.0:
            self.on_key_press(self,1)
        if self.center_y == 1.0:
            self.on_key_press(self,1)
        if self.center_y == -1.0:
            self.on_key_press(self,1)

        if self.center_x2 == 1.0:
            self.on_key_press(self,1)
        if self.center_x2 == -1.0:
            self.on_key_press(self,1)
        if self.center_y2 == 1.0:
            self.on_key_press(self,1)
        if self.center_y2 == -1.0:
            self.on_key_press(self,1)

        if self.moved:
            for i in range(2,len(self.snake_coords2)):
                 if self.snake_head == self.snake_coords2[i]:
                     sleep(1); self.game_over()
            for i in range(2,len(self.snake_coords)):
                 if self.snake_head == self.snake_coords[i] :
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

        if self.moved2:
            for i in range(2,len(self.snake_coords)):
                 if self.snake_head2 == self.snake_coords[i]:
                     sleep(1); self.game_over()
            for i in range(2,len(self.snake_coords2)):
                 if self.snake_head2 == self.snake_coords2[i]:
                    sleep(1);self.game_over()
            if self.snake_head2[0] < 50:
                sleep(1);self.game_over()
            elif self.snake_head2[0] > WIDTH - 50:
                sleep(1);self.game_over()
            elif self.snake_head2[1] < 50:
                sleep(1),self.game_over()
            elif self.snake_head2[1] > HEIGHT -50:
                sleep(1),self.game_over()
            else:
                self.snake_head2 = self.snake_coords2[0]
                self.new_head_position2 = [self.snake_head2[0] + self.snake_move_x2, self.snake_head2[1] + self.snake_move_y2]
                self.snake_coords2 = [self.new_head_position2] + self.snake_coords2[:-1]


    def on_key_press(self, key, _modifiers):
        print("KeyPress")

        if self.center_x2 == -1.0 or self.center_x2 == 1.0 or self.center_y2 == 1.0:
            self.moved2 = True
            self.bug2 = True
        if self.center_x2 == 1.0 and self.direction2[0] != -1:
            self.snake_move_x2 = 50
            self.snake_move_y2 = 0
            self.direction2 = [1, 0]
            self.bug2 = True

        if self.center_x2 == -1.0 and self.direction2[0] != 1:
            self.snake_move_x2 = -50
            self.snake_move_y2 = 0
            self.direction2 = [-1, 0]
            self.bug2 = True

        if self.center_y2 == 1.0 and self.direction2[1] != -1:
            self.snake_move_x2 = 0
            self.snake_move_y2 = 50
            self.direction2 = [0, 1]
            self.bug2 = True

        if self.center_y2 == -1.0 and self.direction2[1] != 1:
            self.snake_move_x2 = 0
            self.snake_move_y2 = -50
            self.direction2 = [0, -1]
            self.bug2 = True


        if self.center_x == 1.0 or self.center_x == -1.0 or  self.center_y == -1.0:
            self.moved = True
            self.bug = True
        if self.center_x == -1.0 and self.direction[0] != -1:
            self.snake_move_x = 50
            self.snake_move_y = 0
            self. direction = [1,0]
            self.bug = True

        if self.center_x == 1.0 and self.direction[0] != 1:
            self.snake_move_x = -50
            self.snake_move_y = 0
            self. direction = [-1,0]
            self.bug = True

        if self.center_y == -1.0 and self.direction[1] != -1:
            self.snake_move_x = 0
            self.snake_move_y = 50
            self.direction = [0, 1]
            self.bug = True

        if self.center_y == 1.0 and self.direction[1] != 1:
            self.snake_move_x = 0
            self.snake_move_y = -50
            self.direction = [0, -1]
            self.bug = True

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)

        if  key == arcade.key.W or key == arcade.key.A or  key == arcade.key.D:
            self.moved2 = True
            self.bug = True
        if key == arcade.key.D and self.direction2[0] != -1:
            self.snake_move_x2 = 50
            self.snake_move_y2 = 0
            self. direction2 = [1,0]
            self.bug = True

        if key == arcade.key.A  and self.direction2[0] != 1:
            self.snake_move_x2 = -50
            self.snake_move_y2 = 0
            self. direction2 = [-1,0]
            self.bug = True

        if  key == arcade.key.W and self.direction2[1] != -1:
            self.snake_move_x2 = 0
            self.snake_move_y2 = 50
            self.direction2 = [0, 1]
            self.bug = True

        if key == arcade.key.S and self.direction2[1] != 1:
            self.snake_move_x2 = 0
            self.snake_move_y2 = -50
            self.direction2 = [0, -1]
            self.bug = True
class SnakeViewEinspieler(arcade.View):
    def __init__(self):
        super().__init__()
        self.window.set_update_rate(0.15)
        joysticks = arcade.get_joysticks()
        self.background = arcade.load_texture("Pictures/GameBackground.png")
        main.lastView = "SnakeViewEinspieler"

        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)

        self.score = 0
        self.moved = None
        self.bug = None

        self.snake_image = arcade.Sprite("Pictures/SnakeVorschau.png", image_height=50, image_width=50)
        self.snake_coords = []
        self.snake_move_x = 0
        self.snake_move_y = 20

        self.head_image = arcade.Sprite("Pictures/SnakeHead.png", image_height=50, image_width=50)
        self.snake_head = None
        self.new_head_position = None
        self.direction = [0, 1]

        self.food_image = arcade.Sprite("Pictures/SnakeHead.png", image_height=50, image_width=50)
        self.food = None
        self.food_coords = []

        self.gameOn = False

        self.snake_coords_collision = []


    def on_joybutton_press(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 2 and main.lastView == "SnakeViewEinspieler":
            game = PauseView(self)
            self.window.show_view(game)

    def setup(self):
        self.snake_coords = [[400, 400], [400, 350], [400, 300]]
        self.snake_head = self.snake_coords[0]
        self.food_coords = [randrange(50, 1200, 50), randrange(50, 700, 50)]
        self.gameOn = True

    def on_draw(self):
        self.clear()

        if self.gameOn == False:
            arcade.draw_lrwh_rectangle_textured(0, 0, 1536, 864, self.background)
            self.setup()

        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, 1536, 864, self.background)

        self.head_image.center_x = self.snake_coords[0][0]
        self.head_image.center_y = self.snake_coords[0][1]
        self.head_image.draw()

        self.food_image.center_x = self.food_coords[0]
        self.food_image.center_y = self.food_coords[1]
        self.food_image.draw()

        for x, y in self.snake_coords[1:]:
            self.snake_image.center_x = x
            self.snake_image.center_y = y
            self.snake_image.draw()
            arcade.draw_text("Score:" + str(self.score) ,10,self.window.height - 40, WHITE, font_size=30)

    def game_over(self):
        main.lastGame = 1
        main.SCORE = self.score
        game = GameOverView()
        self.window.show_view(game)

    def update(self, delta_time):
        self.bug = False
        self.center_x = 0
        self.center_y = 0
        if self.joystick:
            # x-axis
            self.change_x = self.joystick.x
            # y-axis
            self.change_y = -self.joystick.y

        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.center_x == 1.0:
            print(self.center_x)

        if self.snake_head == self.food_coords:
            self.score += 1
            Score = self.score
            self.food_coords = [randrange(50, 1200, 50), randrange(50, 700, 50)]
            self.snake_coords.append(self.snake_coords[-1][0] + 50)

        if self.center_x == 1.0:
            self.on_key_press(self, 1)
        if self.center_x == -1.0:
            self.on_key_press(self, 1)
        if self.center_y == 1.0:
            self.on_key_press(self, 1)
        if self.center_y == -1.0:
            self.on_key_press(self, 1)

        if self.moved:

            for i in range(2, len(self.snake_coords)):
                if self.snake_head == self.snake_coords[i]:
                    sleep(1);
                    self.game_over()
            if self.snake_head[0] < 50:
                sleep(1);
                self.game_over()
            elif self.snake_head[0] > WIDTH - 50:
                sleep(1);
                self.game_over()
            elif self.snake_head[1] < 50:
                sleep(1), self.game_over()
            elif self.snake_head[1] > HEIGHT - 50:
                sleep(1), self.game_over()
            else:
                self.snake_head = self.snake_coords[0]
                self.new_head_position = [self.snake_head[0] + self.snake_move_x,
                                          self.snake_head[1] + self.snake_move_y]
                self.snake_coords = [self.new_head_position] + self.snake_coords[:-1]

    def on_key_press(self, key, _modifiers):

        if self.center_x == 1.0 or self.center_x == -1.0 or self.center_y == -1.0:
            self.moved = True
            self.bug = True
        if self.center_x == -1.0 and self.direction[0] != -1:
            self.snake_move_x = 50
            self.snake_move_y = 0
            self.direction = [1, 0]
            self.bug = True

        if self.center_x == 1.0 and self.direction[0] != 1:
            self.snake_move_x = -50
            self.snake_move_y = 0
            self.direction = [-1, 0]
            self.bug = True

        if self.center_y == -1.0 and self.direction[1] != -1:
            self.snake_move_x = 0
            self.snake_move_y = 50
            self.direction = [0, 1]
            self.bug = True

        if self.center_y == 1.0 and self.direction[1] != 1:
            self.snake_move_x = 0
            self.snake_move_y = -50
            self.direction = [0, -1]
            self.bug = True

        if key == arcade.key.ESCAPE:
            # pass self, the current view, to preserve this view's state
            pause = PauseView(self)
            self.window.show_view(pause)
class PongView(arcade.View):
    def __init__(self):
            super().__init__()
            main.lastView = "PongView"

            joysticks = arcade.get_joysticks()
            if joysticks:
                # Grab the first one in  the list
                self.joystick = joysticks[0]
                self.joystick2 = joysticks[1]
                self.joystick.open()
                self.joystick2.open()
                # Push this object as a handler for joystick events.
                # Required for the on_joy* events to be called.
                self.joystick.push_handlers(self)
                self.joystick2.push_handlers(self)

            self.SPEED = 5
            self.counter = 0
            self.window.set_update_rate(0.01)
            self.background = arcade.load_texture("Pictures/GameBackground.png")

            self.paddles: SpriteList = SpriteList()
            self.bot: SpriteSolidColor = SpriteSolidColor(10, 100, WHITE)
            self.right_player: SpriteSolidColor = SpriteSolidColor(10, 100, WHITE)

            self.paddles.append(self.bot)
            self.paddles.append(self.right_player)

            self.ball: SpriteCircle = SpriteCircle(10, RED)

    def on_joybutton_release(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 2 and main.lastView == "PongView":
            game = PauseView(self)
            self.window.show_view(game)

        if button == 9 and main.lastView == "PongView":
            game = PauseView(self)
            self.window.show_view(game)

    def setup(self):
            self.ball.position = self.window.width / 2, self.window.height / 2
            self.bot.position = 0 + 20, self.window.height / 2
            self.right_player.position = self.window.width - 20, self.window.height / 2

            # ball speed/direction
            self.ball.change_x = random.choice([SPEED, -SPEED])
            self.ball.change_y = random.choice([-2, -3, -4, -5, -6, -7, -8, 2, 3, 4, 5, 6, 7, 8])

            self.counter = 0

    def on_update(self, delta_time: float):
            main.lastView = "PongView"
            self.ball.update()
            self.bot.update()
            self.right_player.update()

            self.center_x = 0
            self.center_y = 0

            if self.joystick:
                # x-axis
                self.change_x = self.joystick.x
                # y-axis
                self.change_y = -self.joystick.y

            self.center_x += self.change_x
            self.center_y += self.change_y

            if self.center_x == 1.0:
                print(self.center_x)

            if self.center_x == 1.0:
                self.on_key_press(self, 1)
            if self.center_x == -1.0:
                self.on_key_press(self, 1)
            if self.center_y == 1.0:
                self.on_key_press(self, 1)
            if self.center_y == -1.0:
                self.on_key_press(self, 1)
            if self.center_y != 1.0 and self.center_y != -1.0:
                self.on_key_release(self, 1)

            # bounce ball
            if self.ball.bottom <= 0:
                self.ball.change_y *= -1
            elif self.ball.top >= self.window.height:
                self.ball.change_y *= -1

            # moving the bot
            if self.bot.position[0] != self.ball.position[0]:
                position_y = self.ball.position[1]
                position_x = self.bot.position[0]
                self.bot.set_position(position_x, position_y)

            # limit bot movement
            if self.bot.top > self.window.height:
                self.bot.top = self.window.height

            if self.bot.bottom < 0:
                self.bot.bottom = 0

            # limit Player movement
            if self.right_player.top > self.window.height:
                self.right_player.top = self.window.height

            if self.right_player.bottom < 0:
                self.right_player.bottom = 0

            # collide with paddle
            collided_paddle = self.ball.collides_with_list(self.paddles)
            if collided_paddle:
                if collided_paddle[0] is self.bot:
                    self.ball.left = self.bot.right
                    self.SPEED += .5
                    self.ball.change_x = -self.SPEED
                    print(self.SPEED)
                else:
                    self.ball.right = self.right_player.left
                    self.SPEED += .5
                    self.ball.change_x = self.SPEED
                    self.counter += 1
                    print(self.SPEED)

                # bounce ball from paddle
                self.ball.change_x *= -1

            if self.ball.left >= self.window.width:
                self.end_game()

    def on_key_press(self, symbol: int, modifiers: int):
            if symbol == arcade.key.UP:
                self.right_player.change_y = PLAYER_PADDLE_SPEED
            if symbol == arcade.key.DOWN:
                self.right_player.change_y = -PLAYER_PADDLE_SPEED
            if self.center_y == -1.0:
                self.right_player.change_y = PLAYER_PADDLE_SPEED
            if self.center_y == 1.0:
                self.right_player.change_y = -PLAYER_PADDLE_SPEED

    def on_key_release(self, _symbol: int, _modifiers: int):
            self.right_player.stop()

    def end_game(self):
        main.lastGame = 3
        main.SCORE = self.counter
        game = GameOverView()
        self.window.show_view(game)

    def on_draw(self):
            self.clear()
            arcade.draw_lrwh_rectangle_textured(0, 0, 1536, 864, self.background)

            draw_text(f'Score: {self.counter}', 40,
                      self.window.height - 50, WHITE, font_size=30)

            half_window_x = self.window.width / 2
            draw_line(half_window_x, 0, half_window_x, self.window.height, GRAY, 2)

            self.ball.draw()
            self.bot.draw()
            self.right_player.draw()
class PauseView(arcade.View):
    def __init__(self, game_view):
        super().__init__()
        self.game_view = game_view

        main.lastView = "PauseView"

        joysticks = arcade.get_joysticks()

        if joysticks:
            # Grab the first one in  the list
            self.joystick = joysticks[0]
            self.joystick2 = joysticks[1]
            self.joystick.open()
            self.joystick2.open()
            # Push this object as a handler for joystick events.
            # Required for the on_joy* events to be called.
            self.joystick.push_handlers(self)
            self.test = self.joystick2.push_handlers(self)
        self.background = arcade.load_texture("Pictures/BackgroundMenü.jpg")
    def on_joybutton_release(self, _joystick, button):
        """ Handle button-down event for the joystick """
        if button == 2 and main.lastView == "PauseView":
            self.window.show_view(self.game_view)
        if button == 9 and main.lastView == "PauseView":
            self.window.show_view(self.game_view)
    def on_update(self,delta_time):
        print("Updated")
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

        self.manager.add(arcade.gui.UIAnchorWidget(anchor_x="center_x",anchor_y="center_y",child=self.v_box))

    def resume_button(self, event):
        arcade.set_background_color(arcade.color.WHITE)
        self.window.show_view(self.game_view)
    def hauptmenue_button(self,event):
        game = MenuView()
        self.window.show_view(game)
    def on_draw(self):
        self.clear()
        arcade.draw_lrwh_rectangle_textured(0, 0,1536, 864,self.background)
        self.manager.draw()

    def on_key_press(self, key, _modifiers):
        if key == arcade.key.ESCAPE:   # resume game
            self.window.show_view(self.game_view)
def main():
    window = arcade.Window(fullscreen=True)
    menu = MenuView()
    window.show_view(menu)
    arcade.run()

if __name__ == "__main__":
    main()