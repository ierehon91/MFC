import psycopg2
import config
from flask import Flask, render_template


def get_program_services_table():
    conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                            password=config.base_password, host=config.base_host)
    cursor = conn.cursor()
    sql_script = """SELECT program_services.program_service_name, services.service_name FROM program_services
                    LEFT JOIN services_program_services ON services_program_services.fk_program_service = program_services.program_service_id
                    LEFT JOIN services ON services_program_services.fk_service = services.service_id;"""
    cursor.execute(sql_script)
    program_services = cursor.fetchall()
    return program_services


def get_services_table():
    conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                            password=config.base_password, host=config.base_host)
    cursor = conn.cursor()
    sql_script = """SELECT services.service_name FROM services;"""
    cursor.execute(sql_script)
    return cursor.fetchall()


app = Flask(__name__)


@app.route('/services')
def services():
    return render_template('services.html', program_services=get_program_services_table(),
                           services=get_services_table())


if __name__ == '__main__':
    app.run(debug=True)
