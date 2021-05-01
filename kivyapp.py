from kivy.config import Config
from screeninfo import get_monitors
m = get_monitors()[0]
smaller_d = m.width if m.width <= m.height else m.height
smaller_d = int(0.85 * smaller_d)
Config.set('graphics', 'height', smaller_d)
Config.set('graphics', 'width', smaller_d)

Config.set('graphics', 'resizable', False)
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.graphics import *
from kivy.core.window import Window
from kivy.app import App
from typing import Literal, Union, Optional, List

# m = get_monitors()[0]
#
# smaller_d = m.width if m.width <= m.height else m.height
# smaller_d = int(0.85*smaller_d)
# Config.setdefault('graphics', 'width', smaller_d)
# Config.setdefault('graphics', 'height', smaller_d)
# Config.setdefault('graphics', 'resizable', False)
# Config.write()
# Window.size = (smaller_d, smaller_d)

sm = ScreenManager(transition=FadeTransition())
text_Size = 25

class _Player:
    def __init__(self, name: str, sign: Literal['x', 'o']) -> None:
        self.playerMarks = ""
        self.name = name
        self.sign = sign
class PageTowGridLayout():

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = GridLayout(cols=3)
        layout.add_widget(Button(text='1'))
        layout.add_widget(Button(text='2'))
        layout.add_widget(Button(text='4'))
        layout.add_widget(Button(text='5'))
        layout.add_widget(Button(text='6'))
        layout.add_widget(Button(text='7'))
        layout.add_widget(Button(text='8'))
        layout.add_widget(Button(text='9'))


class PageTowRelativelayout(RelativeLayout):
    def __init__(self, **kw):
        super().__init__(**kw)


