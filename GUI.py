from tkinter import *
import datetime
# from PIL import ImageTk, Image


def settings(config=None):
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

    if config is None:
        from main import settings_manager
        config = settings_manager.config

    config_read = config['DATABASE']

    def zapisz():
        config_read['password'] = password.get()
        config_read['host'] = server_ip.get()
        config_read['database'] = catalogue.get()
        config_read['port'] = port.get()
        config['other']['output_file'] = path.get()

        close()

    def close():
        settings_window.quit()
        settings_window.destroy()

    settings_window = Tk()
    settings_window.title("Ustawienia")
    settings_window.resizable(False, False)

    connection_frame = LabelFrame(settings_window, text="Ustawienia Połączenia", padx=10, pady=10)
    other_frame = LabelFrame(settings_window, text="Inne ustawienia", padx=10, pady=10)

    password = Entry(connection_frame, width=30, borderwidth=3, show =u"\u2022")
    server_ip = Entry(connection_frame, width=30, borderwidth=3)
    port = Entry(connection_frame, width=30, borderwidth=3)
    catalogue = Entry(connection_frame, width=30, borderwidth=3)
    path = Entry(other_frame, width=35, borderwidth=3)

    password.grid(row=1, column=1)
    server_ip.grid(row=2, column=1)
    port.grid(row=3, column=1)
    catalogue.grid(row=4, column=1)
    path.grid(row=7, column=1, sticky=W+E)

    password.insert(0, config_read['password'])
    server_ip.insert(0, config_read['host'])
    catalogue.insert(0, config_read['database'])
    port.insert(0, config_read['port'])
    path.insert(0, config['other']['output_file'])

    myLabel1 = Label(connection_frame, text="Hasło użytkownika SYSDBA:")
    myLabel2 = Label(connection_frame, text="IP servera bazy danych:")
    myLabel3 = Label(connection_frame, text="Numer portu:")
    myLabel4 = Label(connection_frame, text="Katalog główny programu FAKT:")
    myLabel5 = Label(other_frame, text="Ścieżka pliku docelowego:")

    myLabel1.grid(row=1, column=0, sticky=E)
    myLabel2.grid(row=2, column=0, sticky=E)
    myLabel3.grid(row=3, column=0, sticky=E)
    myLabel4.grid(row=4, column=0, sticky=E)
    myLabel5.grid(row=7, column=0, sticky=E)

    connection_frame.grid(row=0, column=0, columnspan=2, pady=10, padx=10)
    other_frame.grid(row=1, column=0, columnspan=2, pady=0, padx=10, sticky=E+W)

    button_1 = Button(settings_window, text="Zapisz", command=zapisz, padx=50)
    button_2 = Button(settings_window, text="Anuluj", command=close, padx=50)
    button_1.grid(row=3, column=0, pady=15)
    button_2.grid(row=3, column=1)

    settings_window.mainloop()


def lobby():
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
        settings()
        settings_manager.write_config()

    def zakupy():
        saveall()
        execute(False)

    def sprzedarze():
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
            settings_manager.config['splits']['splits'] = str(found_splits)
            write = True

        if write:
            settings_manager.write_config()

    main_window = Tk()
    main_window.title("Nasz program")
    main_window.resizable(False, False) #

    splits_frame = LabelFrame(main_window, text="Wybrane przedziały danych:", padx=10, pady=10)
    important_frame = Frame(main_window, padx=10, pady=10)

    for barrier in splits:
        display_split(str(barrier))

    new_split_button = Button(splits_frame, text="+", command=add_split, padx=6, pady=2)
    new_split_button.grid(row=y, column=0, padx=(0, 6))
    # ---------------------------------------
    myLabel0 = Label(important_frame, text="ID firmy do zestawienia:")
    myLabel0.grid(row=0, column=1, pady=(0, 20))
    myLabel1 = Label(important_frame, text="Data:")
    myLabel1.grid(row=1, column=1, pady=(0, 20), padx = (97, 0))

    id = Entry(important_frame, width=10, borderwidth=3)
    id.grid(row=0, column=2, pady=(0, 20))
    id.insert(0, settings_manager.config['other']['id_firmy'])

    to_date = Entry(important_frame, width=10, borderwidth=3)
    to_date.grid(row=1, column=2, pady=(0, 20))
    to_date.insert(0, settings_manager.config['other']['to_date'])

    button_0 = Button(important_frame, text="Zestawienie sprzedaży", pady=6, command=sprzedarze)
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









