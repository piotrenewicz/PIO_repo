import arial10

from os import startfile
import fdb
import xlwt
import datetime


class DataManager(object):
    date = str
    date_explicit = bool
    output_filename = str
    connection_args = dict
    splits = []

    def __init__(self, choice: bool):
        # collecting params from settings_manager
        from main import settings_manager
        other_config = settings_manager.config['other']
        self.date = other_config['to_date']
        self.output_filename = other_config['output_file']
        self.connection_args = settings_manager.get_connection_arg()
        self.splits = settings_manager.get_split_list()

        # generating today, in case date is not explicit
        if self.date == '':
            now = datetime.datetime.now()
            self.date = now.strftime("%Y-%m-%d")
            self.date_explicit = False
        else:
            self.date_explicit = True

        # Doing all the magic
        query = self.render_query(choice)
        header, data = self.read_database(query)
        podzielone_dane = self.split_data(data)
        self.write_to_spreadsheet(header, podzielone_dane, self.create_split_labels())

        if other_config.getboolean('open_file'):
            startfile(self.output_filename + ".xls")

    def render_query(self, choose: bool):

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
                date '{self.date}' - DATA - TERMIN_ZAPLATY AS DNI_PO_TERMINIE
            FROM 
                ({mapa_kolumn})
            )
        WHERE
            DO_ZAPLATY > 0 AND DNI_PO_TERMINIE > 0
        ORDER BY
            KONTRAHENT
        ;
        """
        return query

    def read_database(self, query: str):
        connection = fdb.connect(**self.connection_args)
        cursor = connection.cursor()
        cursor.execute(query)

        header = [fieldDesc[fdb.DESCRIPTION_NAME] for fieldDesc in cursor.description]
        data = [[value for value in row] for row in cursor]

        return header, data

    def split_data(self, og_data: list):
        processed_data = []
        data = og_data

        for limit in self.splits:
            passed, data = self.filter_limit(data, limit)
            processed_data.append(passed)

        return processed_data

    @staticmethod
    def filter_limit(data: list, limit: int):
        passed = []
        failed = []

        for faktura in data:
            if faktura[-1] > limit:
                passed.append(faktura)
            else:
                failed.append(faktura)

        return passed, failed

    def create_split_labels(self):
        prev = "+"
        split_labels = []

        for idx in range(len(self.splits)):
            current_label = str(self.splits[idx])
            split_labels.append(current_label + prev)
            prev = "-" + current_label

        return split_labels

    class FitSheetWrapper(object):
        """Try to fit columns to max size of any entry.
        To use, wrap this around a worksheet returned from the
        workbook's add_sheet method, like follows:

            sheet = FitSheetWrapper(book.add_sheet(sheet_name))

        The worksheet interface remains the same: this is a drop-in wrapper
        for auto-sizing columns.
        """
        def __init__(self, sheet):
            self.sheet = sheet
            self.widths = dict()

        def write(self, r, c, label, *args, **kwargs):
            self.sheet.write(r, c, label, *args, **kwargs)

            offset = 0
            if type(label) == float:
                offset = 262.637 * 2 + 146.015

            width = arial10.fitwidth(str(label)) + offset
            if width > self.widths.get(c, 0):
                self.widths[c] = width
                self.sheet.col(c).width = int(width)

        def __getattr__(self, attr):
            return getattr(self.sheet, attr)

    def write_to_spreadsheet(self, header, splitted_data, split_labels):
        split_labels.reverse()
        splitted_data.reverse()
        wb = xlwt.Workbook()

        for idx, split in enumerate(splitted_data):
            self.add_new_sheet(wb, header, split, split_labels[idx])

        wb.save(self.output_filename + ".xls")

    def add_new_sheet(self, wb, header, data, sheet_name):
        ws = self.FitSheetWrapper(wb.add_sheet(sheet_name, cell_overwrite_ok=True))

        # style = xlwt.XFStyle()
        # style.num_format_str = r'#,##0'
        # pattern = xlwt.Pattern()
        # pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        # pattern.pattern_fore_colour = xlwt.Style.colour_map['dark_purple']
        # style.pattern = pattern

        style = xlwt.easyxf("", "#,##0.00")

        for column, column_value in enumerate(header):
            ws.write(0, column, column_value)

            for row, row_value in enumerate(data):
                if column in range(3, 8):
                    ws.write(row + 1, column, row_value[column], style)
                else:
                    ws.write(row + 1, column, str(row_value[column]))

        for column_idx in range(3, 8):
            suma = 0
            for row_value in data:
                suma += row_value[column_idx]
            ws.write(len(data) + 1, column_idx, round(suma, 2), style)
        ws.write(len(data) + 1, 0, "SUMA:")

        if self.date_explicit:
            ws.write(len(data) + 2, 2, f"WYBRANA DATA: {self.date}")
