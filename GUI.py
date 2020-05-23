from tkinter import *
from PIL import ImageTk, Image


def settings(config=None):
    if config is None:
        from main import settings_manager
        config = settings_manager.config

    def zapisz():
        config_read['password'] = password.get()
        config_read['host'] = server_ip.get()
        config_read['database'] = catalogue.get()
        config_read['port'] = port.get()

    settings_window = Tk()

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

    config_read = config['DATABASE']

    password = Entry(settings_window, width=30, borderwidth=3)
    server_ip = Entry(settings_window, width=30, borderwidth=3)
    port = Entry(settings_window, width=30, borderwidth=3)
    catalogue = Entry(settings_window, width=30, borderwidth=3)
    path = Entry(settings_window, width=30, borderwidth=3)

    password.grid(row=1, column=1)
    server_ip.grid(row=2, column=1)
    port.grid(row=3, column=1)
    catalogue.grid(row=4, column=1)
    path.grid(row=7, column=1)

    password.insert(0, config_read['password'])
    server_ip.insert(0, config_read['host'])
    catalogue.insert(0, config_read['database'])
    port.insert(0, config_read['port'])

    myLabel0 = Label(settings_window, text="Ustawienia połączenia")
    myLabel1 = Label(settings_window, text="Hasło użytkownika SYSDBA:")
    myLabel2 = Label(settings_window, text="IP servera bazy danych:")
    myLabel3 = Label(settings_window, text="Numer portu:")
    myLabel4 = Label(settings_window, text="Katalog główny programu FAKT:")
    myLabel5 = Label(settings_window, text="Inne ustawienia")
    myLabel6 = Label(settings_window, text="Ścieżka pliku docelowego:")

    myLabel0.grid(row=0, column=0)
    myLabel1.grid(row=1, column=0)
    myLabel2.grid(row=2, column=0)
    myLabel3.grid(row=3, column=0)
    myLabel4.grid(row=4, column=0)
    myLabel5.grid(row=6, column=0)
    myLabel6.grid(row=7, column=0)

    button_0 = Button(settings_window, text="Sprawdź połączenie")
    button_1 = Button(settings_window, text="Zapisz", command=zapisz)
    button_2 = Button(settings_window, text="Anuluj", command=settings_window.quit)
    button_0.grid(row=5, column=1)
    button_1.grid(row=8, column=0)
    button_2.grid(row=8, column=1)

    zapisz()

    settings_window.mainloop()


def lobby():
    from main import settings_manager
    splits = settings_manager.get_split_list()

    def add_split():
        pass

    def remove_split(idx: int):
        pass

    def save_splits():
        # TODO this will most probably require a loop over the text fields and casting to int
        settings_manager.set_split_list(splits)

    main_window = Tk()
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

    # ---------------------------------------


    main_window.mainloop()









