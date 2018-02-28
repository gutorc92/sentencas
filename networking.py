import subprocess

import os
import psutil
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from stem import Signal
from stem.control import Controller

from utils import Singleton
import platform

class ProxedHTTPRequester(metaclass=Singleton):
    def __init__(self):
        self.__start_proxies()
        self.__proxies = {"http": "127.0.0.1:8118", "https": "127.0.0.1:8118"}
        user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
        self.__headers = {'User-Agent': user_agent}
        #self.__renew_connection()
        self.session = self.__get_new_session()

    def head(self, url):
        session = self.__get_new_session()
        html = session.head(url, proxies=self.__proxies, headers=self.__headers)
        session.close()
        return html

    def get(self, url):
        return self.__request(url)

    def __start_proxies(self):
        _TaskManager().init_tor()
        _TaskManager().init_privoxy()

    def __request(self, url):
        html = self.session.get(url, proxies=self.__proxies, headers=self.__headers)
        return html

    def __get_new_session(self):
        session = requests.Session()
        adapter = HTTPAdapter(max_retries=Retry(connect=30, backoff_factor=1))
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        return session

    def __renew_connection(self):
        with Controller.from_port(port=19051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
            controller.close()

    def end(self):
        _TaskManager().close()

    def close(self):
        self.session.close()




class _TaskManager(metaclass=Singleton):
    def __init__(self):
        self.__tor = None
        self.__privoxy = None
        self.dir_ = os.path.dirname(os.path.abspath(__file__))

    def close(self):
        self.end_privoxy()
        self.end_tor()

    def checkIfTaskRunning(self, task_name):
        task_names = set([it.name() for it in psutil.process_iter()])
        return task_name in task_names

    @property
    def is_tor_running(self):
        return self.checkIfTaskRunning("tor") or self.checkIfTaskRunning("tor.exe")

    @property
    def is_privoxy_running(self):
        return self.checkIfTaskRunning("privoxy.exe") or self.checkIfTaskRunning("privoxy")

    def init_tor(self):
        if not self.is_tor_running:
            self.start_tor()

    def start_tor(self):
        prog = "tor.exe" if platform.system() == "Windows" else "tor"
        self.__tor = subprocess.Popen(
            [prog, "-f", os.path.join(self.dir_,"thirdpartsprocs", "Tor","Data",  "Tor", "torrc")], shell=True
        )

    def init_privoxy(self):
        if not self.is_privoxy_running:
            self.start_privoxy()

    def start_privoxy(self):
        prog = "privoxy.exe" if platform.system() == "Windows" else "privoxy"
        self.__privoxy = subprocess.Popen(
            [prog], shell=True
        )

    def end_tor(self):
        if self.is_tor_running:
            self.close_tor()

    def close_tor(self):
        if self.__tor is not None:
            self.__tor.terminate()

    def end_privoxy(self):
        if self.is_privoxy_running:
            self.close_privoxy()

    def close_privoxy(self):
        if self.__privoxy is not None:
            self.__privoxy.terminate()

