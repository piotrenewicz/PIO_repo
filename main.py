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
        }

    def get_connection_arg(self, id_firmy: int):
        connection_arg = dict(self.config['DATABASE'])
        connection_arg['port'] = int(connection_arg['port'])
        padded_id_firmy = str(id_firmy).zfill(4)
        connection_arg['database'] = "".join([connection_arg['database'], "\\", padded_id_firmy, "\\", padded_id_firmy, "baza.fdb"])
        return connection_arg

    def read_config(self):
        with open('config.ini', 'r') as configfile:
            self.config.read_file(configfile)

    def write_config(self):
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)


settings_manager = SettingManager()
if __name__ == "__main__":
    # GUI.lobby()
    settings_manager.get_connection_arg(1)
    # data_processing.execute()
    exit()  # comment this for debug
    import debug
    debug.run()
    exit()

