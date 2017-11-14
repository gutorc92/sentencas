# -*- coding: utf-8 -*-
import os
import time
import codecs
import re
import getpass


class MissingFileSettings(Exception):
    pass


class MissingValueRequired(Exception):
    pass


class Settings(object):
    FILE_SETTINGS = "setencas.settings"

    def __init__(self, file_path=None):
        self.file_path = file_path if file_path is not None else self.find_settings_file()
        self.settings_values = {"path": "required"}

    def find_settings_file(self):
        uritools_dir = os.path.dirname(os.path.realpath(__file__))
        file_settings = os.path.join(uritools_dir, self.FILE_SETTINGS)
        if os.path.isfile(file_settings):
            return file_settings
        uritools_dir = os.path.expanduser("~")
        file_settings = os.path.join(uritools_dir, self.FILE_SETTINGS)
        if os.path.isfile(file_settings):
            return file_settings
        file_settings = os.path.join(uritools_dir, "..", self.FILE_SETTINGS)
        if os.path.isfile(file_settings):
            return file_settings
        file_settings = os.path.join(os.getcwd(), self.FILE_SETTINGS)
        if os.path.isfile(file_settings):
            return file_settings
        file_settings = os.path.join(os.getcwd(), "..", self.FILE_SETTINGS)
        if os.path.isfile(file_settings):
            return file_settings
        else:
            return None


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




