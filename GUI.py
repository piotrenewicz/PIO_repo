# from PIL import ImageTk, Image
from tkinter import *


class SettingsWindow(object):
    # ======= Ustawienia Połączenia ==================
    # hasło użytkownika SYSDBA
    # IP servera bazy danych
    # Numer Portu
    # Katalog Główny programu FAKT
    # [Sprawdź Połączenie]
    # ================================================

    # ======= Inne Ustawienia ========================
    # Ścieżka / Nazwa Pliku docelowego
    # ?????? Cokolwiek jeszcze będziemy potrzebować
    # Jeśli się będziemy bawić w kolory to możemy tu to ustawiać
    # Ale wątpie
    #
    # [Anuluj?]  [Zapisz]

    config = None
    database_config = None
    other_config = None
    settings_tk_root = Tk

    auto_open_var = IntVar
    password = Entry
    server_ip = Entry
    catalogue = Entry
    port = Entry
    path = Entry

    def __init__(self, config=None):
        if config is None:
            from main import settings_manager
            self.config = settings_manager.config
        else:
            self.config = config

        self.database_config = self.config['DATABASE']
        self.other_config = self.config['other']

        self.settings_tk_root = Tk()
        self.settings_tk_root.title("Ustawienia")
        self.settings_tk_root.resizable(False, False)
        self.settings_tk_root.iconphoto(False, PhotoImage(file="icon/256x256.png"))

        self.settings_tk_root.option_add("*font", "Lucida 10")

        connection_frame = LabelFrame(self.settings_tk_root, text="Ustawienia Połączenia", padx=10, pady=10)
        other_frame = LabelFrame(self.settings_tk_root, text="Inne ustawienia", padx=10, pady=10)
        self.auto_open_var = IntVar(master=other_frame, value=self.other_config.getboolean('open_file'))

        self.password = Entry(connection_frame, width=30, borderwidth=3, show=u"\U00002B24")
        self.server_ip = Entry(connection_frame, width=30, borderwidth=3)
        self.port = Entry(connection_frame, width=30, borderwidth=3)
        self.catalogue = Entry(connection_frame, width=30, borderwidth=3)
        self.path = Entry(other_frame, width=35, borderwidth=3)
        auto_open_box = Checkbutton(other_frame, variable=self.auto_open_var)

        self.password.grid(row=1, column=1)
        self.server_ip.grid(row=2, column=1)
        self.port.grid(row=3, column=1)
        self.catalogue.grid(row=4, column=1)
        self.path.grid(row=7, column=1, columnspan=2, sticky=W + E, pady=3)
        auto_open_box.grid(row=8, column=2, sticky=W, pady=6)

        self.password.insert(0, self.database_config['password'])
        self.server_ip.insert(0, self.database_config['host'])
        self.catalogue.insert(0, self.database_config['database'])
        self.port.insert(0, self.database_config['port'])
        self.path.insert(0, self.other_config['output_file'])

        my_label1 = Label(connection_frame, text="Hasło użytkownika SYSDBA:")
        my_label2 = Label(connection_frame, text="IP servera bazy danych:")
        my_label3 = Label(connection_frame, text="Numer portu:")
        my_label4 = Label(connection_frame, text="Katalog główny programu FAKT:")
        my_label5 = Label(other_frame, text="Ścieżka pliku docelowego:")
        my_label6 = Label(other_frame, text="Otwórz wykonane zestawienie: ")

        my_label1.grid(row=1, column=0, sticky=E)
        my_label2.grid(row=2, column=0, sticky=E)
        my_label3.grid(row=3, column=0, sticky=E)
        my_label4.grid(row=4, column=0, sticky=E)
        my_label5.grid(row=7, column=0, sticky=E, pady=3)
        my_label6.grid(row=8, column=0, sticky=E, columnspan=2, pady=6)

        connection_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
        other_frame.grid(row=1, column=0, columnspan=2, pady=0, padx=10, sticky=E + W)

        button_1 = Button(self.settings_tk_root, text="Zapisz", command=self.zapisz, padx=50)
        button_2 = Button(self.settings_tk_root, text="Anuluj", command=self.close, padx=50)
        button_1.grid(row=3, column=0, pady=15)
        button_2.grid(row=3, column=1)

        self.settings_tk_root.mainloop()

    def zapisz(self):
        self.database_config['password'] = self.password.get()
        self.database_config['host'] = self.server_ip.get()
        self.database_config['database'] = self.catalogue.get()
        self.database_config['port'] = self.port.get()
        self.other_config['output_file'] = self.path.get()
        self.other_config['open_file'] = str(self.auto_open_var.get())

        self.close()

    def close(self):
        self.settings_tk_root.quit()
        self.settings_tk_root.destroy()


