import time
from fastcore.basics import true
import keyboard
from ahk import AHK, keys
from pynput.keyboard import Controller as Cont
from pynput.keyboard import Key
import pyautogui
from pywinauto import application
from win32gui import GetWindowText, GetForegroundWindow


class Controller:
    def __init__(self):
        self.key_inputs = [
            "left",
            "right",
            "space",
        ]
        self.ahk = AHK()
        self.controller = Cont()
        self.controller.press(Key.space)
        self.previous_key = []

    def start_program_func(self, function, key="q"):
        keyboard.add_hotkey(key, function)

    def movement_state(self):
        keys_pressed = []
        for key in self.key_inputs:
            if keyboard.is_pressed(key):
                keys_pressed.append(key)
        if len(keys_pressed) == 0:
            keys_pressed.append("nothing")  # Enough data on doing nothing
        return keys_pressed

    # Was not as reliable as using pywinauto
    # def display_game(self, x, y, width, height):
    #     roblox_window = self.ahk.find_window_by_title(
    #         title=b'Roblox', exact=True)
    #     print(roblox_window.title)
    #     roblox_window.move(x, y, width, height)
    #     roblox_window.minimize()
    #     roblox_window.restore()
    #     #roblox_window.always_on_top = True

    # Bring the game window to the front and reposition
    def display_game(self, window_x, window_y, window_width, window_height):
        window_x_offset = 10
        try:
            app = application.Application()
            app.connect(title_re="Roblox")
            app_dialog = app.top_window()
            if app_dialog.exists() and GetWindowText(GetForegroundWindow()) != "Roblox":
                app_dialog.minimize()
                app_dialog.restore()
                app_dialog.active()

            app_dialog.move_window(
                x=window_x - window_x_offset, y=window_y, width=window_width, height=window_height, repaint=True)
        except Exception as e:
            print(e)

    def move_test(self):
        print("start")
        # keyboard.press("space")
        # keyboard.press("Left")
        #self.ahk.key_down("left", False)
        # keyboard.send("left,space,right")
        time.sleep(1)
        print("end")

    def move_player(self, predictions):
        if predictions == "nothing":
            return

        # self.ahk.key_up(self.previous_key)

        # self.ahk.key_down(predictions)

        # self.previous_key = predictions

        for key in self.previous_key:
            if key == "space":
                keyboard.release(key)
            else:
                self.ahk.key_release(key, blocking=False)
        self.previous_key = []

        key_press = []
        options = ["left", "nothing", "right", "space"]
        for i in range(len(predictions)):
            if predictions[i] > 0.45:
                if options[i] == "nothing":
                    continue
                key_press.append(options[i])
        if len(key_press) == 0:
            return
        for key in key_press:
            if key == "space":
                keyboard.press(key)
            else:
                self.ahk.key_down(key, blocking=False)
        self.previous_key = key_press

        # for key in key_press:
        #     self.ahk.key_down(key)
        # time.sleep(0.1)
        # for key in key_press:
        #     self.ahk.key_release(key)
