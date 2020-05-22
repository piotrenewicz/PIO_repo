import fdb
import xlwt
import datetime


def read_config(path: str):
    args = {}  # TODO: obsługa braku pliku. W takim przypadku otworzyć ustawienia, zebrać dane, i stworzyć ten plik
    with open(path, "r") as f:
        for line in f.readlines():
            line = line.strip("\n")
            arg, value = line.split("=")
            args[arg] = value
    return args

def render_query(choose:bool, to_date=None):

    if not to_date:
        now = datetime.datetime.now()
        to_date = now.strftime("%Y-%m-%d")  # TODO: to_date = dzisiaj

    wybierz_sprzedaz = """
    SELECT
        FAKT_NUMER_FAKTURY AS NR,
        FAKT_DATA AS DATA,
        KONT_NAZWA AS NAZWA,
        KONT_NAZWA2 AS NAZWA2,
        FAKT_BEZ_PODATKU AS BEZ_PODATKU,
        FAKT_PODATEK_RAZEM AS ODLICZ,
        FAKT_ZAPLATA_RAZEM AS ZAPLACONO,
        FAKT_TERMIN_ZAPLATY AS TERMIN_ZAPLATY
    FROM
        VIEW_OKNO_FAKT
    """

    wybierz_zakup = """
    SELECT 
        ZAKU_NUMER_DOK AS NR, 
        ZAKU_DATA AS DATA,
        KONT_NAZWA AS NAZWA,
        KONT_NAZWA2 AS NAZWA2,
        ZAKU_BEZ_PODATKU AS BEZ_PODATKU,
        ZAKU_ODLICZ AS ODLICZ,
        ZAKU_ZAPLACONO AS ZAPLACONO,
        ZAKU_TERMIN_ZAPL AS TERMIN_ZAPLATY
    FROM 
        VIEW_OKNO_ZAKU
    """

    mapa_kolumn = ''
    if choose:
        mapa_kolumn = wybierz_sprzedaz
    else:
        mapa_kolumn = wybierz_zakup


    query = f"""
    SELECT *
    FROM 
        (SELECT 
            NR,
            DATA,
            NAZWA || coalesce(' ' || NAZWA2, '') as KONTRAHENT,
            ROUND(BEZ_PODATKU, 2) AS NETTO,
            ROUND(ODLICZ, 2) AS VAT,
            ROUND(BEZ_PODATKU + ODLICZ, 2) AS BRUTTO,
            ROUND(ZAPLACONO, 2) AS ZAPLACONO,
            ROUND(BEZ_PODATKU + ODLICZ - ZAPLACONO, 2) AS DO_ZAPLATY,
            DATA + TERMIN_ZAPLATY AS TERMIN_PLATNOSCI,
            date '{to_date}' - DATA - TERMIN_ZAPLATY AS DNI_PO_TERMINIE
        FROM 
            ({mapa_kolumn})
        )
    WHERE
        DO_ZAPLATY > 0 AND DNI_PO_TERMINIE > 0
    ORDER BY
        DATA
    ;
    """
    return query


def read_database(connection_args: dict, query: str):
    connection = fdb.connect(**connection_args)
    cursor = connection.cursor()
    cursor.execute(query)

    header = [fieldDesc[fdb.DESCRIPTION_NAME] for fieldDesc in cursor.description]
    data = [[value for value in row] for row in cursor]

    return header, data


def split_data(og_data: list, split_pattern: list):
    processed_data = []
    data = og_data

    for limit in split_pattern:
        passed, data = filter_limit(data, limit)
        processed_data.append(passed)

    return processed_data


def filter_limit(data: list, limit: int):
    passed = []
    failed = []

    for faktura in data:
        if faktura[-1] > limit:
            passed.append(faktura)
        else:
            failed.append(faktura)

    return passed, failed


def write_to_spreadsheet(filename, header, data):

    wb = xlwt.Workbook()  # TODO
    ws = wb.add_sheet("Sheet 1", cell_overwrite_ok=True)

    for row, row_value in enumerate(header):
        ws.write(0, row, row_value)
        for col, col_value in enumerate(data):
            ws.write(col+1, row, str(col_value[row]))

    wb.save("Spreadsheet.xls")


def execute():
    connection_args = read_config("connection_config.txt")
    query = render_query(False)
    header, data = read_database(connection_args, query)
    write_to_spreadsheet("filename", header, data)

