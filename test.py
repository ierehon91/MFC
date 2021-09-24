import psycopg2
import config
from flask import Flask, render_template, request


def get_program_services_table():
    conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                            password=config.base_password, host=config.base_host)
    cursor = conn.cursor()
    sql_script = """SELECT program_services.program_service_name, services.service_name, program_services.program_service_id, services.service_id FROM program_services
                    LEFT JOIN services_program_services ON services_program_services.fk_program_service = program_services.program_service_id
                    LEFT JOIN services ON services_program_services.fk_service = services.service_id
                    ORDER BY services.service_name;"""
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


def set_services_program_services(data):
    conn = psycopg2.connect(dbname=config.base_name, user=config.base_user,
                            password=config.base_password, host=config.base_host)
    cursor = conn.cursor()
    sql_script_delete = """DELETE FROM services_program_services;"""
    cursor.execute(sql_script_delete)
    for p_service_id, service_name in data.items():
        sql_script = f"""INSERT INTO services_program_services (fk_program_service, fk_service) VALUES ({p_service_id}, (SELECT service_id FROM services WHERE service_name = '{service_name}'))"""
        cursor.execute(sql_script)
    conn.commit()


app = Flask(__name__)


@app.route('/services', methods=["GET", "POST"])
def services():
    if request.method == 'POST':
        set_services_program_services(request.form.to_dict())
    return render_template('services.html', program_services=get_program_services_table(),
                           services=get_services_table())


if __name__ == '__main__':
    app.run(debug=True)
