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


def render_query(to_date=None):
    if not to_date:
        pass  # TODO: to_date = dzisiaj

    query = f"""
SELECT *
FROM 
    (SELECT 
        ZAKU_NUMER_DOK AS NR,
        ZAKU_DATA AS DATA,
        KONT_NAZWA || KONT_NAZWA2 as Kontrahent,
        ROUND(ZAKU_BEZ_PODATKU, 2) AS NETTO,
        ROUND(ZAKU_ODLICZ, 2) AS VAT,
        ROUND(ZAKU_BEZ_PODATKU + ZAKU_ODLICZ, 2) AS BRUTTO,
        ROUND(ZAKU_ZAPLACONO, 2) AS ZAPLACONO,
        ROUND(ZAKU_BEZ_PODATKU + ZAKU_ODLICZ - ZAKU_ZAPLACONO, 2) AS DO_ZAPLATY,
        ZAKU_DATA + ZAKU_TERMIN_ZAPL AS TERMIN_PLATNOSCI,
        date '{to_date}' - ZAKU_DATA - ZAKU_TERMIN_ZAPL AS DNI_PO_TERMINIE
    FROM 
        VIEW_OKNO_ZAKU)
WHERE
    DO_ZAPLATY > 0 AND DNI_PO_TERMINIE > 0
ORDER BY
    DATA
;
"""     # ZAKU_TERMIN_ZAPL AS DNI_NA_ZAPLATE,
    return query


def read_database(connection_args: dict, query: str):
    connection = fdb.connect(**connection_args)
    cursor = connection.cursor()
    cursor.execute(query)

    header = [fieldDesc[fdb.DESCRIPTION_NAME] for fieldDesc in cursor.description]
    data = [[value for value in row] for row in cursor]

    return header, data


def split_data(data: list, split_pattern: list):
    processed_data = []
    for limit in split_pattern:
        data_bucket = []
        for idx, row in enumerate(data):
            if row[-1] > limit:
                data_bucket.append(row[:])
                del row
        processed_data.append(data_bucket)
    return processed_data


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
    query = render_query("01.01.2020")
    header, data = read_database(connection_args, query)
    write_to_spreadsheet("filename", header, data)

