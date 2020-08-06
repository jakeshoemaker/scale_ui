import serial
import io
import clipboard
from threading import Thread
import kivy
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout   
from kivy.clock import Clock
from kivy.uix.screenmanager import Screen, ScreenManager, FadeTransition
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.properties import StringProperty, ObjectProperty, NumericProperty

class ScaleScreen(Screen):
    intialized = False
    weight_btn = ObjectProperty(None)
    zero_btn = ObjectProperty(None)
    calib_btn = ObjectProperty(None)
    display_text = StringProperty("Scale Weight")
    

    def worker(self):
        Clock.schedule_interval(lambda dt: self.update_weight(), .5)
    
    def connect_btn(self):
        t = Thread(target=self.worker)
        t.start()

    def update_weight(self):
        self.talk_to_scale('H')
    
    def weight_btn(self):
         # copy weight to clipboard and ignore the weird byte in front
         clipboard.copy(self.display_text[1:])
         # print("Copied to clipboard")
 
    def zero_btn(self):
        print("zero clicked")
        self.talk_to_scale('Z')

    def calib_btn(self):
        print("calib clicked")
        self.display_text = "calibrate scale was clicked"

    # send a serial request to get the scale information
    def talk_to_scale(self, letter):
        if (self.intialized == True):
            ser.write(bytes(letter, "utf-8"))
            self.display_text = (str(ser.read(8).decode("utf-8")))
        else:
            intialized = True
            settings = self.manager.get_screen('settings')
            ser = serial.Serial(port =str(settings.port), baudrate= int(settings.baudrate),
                           bytesize=int(settings.bytesize), timeout=.5, stopbits=1, parity='N')

            ser.write(bytes(letter, "utf-8"))
            self.display_text = (str(ser.read(8).decode("utf-8")))
        


class SettingsScreen(Screen):
    port = StringProperty("COM18")
    baudrate = NumericProperty(9600)
    bytesize = NumericProperty(8)
    stop_bits = NumericProperty(1)
    timeout = NumericProperty(0)
    parity = StringProperty("None")
    status = StringProperty("Not Saved")

    def save_btn(self):
        self.status = "Saved!"
        

class WindowManager(ScreenManager):
    pass

class ScaleApp(App): # <- Main Class
    def build(self):
        sm = WindowManager()
        sm.add_widget(ScaleScreen(name="main"))
        sm.add_widget(SettingsScreen(name="settings"))
        return sm

ScaleApp().run()