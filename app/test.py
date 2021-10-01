from flask import Flask, render_template, request

from base.base import Base


app = Flask(__name__)
db_data = Base()


@app.route('/')
@app.route('/index')
def index():
    """Главная"""
    return render_template('index.html')


# Отчёты
@app.route('/reports')
def reports():
    """Главная отчёты"""
    render_template('reports.html')


@app.route('/reports/report-specialists')
def report_specialists():
    """Отчёты по специалистам"""
    return render_template('report_specialists.html')


@app.route('/reports/report-services', methods=['GET', 'POST'])
def report_services():
    """Отчёты по услугам"""
    if request.method == 'POST':
        dates = request.form.to_dict()
        report_services = db_data.get_report_services(dates['first_date'], dates['last_date'])
        return render_template('report_services.html', report_services=report_services, dates=dates)
    else:
        dates = {'first_date': '2021-06-01', 'last_date': '2021-09-30'}
        report_services = db_data.get_report_services(dates['first_date'], dates['last_date'])
        return render_template('report_services.html', report_services=report_services, dates=dates)


# Блок /reports/settings

@app.route('/reports/settings')
def reports():
    """Панель администратора отчётов"""
    render_template('reports_settings.html')


@app.route('/reports/settings/services')
def services():
    """Список фактических услуг"""
    all_services_data = db_data.get_all_services_table()
    return render_template('services.html', services=all_services_data)


@app.route('/reports/settings/services/add', methods=['GET', 'POST'])
def add_service():
    """Добавление фактической услуги"""
    if request.method == 'POST':
        db_data.insert_service_in_db(request.form.to_dict())
        db_data.commit_bd()
    groups = db_data.get_group_services()
    return render_template('add_service.html', groups=groups)


@app.route('/reports/settings/services/<service_id>')
def service_page(service_id):
    """Страница фактической услуги"""
    service_info = db_data.get_service_info(service_id)
    return render_template('service_page.html', service_info=service_info)


@app.route('/reports/settings/services/groups-services')
def groups_services():
    """Группы услуг"""
    return render_template('groups_services.html')


@app.route('/reports/settings/services/groups-services/add')
def add_group_services():
    """Добавление группы услуг"""
    return render_template('add_group_services.html')


@app.route('/reports/settings/services/groups-services/<group_services_id>')
def group_services_page(group_services_id):
    """Страница группы услуг"""
    return render_template('group_services_page.html')


@app.route('/reports/services/add_program_service', methods=['GET', 'POST'])
def add_program_service():
    if request.method == 'POST':
        db_data.insert_program_service_in_db(request.form.to_dict())
        db_data.commit_bd()
    tags = db_data.get_tags_services()
    return render_template('add_program_service.html', tags=tags)





@app.route('/reports/services/program_services/change', methods=["GET", "POST"])
def change_rel_program_services_services():
    if request.method == 'POST':
        db_data.set_services_program_services(request.form.to_dict())
        db_data.commit_bd()
    program_services = db_data.get_program_services_table()
    services_data = db_data.get_services_table()
    return render_template('change_rel_serv_prog_serv.html', program_services=program_services,
                           services=services_data)


@app.route('/reports/specialists')
def specialists():
    specialists = db_data.get_specialists()
    return render_template('specialists.html', specialists=specialists)


if __name__ == '__main__':
    app.run(debug=True)