class PageOneFloatLayout(FloatLayout):
    def __init__(self):
        super(PageOneFloatLayout, self).__init__()
        
        self.add_widget(Label(text="first player", size_hint=(.3, .1),
                              pos_hint={"x": .05, "y": .7}, font_size=text_Size))

        self.add_widget(Label(text="second player", size_hint=(.3, .1),
                              pos_hint={"x": .05, "y": .59}, font_size=text_Size))

        self.edt1 = TextInput(font_size=text_Size, text="", hint_text="player name", size_hint=(.3, .05),
                              pos_hint={"x": .4, "y": .725})
        self.edt2 = TextInput(font_size=text_Size, text="", hint_text="player name", size_hint=(.3, .05),
                              pos_hint={"x": .4, "y": .62})

        self.StartGameBtn = Button(font_size=text_Size, text="start game", size_hint=(.3, .1),
                                   pos_hint={"x": .4, "y": .45}, on_press=self.on_press_startgame)
        self.toggle1 = ToggleButton(text="x", group="firstplayer", state="down", font_size=text_Size,
                                    size_hint=(.05, .05),
                                    pos_hint={"x": .75, "y": .725}, on_press=self.on_state_toggle1)
        self.toggle2 = ToggleButton(text="o", group="firstplayer", font_size=text_Size,
                                    size_hint=(.05, .05),
                                    pos_hint={"x": .825, "y": .725}, on_press=self.on_state_toggle2)
        self.toggle3 = ToggleButton(text="x", group="secondplayer", state="normal", font_size=text_Size,
                                    size_hint=(.05, .05),
                                    pos_hint={"x": .75, "y": .62}, on_press=self.on_state_toggle3)
        self.toggle4 = ToggleButton(text="o", group="secondplayer", font_size=text_Size,state="down",
                                    size_hint=(.05, .05), pos_hint={"x": .825, "y": .62},
                                    on_press=self.on_state_toggle4)
        self.add_widget(self.edt1)
        self.add_widget(self.edt2)
        self.add_widget(self.StartGameBtn)
        self.add_widget(self.toggle1)
        self.add_widget(self.toggle2)
        self.add_widget(self.toggle3)
        self.add_widget(self.toggle4)

    def on_press_startgame(self, value):
        if all([self.edt1.text != "", self.edt2.text != "",
                any([True if self.toggle1.state == "down" else False,
                     True if self.toggle2.state == "down" else False]),
                any([True if self.toggle3.state == "down" else False,
                     True if self.toggle4.state == "down" else False])
                ]):

            self.player1 = _Player(self.edt1.text,
                                   self.toggle1.text if self.toggle1.state=="down" else self.toggle2.text)

            self.player2 = _Player(self.edt2.text,
                                   self.toggle3.text if self.toggle3.state == "down" else self.toggle4.text)
            self.turn = turn = self.player1
            self.xo_map = {k: None for k in range(1, 10)}
            sm.current = "2"
            mainlayout = RelativeLayout()
            layout = GridLayout(cols=3)
            for i in range(1,10):
                self.xoTableBtn = Button(text=str(i),on_press=self.on_press_xoTable)
                layout.add_widget(self.xoTableBtn)
            layout.size_hint = (1,.9)
            self.lb = Label(text=f"it's {turn.name} turn", size_hint=(.1, .1),
                            pos_hint={"x": .1, "y": .9}, font_size=text_Size)
            mainlayout.add_widget(layout)
            mainlayout.add_widget(self.lb)
            sm.get_screen("2").add_widget(mainlayout)

        else:
            print("fuck it")
            pass

    def _calculate_result(self) -> str:
        print("calcute")
        win_list = ["123", "456", "789", "147", "258", "369", "159", "357"]
        for item in win_list:
            value_list = [self.xo_map[int(index)] for index in item if self.xo_map[int(index)]]

            if "".join(value_list) == "xxx" or "".join(value_list) == "ooo":
                return "".join(value_list)[0]  # change true and false to player sign
        return ""  # bool(empty str) == False

    def winner(self):  # -> Optional[_Player]:
        res = self._calculate_result()  # res = 'x' or res = 'o' or res = ''
        # if not res and None in self.table.xo_map.values():  # check winner before end game round raise Exception
        #     raise self.UnFinishedGameError("The Game has not Finished yet!...")
        if res:  # if res != ''
            return self.player1 if res == self.player1.sign else self.player2  # find winner player sign
        elif not res and None not in self.xo_map.values():
            return None
        return False

    def on_press_xoTable(self,value):
        if value.text != "x" and value.text != "o":
            print("oops")
            self.xo_map[int(value.text)] = self.turn.sign
            value.text = self.turn.sign
            self.turn.playerMarks = self.turn.playerMarks + value.text
            print(self.winner())
            if self.winner()!= False:
                print(self.winner().name)
                sm.current = "3"
                sm.get_screen("3").add_widget(Label(text=f"{self.turn.name} wins game", size_hint=(.3, .1),
                                      pos_hint={"x": .4, "y": .6}, font_size=40))

                self.gotomain = Button(font_size=text_Size, text="start game", size_hint=(.3, .1),
                                        pos_hint={"x": .4, "y": .45}, on_press=self.on_press_gotomain)
                sm.get_screen("3").add_widget(self.gotomain)

            self.turn = self.player1 if self.turn == self.player2 else self.player2
            self.lb.text = f"it's {self.turn.name} turn"

    def on_press_gotomain(self, value):
        sm.current ="1"
        sm.clear_widgets("3")

    def on_state_toggle1(self, value):
        print(value)
        self.toggle4.state = "down"
        self.toggle3.state = "normal"

    def on_state_toggle2(self, value):
        print(value)
        self.toggle4.state = "normal"
        self.toggle3.state = "down"

    def on_state_toggle3(self, value):
        print(value)
        self.toggle1.state = "normal"
        self.toggle2.state = "down"

    def on_state_toggle4(self, value):
        print(value)
        self.toggle1.state = "down"
        self.toggle2.state = "normal"


class MyApp(App):
    def __init__(self):
        super(MyApp, self).__init__()
    def build(self):
        self.title = "XO Game"
        sm.add_widget(Screen(name="1"))
        sm.add_widget(Screen(name="2"))
        sm.add_widget(Screen(name="3"))
        sm.get_screen("1").add_widget(PageOneFloatLayout())
        sm.current = "1"
        return sm


if __name__ == "__main__":
    theApp = MyApp()
    theApp.run()
