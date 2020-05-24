# import fdb
# import tkinter as tk
import data_processing
import configparser
import GUI
import os
import winpath
from tkinter import messagebox

class SettingManager(object):
    config = None

    def __init__(self):
        self.config = configparser.ConfigParser()
        try:
            self.read_config()
        except FileNotFoundError:
            self.populate_with_defaults()

            GUI.settings(self.config)

            self.write_config()

    def populate_with_defaults(self):
        self.config['DATABASE'] = {
            'host': '127.0.0.1',
            'port': '3050',
            'database': 'C:\\FAKT95',
            'user': 'sysdba',
            'password': 'masterkey',
            'charset': 'UTF8'
        }

        self.config['splits'] = {
            'splits': str([180, 90, 60, 30, 0]),
        }

        self.config['other'] = {
            'output_file': os.path.join(winpath.get_desktop(), 'Zestawienie'),
            'id_firmy': '1',
            'to_date': '',
            'open_file': '1',
        }

    def get_connection_arg(self):
        connection_arg = dict(self.config['DATABASE'])
        connection_arg['port'] = int(connection_arg['port'])
        padded_id_firmy = self.config['other']['id_firmy'].zfill(4)
        connection_arg['database'] = "".join([connection_arg['database'], "\\", padded_id_firmy, "\\", padded_id_firmy, "baza.fdb"])
        return connection_arg

    def get_split_list(self):
        splits = self.config['splits']['splits'].strip('[]').split(',')
        if splits == [""]:
            return []
        splits = sorted(list(map(int, splits)), reverse=True)
        return splits

    def read_config(self):
        with open('config.ini', 'r') as configfile:
            self.config.read_file(configfile)

    def write_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


settings_manager = SettingManager()


def create_split_labels(split_list):
    prev = "+"
    split_labels = []
    for idx in range(len(split_list)):
        current_label = str(split_list[idx])
        split_labels.append(current_label + prev)
        prev = "-" + current_label
    return split_labels


def execute(switch: bool):
    try:
        date = settings_manager.config['other']['to_date']
        connection_args = settings_manager.get_connection_arg()
        query = data_processing.render_query(switch, to_date=date)
        header, data = data_processing.read_database(connection_args, query)
        splits = settings_manager.get_split_list()
        podzielone_dane = data_processing.split_data(data, splits)
        output_filename = settings_manager.config['other']['output_file']
        split_labels = create_split_labels(splits)
        data_processing.write_to_spreadsheet(output_filename, header, podzielone_dane, split_labels)
    except Exception(BaseException):
        messagebox.showerror("Error", "Klient FireBird nie jest zainstalowany")
    except PermissionError:
        messagebox.showerror("Error", "Próba wygenerowania zestawienia, gdy jest już otwarte")
    except OSError(Exception):
        messagebox.showerror("Error", "Wymagany program do otwierania plików z rozszerzeniem .xls")

    if settings_manager.config['other'].getboolean('open_file'):
       os.startfile(output_filename + ".xls")


if __name__ == "__main__":
    GUI.lobby()
