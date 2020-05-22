import data_processing
import fdb


def run():
    connection_args = data_processing.read_config("connection_config.txt")
    query = data_processing.render_query(False)

    # query = "SELECT * FROM VIEW_OKNO_ZAKU;"
    # query = "select * from VIEW_OKNO_FAKT;"
    # query = "SELECT RDB$RELATION_NAME, RDB$DESCRIPTION  FROM RDB$RELATIONS;"

    header, data = data_processing.read_database(connection_args, query)

    split_data = data_processing.split_data(data, [180, 90, 30, 0])




    data_processing.write_to_spreadsheet("filename", header, split_data[3])



    # con = fdb.connect(**connection_args)
    # cur = con.cursor()
    # cur.execute(query)
    #
    # # Print a header.
    # for fieldDesc in cur.description:
    #     print(fieldDesc[fdb.DESCRIPTION_NAME].ljust(fieldDesc[fdb.DESCRIPTION_DISPLAY_SIZE]), end=" ")
    # print()  # Finish the header with a newline.
    # print('-' * 78)
    #
    # # For each row, print the value of each field left-justified within
    # # the maximum possible width of that field.
    # fieldIndices = range(len(cur.description))
    # for row in cur:
    #     for fieldIndex in fieldIndices:
    #         fieldValue = str(row[fieldIndex])
    #         fieldMaxWidth = cur.description[fieldIndex][fdb.DESCRIPTION_DISPLAY_SIZE]
    #
    #         print(fieldValue.ljust(fieldMaxWidth), end=" ")
    #
    #     print()  # Finish the row with a newline.