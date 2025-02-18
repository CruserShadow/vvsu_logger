from exception_vvsu import VvsuException, IncorrectDataException

import requests

from requests import HTTPError
from lxml import etree
from lxml.etree import Element


class Vvsu:

    def __init__(self):
        self.__HEADERS = {"Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
                          "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0",
                          "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
                          "Referer": "https://cabinet.vvsu.ru/",
                          "Accept-Encoding": "gzip, br"}

        self.__session = requests.Session()
        self.__session.headers = self.__HEADERS

        self.URL = "https://cabinet.vvsu.ru/"

        self.__logged = False
        self.__name = None
        self.__surname = None

    def _post_data(self, link, **kwargs):
        for k in list(kwargs.keys()):
            kwargs[str(k).lstrip("_")] = kwargs.pop(k)
        return self.__session.post(link, data=kwargs)

    def _parse_fio(self, document):
        doc: Element = etree.HTML(document)
        elem = doc.xpath(".//div[@class='fio']")

        if elem:
            fio = list(elem[0])[0].text.split()
            self.__name = fio[1]
            self.__surname = fio[0]
        else:
            raise IncorrectDataException("Incorrect username or password")

    def login_into_vvsu(self, username, password):
        response = self._post_data(self.URL, user=username, _pass=password)
        response.raise_for_status()

        body = response.content.decode(response.apparent_encoding)
        try:
            self._parse_fio(body)
        except IncorrectDataException as err:
            print(err)
        else:
            self.__logged = True
            print("Logged in")

    def sign_out_vvsu(self):
        if self.__logged:
            try:
                response = self.__session.get(f"{self.URL}?logout=1")

                response.raise_for_status()
            except HTTPError as err:
                print(err, type(err))

            else:
                if "Войти в систему" in response.content.decode(response.apparent_encoding):
                    self.__session.close()
                    print("Logged out")
        else:
            print("You are not logged in")

    def get_name(self):
        return self.__name

    def get_surname(self):
        return self.__surname


if __name__ == '__main__':
    v = Vvsu()
    usr = input("Username: ")
    password = input("Password: ")

    v.login_into_vvsu(usr, password)
    v.sign_out_vvsu()
