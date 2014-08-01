import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button

__author__ = 'boisei0'


class TrajectInfoCore(BoxLayout):
    from_field = ObjectProperty()
    to_field = ObjectProperty()
    stations = ListProperty()

    def __init__(self, **kwargs):
        super(TrajectInfoCore, self).__init__(**kwargs)
        self.app = App.get_running_app()
        self.stations = self.app.stations

        stations_names = sorted([self.app.stations[code].names[-1] for code in self.app.stations.keys()])

        stations_list_from = [Button(text=unicode(name), size_hint_y=None, height=30) for name in stations_names]
        stations_list_to = [Button(text=unicode(name), size_hint_y=None, height=30) for name in stations_names]

        self.ids['from_field'].__self__.on_options(None, sorted(stations_list_from))
        self.ids['to_field'].__self__.on_options(None, sorted(stations_list_to))

    def get_delay_info(self):
        form_box = self.ids['form_box'].__self__
        station_from = form_box.children[3].text
        station_to = form_box.children[1].text
        travel_advice = self.app.api.get_travel_advice(station_from, station_to)
        for advice in travel_advice:
            heeft_vertraging, voor, na = advice.heeft_vertraging()
            if heeft_vertraging:
                print('De trein van {0.station_from} naar {0.station_to} van {0.geplande_vertrek_tijd} heeft bij '
                'vertrek {1} minuten vertraging en op bestemming {2} minuten vertraging'.format(advice, int(voor),
                                                                                               int(na)))