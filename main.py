import fdb
import tkinter as tk
import data_processing
import configparser
import GUI


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
            'output_file': 'Spreadsheet',
            'id_firmy': '1',
        }

    def get_connection_arg(self):
        connection_arg = dict(self.config['DATABASE'])
        connection_arg['port'] = int(connection_arg['port'])
        padded_id_firmy = self.config['other']['id_firmy'].zfill(4)
        connection_arg['database'] = "".join([connection_arg['database'], "\\", padded_id_firmy, "\\", padded_id_firmy, "baza.fdb"])
        return connection_arg

    def get_split_list(self):
        splits = self.config['splits']['splits'].strip('[]').split(',')
        splits = sorted(list(map(int, splits)), reverse=True)
        return splits

    def read_config(self):
        with open('config.ini', 'r') as configfile:
            self.config.read_file(configfile)

    def write_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


settings_manager = SettingManager()


def execute(switch: bool):
    connection_args = settings_manager.get_connection_arg()
    query = data_processing.render_query(switch)
    header, data = data_processing.read_database(connection_args, query)
    podzielone_dane = data_processing.split_data(data, settings_manager.get_split_list())
    data_processing.write_to_spreadsheet(settings_manager.config['other']['output_file'], header, podzielone_dane)

    # TODO find a way to open Output file in system preffered spreadsheet app


if __name__ == "__main__":
    GUI.lobby()
