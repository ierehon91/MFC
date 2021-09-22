import psycopg2
from openpyxl import load_workbook
import config


class Base:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                                     password=config.base_password, host=config.base_host)
        self.cursor = self.conn.cursor()

    def create_tablets(self):
        with open('CREATE_TABLES_SCRIPT.sql', 'r') as file:
            sql = file.read()
        self.cursor.execute(sql)

    def commit_bd(self):
        self.conn.commit()

    def close_bd(self):
        self.conn.close()


class ExcelBase:
    def __init__(self):
        self.wb = load_workbook('base_model.xlsx')

    def parse_status_specialist(self):
        sheet_status_specialist = self.wb.get_sheet_by_name('status_specialists')
        statuses_specialists = []
        for i in range(2, 31):
            statuses_specialists.append(sheet_status_specialist.cell(row=i, column=1).value)
        return statuses_specialists


if __name__ == '__main__':
    # bd = Base()
    # bd.create_tablets()
    # bd.commit_bd()
    # bd.close_bd()
    excel_data = ExcelBase()
    print(excel_data.parse_status_specialist())
