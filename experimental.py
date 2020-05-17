import fdb

con = fdb.connect(host='10.220.22.171', database='C:\\FAKT95\\0001\\0001baza.fdb', user='sysdba', password='masterkey', charset='UTF8')
cur = con.cursor()
# cur.execute("SELECT RDB$RELATION_NAME, RDB$DESCRIPTION  FROM RDB$RELATIONS;")
# cur.execute("SELECT * FROM TAB_ZAKU;")
cur.execute("SELECT ZAKU_DATA, ZAKU_NUMER_DOK, ZAKU_BEZ_PODATKU, ZAKU_ODLICZ, ZAKU_BEZ_PODATKU + ZAKU_ODLICZ AS BRUTTO, ZAKU_ZAPLACONO, ZAKU_BEZ_PODATKU + ZAKU_ODLICZ - ZAKU_ZAPLACONO AS DO_ZAPLATY, ZAKU_TERMIN_ZAPL  FROM VIEW_OKNO_ZAKU;")
# cur.execute("SELECT * FROM TAB_ZPOZ;")

# cur.execute("SELECT  FROM RDB$RELATIONS;")




# cur.execute("SELECT * FROM VIEW_OKNO_FAKT;")



# VIEW_OKNO_DYST                  None
# VIEW_SPIN_PODO1                 None
# VIEW_SPIN_PODO2                 None
# TAB_DYSP                        ZUI: Dodatkowe zdarzenia zwiazane z klientami
# DEL_DYSP                        Usuniete: ZUI: Dodatkowe zdarzenia zwiazane z klientami
# TAB_KASA                        KBN: Operacje w kasie, banku i noty rozrachunkowe
# DEL_KASA                        Usuniete: KBN: Operacje w kasie, banku i noty rozrachunkowe
# VIEW_SPIN_POZC1                 None
# VIEW_SPIN_POZC2                 None
# VIEW_SPIN_ZPOZ1                 None
# VIEW_SPIN_ZPOZ2                 None
# VIEW_OKNO_DOKT                  None
# VIEW_OKNO_KBN                   None
# VIEW_OKNO_OPER                  None
# VIEW_OKNO_FAKT                  None
# VIEW_OKNO_ZAKU                  None


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

