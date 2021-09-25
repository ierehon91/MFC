import psycopg2
import config
from flask import Flask, render_template, request

from base.base import Base


app = Flask(__name__)
db_data = Base()
program_services = db_data.get_program_services_table()
services_data = db_data.get_services_table()
all_services_data = db_data.get_all_services_table()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/reports/services')
def services():
    return render_template('services.html', services=all_services_data)


@app.route('/reports/services/program_services/change', methods=["GET", "POST"])
def change_rel_program_services_services():
    if request.method == 'POST':
        db_data.set_services_program_services(request.form.to_dict())
        db_data.commit_bd()
    return render_template('change_rel_serv_prog_serv.html', program_services=program_services,
                           services=services_data)


if __name__ == '__main__':
    app.run(debug=True)
