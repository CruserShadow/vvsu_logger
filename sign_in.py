import requests
import re
import lxml
import time

class Vvsu:

    def __init__(self):
        self.user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
        self.session = requests.Session()

        self.session.headers["User-Agent"] = self.user_agent
        print(self.session.headers)

        self.URL = "https://cabinet.vvsu.ru/"
        self.username = ""
        self.password = ""

    def set_login(self, username):
        self.username = username

    def set_password(self,password):
        self.password = password

    def login(self, username=None, password=None):
        response = self.session.post(self.URL, data={"user": username, "pass": password})
        body = response.content.decode(response.apparent_encoding)

        if re.search("http://students.vvsu.ru/education/stud", body) is not None:
            print("Success")
        else:
            print("Incorrect pass or username")

        #print(response.request.headers)

    def log_out(self):
        logout = self.session.get("https://cabinet.vvsu.ru/?logout=1")

        #print(logout.content.decode(logout.apparent_encoding))


#https://cabinet.vvsu.ru/?logout=1


if __name__ == '__main__':
    v = Vvsu()
    username = input("username: ")
    password = input("password: ")

    v.login(username, password)
    v.log_out()