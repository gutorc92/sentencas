# -*- coding: utf-8 -*-
import os
import re
import logging
import operator

class MissingFileSettings(Exception):
    pass


class MissingValueRequired(Exception):
    pass


class Settings(object):
    FILE_SETTINGS = "setencas.settings"

    def __init__(self, file_path=None):
        self.file_path = file_path if file_path is not None else self.find_settings_file()
        self.settings_values = {"path": "required", "init": "required"}
        self.extract_settings()


    def find_settings_file(self):
        search_paths = [
            os.path.join(os.path.dirname(os.path.realpath(__file__)), self.FILE_SETTINGS),
            os.path.join(os.path.expanduser("~"), self.FILE_SETTINGS),
            os.path.join(os.path.expanduser("~"), "..", self.FILE_SETTINGS),
            os.path.join(os.getcwd(), self.FILE_SETTINGS),
            os.path.join(os.getcwd(), "..", self.FILE_SETTINGS)
        ]
        settings_path = None
        for file_path in search_paths:
            if os.path.exists(file_path):
                settings_path = file_path
        return settings_path


    def get_setting(self, setting, line):
        regex_text = setting + ": (.*)"
        m = re.search(regex_text, line)
        if m is not None:
            return m.group(1)
        return None

    def read_settings(self):
        if self.file_path is None or not os.path.isfile(self.file_path):
            raise MissingFileSettings("O arquivo de configuracao nao foi encontrado")
        with open(self.file_path, "r") as handle:
            text = handle.read()
        return text

    def extract_settings(self):
        text = self.read_settings()
        for setting, value in self.settings_values.items():
            found = self.get_setting(setting, text)
            if value == "required" and found == None:
                raise MissingValueRequired("Setting %s not found on file %s" % (setting, self.file_path))
            self.__dict__[setting] = found


    def join(self, path, *args):
        path_all = os.path.join(self.path, path)
        for p in list(args):
            path_all = os.path.join(path_all, p)
        return path_all

    def createLogFile(self,name, logFile):
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        log_file = os.path.join(self.path, "log", logFile)
        print("log file", log_file)
        handler = logging.FileHandler(log_file)
        handler.setFormatter(formatter)
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handlers = logger.handlers[:]
        for h in handlers:
            h.close()
            logger.removeHandler(h)        
        logger.addHandler(handler)

        return logger

    def getLastFile(self, dir_="log"):
        dir_path = os.path.join(self.path, dir_)
        dict_dir = {}
        for filename in os.listdir(dir_path):
            dict_dir[filename] = os.stat(os.path.join(dir_path, filename)).st_mtime

        return sorted(dict_dir.items(), key=operator.itemgetter(1), reverse=True)[0][0]

    def replace_settings(self, setting, value):
        setting = "(" + setting +  ")" + " (\d+)"
        print(setting)
        text = ""
        with open(self.file_path, "r") as handle:
            text = handle.read()
        text = re.sub(setting, r"\1 " + value, text)
        with open(self.file_path, "w") as handle:
            handle.write(text)

