import fdb

connect_args = {}
with open("connection_config.txt", "r") as f:
    for line in f.readlines():
        line = line.strip("\n")
        arg, value = line.split("=")
        connect_args[arg] = value

querry = """
SELECT 
    ZAKU_DATA AS DATA,
    ZAKU_NUMER_DOK AS NR,
    ZAKU_BEZ_PODATKU AS NETTO,
    ZAKU_ODLICZ AS VAT,
    ZAKU_BEZ_PODATKU + ZAKU_ODLICZ AS BRUTTO,
    ZAKU_ZAPLACONO,
    ZAKU_BEZ_PODATKU + ZAKU_ODLICZ - ZAKU_ZAPLACONO AS DO_ZAPLATY,
    ZAKU_TERMIN_ZAPL 
FROM 
    VIEW_OKNO_ZAKU;
"""

# for arg, val in connect_args.items():
#     print(arg, val)


con = fdb.connect(**connect_args)
cur = con.cursor()
cur.execute(querry)

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

