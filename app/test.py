from flask import Flask, render_template, request

from base.base import Base


app = Flask(__name__)
db_data = Base()


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/reports/services')
def services():
    all_services_data = db_data.get_all_services_table()
    return render_template('services.html', services=all_services_data)

@app.route('/reports/services/add_service', methods = ['GET', 'POST'])
def add_service():
    if request.method == 'POST':
        pass
    return render_template('add_service.html')


@app.route('/reports/services/<service_id>')
def service_page(service_id):
    service_info = db_data.get_service_info(service_id)
    return render_template('service_page.html', service_info=service_info)


@app.route('/reports/services/program_services/change', methods=["GET", "POST"])
def change_rel_program_services_services():
    if request.method == 'POST':
        db_data.set_services_program_services(request.form.to_dict())
        db_data.commit_bd()
    program_services = db_data.get_program_services_table()
    services_data = db_data.get_services_table()
    return render_template('change_rel_serv_prog_serv.html', program_services=program_services,
                           services=services_data)


@app.route('/specialists')
def specialists():
    specialists = db_data.get_specialists()
    return render_template('specialists.html', specialists=specialists)


if __name__ == '__main__':
    app.run(debug=True)
