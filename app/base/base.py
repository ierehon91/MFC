import psycopg2
import app.mfc_config as config


class Base:
    def __init__(self):
        self.conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                                     password=config.base_password, host=config.base_host)
        self.cursor = self.conn.cursor()

    def insert_service_in_db(self, service):
        sql_script = f"""INSERT INTO services (service_name, fk_group_service) VALUES (
        '{service['service_name']}',
        {service['group-select']}
        )"""
        self.cursor.execute(sql_script)
        print(f"Услуга {service['service_name']} добавлена!")

    def insert_program_service_in_db(self, program_service):
        sql_script = f"""INSERT INTO program_services (program_service_name, fk_tag_service) VALUES (
        '{program_service['name-program-service']}',
        {program_service['tag-select']}
        )"""
        self.cursor.execute(sql_script)
        print(f"Программная услуга {program_service['name-program-service']} добавлена!")

    def insert_reception_table_in_db(self, reception_data):
        sql_script = f"""INSERT INTO reception_table (date_reception, fk_specialist, fk_service, count_reception)
            VALUES (
            '{reception_data['date_reception']}',
            (SELECT specialist_id FROM specialists WHERE specialist_name = '{reception_data['specialist_name']}'),
            (SELECT program_service_id FROM program_services WHERE program_service_name = '{reception_data['service_name']}'),
            {reception_data['count_reception']}
            );"""
        self.cursor.execute(sql_script)
        print("Запсиь о приёме добавлена!")

    def add_tag_service_in_db(self, tag: dict):
        sql_script = f"""INSERT INTO tags_services (tag_name) VALUES ('{tag['tag_name']}');"""
        self.cursor.execute(sql_script)
        print(f"Тег {tag['tag_name']} добавлен")

    def get_program_services_table(self):
        sql_script = """SELECT program_services.program_service_name, services.service_name, 
            program_services.program_service_id, services.service_id 
            FROM program_services
            LEFT JOIN services_program_services 
            ON services_program_services.fk_program_service = program_services.program_service_id
            LEFT JOIN services 
            ON services_program_services.fk_service = services.service_id
            ORDER BY services.service_name;"""
        self.cursor.execute(sql_script)
        program_services = self.cursor.fetchall()
        return program_services

    def get_services_table(self):
        sql_script = """SELECT services.service_name FROM services;"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_all_services_table(self):
        sql_script = """SELECT group_services.group_name, service_name, service_id FROM services
            LEFT JOIN group_services ON services.fk_group_service = group_services.group_id
            ORDER BY group_services.group_name, service_name;"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def set_services_program_services(self, data):
        sql_script_delete = """DELETE FROM services_program_services;"""
        self.cursor.execute(sql_script_delete)
        for p_service_id, service_name in data.items():
            sql_script = f"""INSERT INTO services_program_services (fk_program_service, fk_service) VALUES (
                {p_service_id}, 
                (SELECT service_id FROM services WHERE service_name = '{service_name}')
            );"""
            self.cursor.execute(sql_script)

    def get_service_info(self, service_id):
        sql_script = f"""SELECT * FROM services WHERE service_id = {service_id}"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_tags_services(self):
        sql_script = f"""SELECT * FROM tags_services"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_tag_service(self, tag_id):
        sql_script = f"""SELECT * FROM tags_services WHERE tag_id = {tag_id}"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_specialists(self):
        sql_script = """SELECT status_name, specialist_name, rating, specialist_id FROM specialists
            LEFT JOIN specialist_statuses ON specialists.fk_status_specialist = specialist_statuses.status_id
            ORDER BY status_id, specialist_name;"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_group_services(self):
        sql_script = """SELECT * FROM group_services;"""
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def get_report_services(self, first_date, last_date):
        sql_script = f"""
        SELECT group_services.group_name, service_name, sum(count_reception) FROM reception_table
        LEFT JOIN specialists ON reception_table.fk_specialist = specialist_id
        LEFT JOIN program_services ON reception_table.fk_service = program_service_id
        LEFT JOIN services_program_services ON program_service_id = services_program_services.fk_program_service
        LEFT JOIN services ON services_program_services.fk_service = service_id
        LEFT JOIN group_services ON services.fk_group_service = group_id
        WHERE date_reception >= '{first_date}'
        AND date_reception <= '{last_date}'
        GROUP BY service_name, group_services.group_name
        ORDER BY group_services.group_name;
        """
        self.cursor.execute(sql_script)
        return self.cursor.fetchall()

    def change_tag_in_bd(self, tag):
        sql_script = f"""UPDATE tags_services 
        SET tag_name = '{tag['tag_name']}', tag_description = '{tag['tag_description']}'
        WHERE tag_id = {tag['tag_id']}"""
        self.cursor.execute(sql_script)
        print(f"Тег {tag['tag_name']} был изменён!")

    def commit_bd(self):
        self.conn.commit()

    def close_bd(self):
        self.conn.close()
