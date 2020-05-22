import fdb
import tkinter as tk
import data_processing


data_processing.execute()
exit()  # comment this for debug
import debug
debug.run()
exit()


# GOING FURTHER DOWN IS NOW deprecated
print("this shouldn't execute")
# soon to be removed, and replaced with debug file
# if there's anything of value left here copy it to debug

connect_args = {}  # TODO: obsługa braku pliku. W takim przypadku otworzyć ustawienia, zebrać dane, i stworzyć ten plik
with open("connection_config.txt", "r") as f:
    for line in f.readlines():
        line = line.strip("\n")
        arg, value = line.split("=")
        connect_args[arg] = value

to_date = "01.01.2020"

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

# for arg, val in connect_args.items():
#     print(arg, val)

con = fdb.connect(**connect_args)
cur = con.cursor()
# cur.execute(query)
cur.execute("SELECT * FROM VIEW_OKNO_ZAKU;")
# cur.execute("SELECT RDB$RELATION_NAME, RDB$DESCRIPTION  FROM RDB$RELATIONS;")
# cur.execute("select * from TAB_FAKT")
# cur.execute("select * from VIEW_OKNO_FAKT")

# Print a header.
for fieldDesc in cur.description:
    print(fieldDesc[fdb.DESCRIPTION_NAME].ljust(fieldDesc[fdb.DESCRIPTION_DISPLAY_SIZE]), end=" ")
print()  # Finish the header with a newline.
print('-' * 78)

# For each row, print the value of each field left-justified within
# the maximum possible width of that field.
fieldIndices = range(len(cur.description))
for row in cur:
    for fieldIndex in fieldIndices:
        fieldValue = str(row[fieldIndex])
        fieldMaxWidth = cur.description[fieldIndex][fdb.DESCRIPTION_DISPLAY_SIZE]

        print(fieldValue.ljust(fieldMaxWidth), end=" ")

    print()  # Finish the row with a newline.

