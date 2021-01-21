import os
import sys


class Utilities:
    def str_to_ascii(self, text):
        str_to_asc_list = []
        for i in text:
            a = ord(i)
            str_to_asc_list.append(a)
        return str_to_asc_list

    def ascii_to_str(self, asciiList):
        text_from_ascii = ""
        for i in asciiList:
            text_from_ascii += (chr(i))
        return text_from_ascii

    def calculateTime(self, start_time, end_time):
        return round(end_time - start_time, 4)

    def resource_path(self, relative_path):
        """ Get absolute path to resource, works for dev and for PyInstaller """

        try:
            # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)


utilities = Utilities()
