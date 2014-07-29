import kivy
kivy.require('1.8.0')

from kivy.app import App
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout

__author__ = 'boisei0'


class TrajectInfoCore(BoxLayout):
    from_field = ObjectProperty()
    to_field = ObjectProperty()

    def __init__(self, **kwargs):
        super(TrajectInfoCore, self).__init__(**kwargs)

    def get_delay_info(self):
        app = App.get_running_app()
        form_box = self.ids['form_box'].__self__
        travel_advice = app.api.get_travel_advice(form_box.children[1].text, form_box.children[3].text)
        for advice in travel_advice:
            heeft_vertraging, voor, na = advice.heeft_vertraging()
            if heeft_vertraging:
                print('De trein van {} naar {} van {} heeft {} minuten vertraging'.format(advice.station_from,
                                                                                          advice.station_to,
                                                                                          advice.geplande_vertrek_tijd,
                                                                                          voor))