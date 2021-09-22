import psycopg2
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


if __name__ == '__main__':
    bd = Base()
    bd.create_tablets()
    bd.commit_bd()
    bd.close_bd()
