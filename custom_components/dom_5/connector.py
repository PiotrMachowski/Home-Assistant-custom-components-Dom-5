from datetime import timedelta

from homeassistant.util import Throttle
import logging
from typing import Any, List, Optional

import requests
import html2text

from requests import Response, Session

_LOGGER = logging.getLogger(__name__)

THROTTLE_INTERVAL = timedelta(minutes=30)


def test_connection(url: str, username: str, password: str) -> bool:
    sensor = Dom5Connector(url, username, password)
    return sensor.test_connection()


class Dom5Data:
    messages_number: Optional[int]
    last_messages_titles: Optional[List[str]]
    last_message_id: Optional[str]
    last_message_title: Optional[str]
    last_message_body: Optional[str]
    last_message_date: Optional[str]
    announcements_number: Optional[int]
    last_announcements_titles: Optional[List[str]]
    last_announcement_id: Optional[str]
    last_announcement_title: Optional[str]
    last_announcement_body: Optional[str]
    last_announcement_date: Optional[str]
    arrear: Optional[float]
    overpayment: Optional[float]
    balance: Optional[float]

    def __init__(self):
        self.messages_number = None
        self.last_messages_titles = None
        self.last_message_id = None
        self.last_message_title = None
        self.last_message_body = None
        self.last_message_date = None
        self.announcements_number = None
        self.last_announcements_titles = None
        self.last_announcement_id = None
        self.last_announcement_title = None
        self.last_announcement_body = None
        self.last_announcement_date = None
        self.arrear = None
        self.overpayment = None
        self.balance = None

    def set_messages(self, messages_response: Response):
        if not Dom5Data.is_valid(messages_response):
            return
        self.messages_number, self.last_message_id, self.last_messages_titles = \
            Dom5Data.parse_communications(messages_response.json())

    def set_last_message(self, last_message_response: Response):
        if not Dom5Data.is_valid(last_message_response):
            return
        self.last_message_title, self.last_message_body, self.last_message_date = \
            Dom5Data.parse_specific_communication(last_message_response.json())

    def set_announcements(self, announcements_response: Response):
        if not Dom5Data.is_valid(announcements_response):
            return
        self.announcements_number, self.last_announcement_id, self.last_announcements_titles = \
            Dom5Data.parse_communications(announcements_response.json())

    def set_last_announcement(self, last_announcement_response: Response):
        if not Dom5Data.is_valid(last_announcement_response):
            return
        self.last_announcement_title, self.last_announcement_body, self.last_announcement_date = \
            Dom5Data.parse_specific_communication(last_announcement_response.json())

    def set_finances(self, finances_response: Response):
        if not Dom5Data.is_valid(finances_response):
            return
        json = finances_response.json()["data"]
        self.arrear = json["Zaleglosci"]
        self.overpayment = json["Nadplaty"]
        self.balance = self.overpayment - self.arrear

    @staticmethod
    def is_valid(response: Response):
        return response.status_code == 200 and "status" in response.json() and response.json()["status"] == "success"

    @staticmethod
    def parse_communications(json: Any):
        communications_number = len(json["data"])
        last_communication_id = None if communications_number == 0 else json["data"][0]["Ident"]
        last_titles = list(map(lambda r: r["Tytul"], json["data"]))[0:10]
        return communications_number, last_communication_id, last_titles

    @staticmethod
    def parse_specific_communication(json: Any):
        title = json["data"]["Tytul"]
        message = html2text.html2text(json["data"]["Tresc"])
        date = json["data"]["Data"]
        return title, message, date


class Dom5Connector:
    data: Optional[Dom5Data]

    def __init__(self, url: str, username: str, password: str):
        self._base_url = url
        self._username = username
        self._password = password
        self.data = Dom5Data()
        self.update = Throttle(THROTTLE_INTERVAL)(self._update)

    @property
    def url(self) -> str:
        return self._base_url

    @property
    def username(self) -> str:
        return self._username

    def _update(self):
        session = self._login()
        if session is None:
            _LOGGER.error('Failed to login')
            return
        try:
            data = Dom5Data()
            messages_response = session.get(self._url('/iokEwid/DajKorespPoz'), verify=False)
            data.set_messages(messages_response)
            if data.last_message_id is not None:
                last_message_response = session.get(
                    self._url(f'/iokEwid/DajSzczegKorespPoz?Ident={data.last_message_id}'), verify=False)
                data.set_last_message(last_message_response)
            announcements_response = session.get(self._url('/iok/DajOgloszenia'), verify=False)
            data.set_announcements(announcements_response)
            if data.last_announcement_id is not None:
                last_announcement_response = session.get(
                    self._url(f'/iok/DajOgloszenie?Ident={data.last_announcement_id}'), verify=False)
                data.set_last_announcement(last_announcement_response)
            finances_response = session.get(self._url('/iokRozr/DajListeRozrachFin'), verify=False)
            data.set_finances(finances_response)
            self.data = data
        finally:
            self._logout(session)

    def _login(self) -> Optional[Session]:
        session = requests.session()
        login = session.post(url=self._url('/iok/Zaloguj'),
                             data={"Ident": self._username, "Haslo": self._password},
                             headers={"Referer": self._url("/content/InetObsKontr/login")},
                             verify=False)
        if Dom5Data.is_valid(login):
            return session
        return None

    def _logout(self, session: Session):
        session.post(self._url('/iok/Wyloguj'), verify=False)

    def _url(self, path: str):
        return f'{self._base_url}{path}'

    def test_connection(self) -> bool:
        session = self._login()
        if session is not None:
            self._logout(session)
            return True
        return False
