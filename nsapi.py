# coding=utf-8
from collections import defaultdict
from lxml import etree
import urllib2
import base64
import datetime

__author__ = 'boisei0 <boisei0@hubsec.eu>'


class NSAPI:
    def __init__(self, api_username, api_password):
        self.auth = base64.encodestring('{}:{}'.format(api_username, api_password)).replace('\n', '')

    def _request(self, url):
        req = urllib2.Request(url)
        req.add_header('Authorization', 'Basic {}'.format(self.auth))
        return urllib2.urlopen(req)

    def get_stations_list(self):
        # stations = defaultdict(str)
        stations = dict()
        r = self._request('http://webservices.ns.nl/ns-api-stations-v2')
        root = etree.XML(r.read())

        for i in range(len(root)):
            names = []
            station_code = root[i][0].text
            for j in range(len(root[i][2])):
                names.append(root[i][2][j].text)
            try:
                for j in range(len(root[i][7])):
                    names.append(root[i][7][j].text)
            except (IndexError, KeyError):
                pass

            stations[station_code] = StationModel(station_code, root[i][3].text, root[i][4].text,
                                                  root[i][5].text, root[i][6].text, names=names)
        return stations

    def get_travel_advice(self, station_from, station_to):
        reis_advies = list()
        station_from = station_from.replace(' ', '+')
        station_to = station_to.replace(' ', '+')
        url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation={0}&toStation={1}'.format(station_from,
                                                                                                  station_to)
        r = self._request(url)
        root = etree.XML(r.read())

        for i in range(len(root)):
            geplande_vertrek_tijd = ''
            actuele_vertrek_tijd = ''
            geplande_aankomst_tijd = ''
            actuele_aankomst_tijd = ''
            for j in range(len(root[i])):
                if root[i][j].tag == 'GeplandeVertrekTijd':
                    geplande_vertrek_tijd = root[i][j].text
                elif root[i][j].tag == 'ActueleVertrekTijd':
                    actuele_vertrek_tijd = root[i][j].text
                elif root[i][j].tag == 'GeplandeAankomstTijd':
                    geplande_aankomst_tijd = root[i][j].text
                elif root[i][j].tag == 'ActueleAankomstTijd':
                    actuele_aankomst_tijd = root[i][j].text
            reis_advies.append(ReisModel(station_from, station_to, geplande_vertrek_tijd, actuele_vertrek_tijd,
                                         geplande_aankomst_tijd, actuele_aankomst_tijd))
        return reis_advies


class StationModel:
    def __init__(self, code, country, uic, lat, lon, names=list()):
        self.code = code
        self.names = names
        self.country = country
        self.uic = uic
        self.lat = lat
        self.lon = lon

    def __repr__(self):
        return self.names


class ReisModel:
    def __init__(self, station_from, station_to, geplande_vertrek_tijd, actuele_vertrek_tijd, geplande_aankomst_tijd,
                 actuele_aankomst_tijd):
        self.station_from = station_from.replace('+', ' ')
        self.station_to = station_to.replace('+', ' ')
        self.geplande_vertrek_tijd = geplande_vertrek_tijd
        self.actuele_vertrek_tijd = actuele_vertrek_tijd
        self.geplande_aankomst_tijd = geplande_aankomst_tijd
        self.actuele_aankomst_tijd = actuele_aankomst_tijd

    def heeft_vertraging(self):
        ts_gvt = self._datetime_string_to_timestamp(self.geplande_vertrek_tijd)
        ts_avt = self._datetime_string_to_timestamp(self.actuele_vertrek_tijd)
        ts_gat = self._datetime_string_to_timestamp(self.geplande_aankomst_tijd)
        ts_aat = self._datetime_string_to_timestamp(self.actuele_aankomst_tijd)

        vertraging_voor = (ts_avt - ts_gvt).total_seconds() / 60
        vertraging_eind = (ts_aat - ts_gat).total_seconds() / 60

        if vertraging_voor > 0 or vertraging_eind > 0:
            return True, vertraging_voor, vertraging_eind
        else:
            return False, vertraging_voor, vertraging_eind

    def __repr__(self):
        return '<ReisModel {}>'.format(self.geplande_vertrek_tijd)

    @staticmethod
    def _datetime_string_to_timestamp(dt_string):
        return datetime.datetime.strptime(dt_string[:-5], '%Y-%m-%dT%H:%M:%S')