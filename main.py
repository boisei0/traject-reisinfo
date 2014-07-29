import kivy
kivy.require('1.8.0')

from kivy.app import App
from trajectinfo import TrajectInfoCore
from nsapi import NSAPI

__author__ = 'boisei0'
__appname__ = 'Traject Reisinformatie'


class TrajectInfoApp(App):
    def __init__(self, ns_username, ns_password):
        super(TrajectInfoApp, self).__init__()

        self.window = None
        self.api = NSAPI(ns_username, ns_password)
        self.stations = self.api.get_stations_list()

    def build(self):
        from kivy.base import EventLoop
        self.window = EventLoop.ensure_window()
        self.title = __appname__

        return TrajectInfoCore()


if __name__ == '__main__':
    TrajectInfoApp('NS USERNAME', 'NS PASSWORD').run()