class LobbyWindow(object):
    # ======= Podziel Spóźnienia na =============
    # [-] [0            ]
    # [-] [30           ]
    # [-] [60           ]
    # [-] [90           ]
    # [-] [180          ]
    # [+]
    #
    # ID Firmy do zestawienia: [1   ]           # potem trzeba będzie zrobić padding    [1   ] == [0001]
    # [Zestawienie Sprzedaży]
    # [Zestawienie Zakupów  ]
    #
    # [Ustawienia]      [Zamknij Program]

    lobby_tk_root = Tk
    y = 0
    splits_entry_fields = []
    splits_remove_buttons = []
    splits = []
    splits_frame = LabelFrame
    new_split_button = Button
    settings_manager = object
    execute = None
    selected_firm_ID = Entry
    to_date = Entry

    def __init__(self):
        from main import settings_manager, execute
        self.settings_manager = settings_manager
        self.execute = execute

        self.splits = self.settings_manager.get_split_list()

        self.lobby_tk_root = Tk()
        self.lobby_tk_root.title("ZZiNP")
        self.lobby_tk_root.resizable(False, False)
        self.lobby_tk_root.iconphoto(False, PhotoImage(file="icon/256x256.png"))

        self.lobby_tk_root.option_add("*font", "Lucida 10")

        self.splits_frame = LabelFrame(self.lobby_tk_root, text="Wybrane przedziały danych:", padx=10, pady=10)
        important_frame = Frame(self.lobby_tk_root, padx=10, pady=10)

        for barrier in self.splits:
            self.display_split(str(barrier))

        self.new_split_button = Button(self.splits_frame, text="+", command=self.add_split, padx=6, pady=2)
        self.new_split_button.grid(row=self.y, column=0, padx=(0, 6))
        # ---------------------------------------
        my_label0 = Label(important_frame, text="ID firmy do zestawienia:")
        my_label0.grid(row=0, column=1)
        my_label1 = Label(important_frame, text="Data:")
        my_label1.grid(row=1, column=1, pady=(0, 20), sticky=E)

        self.selected_firm_ID = Entry(important_frame, width=10, borderwidth=3)
        self.selected_firm_ID.grid(row=0, column=2)
        self.selected_firm_ID.insert(0, self.settings_manager.config['other']['id_firmy'])

        self.to_date = Entry(important_frame, width=10, borderwidth=3)
        self.to_date.grid(row=1, column=2, pady=(0, 20))
        self.to_date.insert(0, self.settings_manager.config['other']['to_date'])

        button_0 = Button(important_frame, text="Zestawienie sprzedaży", pady=6, command=self.sprzedaze)
        button_1 = Button(important_frame, text="Zestawienie zakupów", pady=6, command=self.zakupy)
        button_2 = Button(important_frame, text="Ustawienia", pady=6, command=self.ustawienia)
        button_3 = Button(important_frame, text="Zamknij program", pady=6, command=self.lobby_tk_root.quit)
        button_0.grid(row=2, column=1, columnspan=2, sticky=W + E)
        button_1.grid(row=3, column=1, columnspan=2, sticky=W + E, pady=(0, 20))
        button_2.grid(row=4, column=1, columnspan=2, sticky=W + E)
        button_3.grid(row=5, column=1, columnspan=2, sticky=W + E)

        self.splits_frame.grid(row=0, column=0, padx=15, pady=15)
        important_frame.grid(row=0, column=1, pady=15, sticky=N + E)

        self.lobby_tk_root.mainloop()

    def display_split(self, num: str):
        new_remove = Button(self.splits_frame, text="-", command=lambda y=self.y: self.remove_split(y), padx=8, pady=2)
        new_remove.grid(row=self.y, column=0, padx=(0, 6))
        self.splits_remove_buttons.append(new_remove)
        new_entry = Entry(self.splits_frame, width=15, borderwidth=3)
        new_entry.grid(row=self.y, column=1)
        new_entry.insert(0, num)
        self.splits_entry_fields.append(new_entry)
        self.y += 1

    def add_split(self):
        self.display_split("")
        self.new_split_button.grid_forget()
        self.new_split_button.grid(row=self.y, column=0, padx=(0, 6))

    def remove_split(self, idx: int):
        self.splits_entry_fields[idx].grid_forget()
        self.splits_remove_buttons[idx].grid_forget()
        self.splits_entry_fields[idx] = None
        self.splits_entry_fields[idx] = None

    def ustawienia(self):
        SettingsWindow()
        self.settings_manager.write_config()

    def zakupy(self):
        self.saveall()
        self.execute(False)

    def sprzedaze(self):
        self.saveall()
        self.execute(True)

    def saveall(self):
        write = False
        if self.settings_manager.config['other']['id_firmy'] != self.selected_firm_ID.get():
            self.settings_manager.config['other']['id_firmy'] = self.selected_firm_ID.get()
            write = True

        if self.settings_manager.config['other']['to_date'] != self.to_date.get():
            self.settings_manager.config['other']['to_date'] = self.to_date.get()
            write = True

        found_splits = []
        for entry_field in self.splits_entry_fields:
            if entry_field:
                split = entry_field.get()
                if split.isnumeric():
                    found_splits.append(int(split))

        found_splits = sorted(found_splits, reverse=True)
        if found_splits != self.settings_manager.get_split_list():
            self.settings_manager.config['other']['splits'] = str(found_splits)
            write = True

        if write:
            self.settings_manager.write_config()
