# from PIL import ImageTk, Image
from tkinter import *
from tkinter import messagebox
import sys


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
    settings_tk_root = None

    auto_open_var = None
    password = None
    server_ip = None
    catalogue = None
    port = None
    path = None

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

        myLabel1 = Label(connection_frame, text="Hasło użytkownika SYSDBA:")
        myLabel2 = Label(connection_frame, text="IP servera bazy danych:")
        myLabel3 = Label(connection_frame, text="Numer portu:")
        myLabel4 = Label(connection_frame, text="Katalog główny programu FAKT:")
        myLabel5 = Label(other_frame, text="Ścieżka pliku docelowego:")
        myLabel6 = Label(other_frame, text="Otwórz wykonane zestawienie: ")

        myLabel1.grid(row=1, column=0, sticky=E)
        myLabel2.grid(row=2, column=0, sticky=E)
        myLabel3.grid(row=3, column=0, sticky=E)
        myLabel4.grid(row=4, column=0, sticky=E)
        myLabel5.grid(row=7, column=0, sticky=E, pady=3)
        myLabel6.grid(row=8, column=0, sticky=E, columnspan=2, pady=6)

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


class Lobby(object):
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

    def __init__(self):
        main_window = Tk()
        main_window.title("ZZiNP")
        main_window.resizable(False, False)

        main_window.option_add("*font", "Lucida 10")

        splits_frame = LabelFrame(main_window, text="Wybrane przedziały danych:", padx=10, pady=10)
        important_frame = Frame(main_window, padx=10, pady=10)

        for barrier in splits:
            display_split(str(barrier))

        new_split_button = Button(splits_frame, text="+", command=add_split, padx=6, pady=2)
        new_split_button.grid(row=y, column=0, padx=(0, 6))
        # ---------------------------------------
        myLabel0 = Label(important_frame, text="ID firmy do zestawienia:")
        myLabel0.grid(row=0, column=1)
        myLabel1 = Label(important_frame, text="Data:")
        myLabel1.grid(row=1, column=1, pady=(0, 20), sticky=E)

        id = Entry(important_frame, width=10, borderwidth=3)
        id.grid(row=0, column=2)
        id.insert(0, settings_manager.config['other']['id_firmy'])

        to_date = Entry(important_frame, width=10, borderwidth=3)
        to_date.grid(row=1, column=2, pady=(0, 20))
        to_date.insert(0, settings_manager.config['other']['to_date'])

        button_0 = Button(important_frame, text="Zestawienie sprzedaży", pady=6, command=sprzedaze)
        button_1 = Button(important_frame, text="Zestawienie zakupów", pady=6, command=zakupy)
        button_2 = Button(important_frame, text="Ustawienia", pady=6, command=ustawienia)
        button_3 = Button(important_frame, text="Zamknij program", pady=6, command=main_window.quit)
        button_0.grid(row=2, column=1, columnspan=2, sticky=W + E)
        button_1.grid(row=3, column=1, columnspan=2, sticky=W + E, pady=(0, 20))
        button_2.grid(row=4, column=1, columnspan=2, sticky=W + E)
        button_3.grid(row=5, column=1, columnspan=2, sticky=W + E)

        splits_frame.grid(row=0, column=0, padx=15, pady=15)
        important_frame.grid(row=0, column=1, pady=15, sticky=N + E)

        main_window.mainloop()

    from main import settings_manager, execute
    splits = settings_manager.get_split_list()

    y = 0
    splits_entry_fields = []
    splits_remove_buttons = []

    def display_split(num: str):
        nonlocal y
        new_remove = Button(splits_frame, text="-", command=lambda y=y: remove_split(y), padx=8, pady=2)
        new_remove.grid(row=y, column=0, padx=(0, 6))
        splits_remove_buttons.append(new_remove)
        new_entry = Entry(splits_frame, width=15, borderwidth=3)
        new_entry.grid(row=y, column=1)
        new_entry.insert(0, num)
        splits_entry_fields.append(new_entry)
        y += 1

    def add_split():
        display_split("")
        new_split_button.grid_forget()
        new_split_button.grid(row=y, column=0, padx=(0, 6))

    def remove_split(idx: int):
        splits_entry_fields[idx].grid_forget()
        splits_remove_buttons[idx].grid_forget()
        splits_entry_fields[idx] = None
        splits_entry_fields[idx] = None

    def ustawienia():
        SettingsWindow()
        settings_manager.write_config()

    def zakupy():
        saveall()
        execute(False)

    def sprzedaze():
        saveall()
        execute(True)

    def saveall():
        write = False
        if settings_manager.config['other']['id_firmy'] != id.get():
            settings_manager.config['other']['id_firmy'] = id.get()
            write = True

        if settings_manager.config['other']['to_date'] != to_date.get():
            settings_manager.config['other']['to_date'] = to_date.get()
            write = True

        found_splits = []
        for entry_field in splits_entry_fields:
            if entry_field:
                split = entry_field.get()
                if split.isnumeric():
                    found_splits.append(int(split))

        found_splits = sorted(found_splits, reverse=True)
        if found_splits != settings_manager.get_split_list():
            settings_manager.config['other']['splits'] = str(found_splits)
            write = True

        if write:
            settings_manager.write_config()

    main_window = Tk()
    main_window.title("ZZiNP")
    main_window.resizable(False, False)

    main_window.option_add("*font", "Lucida 10")

    splits_frame = LabelFrame(main_window, text="Wybrane przedziały danych:", padx=10, pady=10)
    important_frame = Frame(main_window, padx=10, pady=10)

    for barrier in splits:
        display_split(str(barrier))

    new_split_button = Button(splits_frame, text="+", command=add_split, padx=6, pady=2)
    new_split_button.grid(row=y, column=0, padx=(0, 6))
    # ---------------------------------------
    myLabel0 = Label(important_frame, text="ID firmy do zestawienia:")
    myLabel0.grid(row=0, column=1)
    myLabel1 = Label(important_frame, text="Data:")
    myLabel1.grid(row=1, column=1, pady=(0, 20), sticky=E)

    id = Entry(important_frame, width=10, borderwidth=3)
    id.grid(row=0, column=2)
    id.insert(0, settings_manager.config['other']['id_firmy'])

    to_date = Entry(important_frame, width=10, borderwidth=3)
    to_date.grid(row=1, column=2, pady=(0, 20))
    to_date.insert(0, settings_manager.config['other']['to_date'])

    button_0 = Button(important_frame, text="Zestawienie sprzedaży", pady=6, command=sprzedaze)
    button_1 = Button(important_frame, text="Zestawienie zakupów", pady=6, command=zakupy)
    button_2 = Button(important_frame, text="Ustawienia", pady=6, command=ustawienia)
    button_3 = Button(important_frame, text="Zamknij program", pady=6, command=main_window.quit)
    button_0.grid(row=2, column=1, columnspan=2, sticky=W+E)
    button_1.grid(row=3, column=1, columnspan=2, sticky=W+E, pady=(0, 20))
    button_2.grid(row=4, column=1, columnspan=2, sticky=W+E)
    button_3.grid(row=5, column=1, columnspan=2, sticky=W+E)

    splits_frame.grid(row=0, column=0, padx=15, pady=15)
    important_frame.grid(row=0, column=1, pady=15, sticky=N+E)

    main_window.mainloop()









