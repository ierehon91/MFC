from flask import Flask, render_template, request, redirect
from app.date_formats.date_formats import get_first_last_this_month_dates
from base.get_is_active_program_service_tags import get_is_active_program_service_tags
from base.data_base_class import Base


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
    return render_template('reports.html')


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

        dates = get_first_last_this_month_dates()
        report_services = db_data.get_report_services(dates['first_date'], dates['last_date'])
        return render_template('report_services.html', report_services=report_services, dates=dates)


# Блок /reports/settings

@app.route('/reports/settings')
def reports_settings():
    """Панель администратора отчётов"""
    return render_template('reports_settings.html')


@app.route('/reports/settings/services')
def services():
    """Список фактических услуг"""
    all_services_data = db_data.get_all_services_table()
    return render_template('reports_settings_services.html', services=all_services_data)


@app.route('/reports/settings/services/add', methods=['GET', 'POST'])
def add_service():
    """Добавление фактической услуги"""
    if request.method == 'POST':
        db_data.insert_service_in_db(request.form.to_dict())
        db_data.commit_bd()
    groups = db_data.get_group_services()
    return render_template('reports_settings_services_add.html', groups=groups)


@app.route('/reports/settings/services/<service_id>')
def service_page(service_id):
    """Страница фактической услуги"""
    service_info = db_data.get_service_info(service_id)
    return render_template('reports_settings_services_page.html', service_info=service_info)


@app.route('/reports/settings/services/groups-services')
def groups_services():
    """Группы услуг"""
    return render_template('reports_settings_services_group_services.html')


@app.route('/reports/settings/services/groups-services/add')
def add_group_services():
    """Добавление группы услуг"""
    return render_template('reports_settings_services_group_services_add.html')


@app.route('/reports/settings/services/groups-services/<group_services_id>')
def group_services_page(group_services_id):
    """Страница группы услуг"""
    return render_template('reports_settings_services_group_services_page.html')


@app.route('/reports/settings/program-services')
def program_services():
    """Программные услуги"""
    program_services = db_data.get_program_services_table()
    rel_services_tags = db_data.get_rel_services_tags()
    ser_tags_dict = []
    for service in program_services:
        tags = []
        for tag in rel_services_tags:
            if service[2] == tag[0]:
                tags.append(tag[1])
        ser_tags_dict.append({service[2]: tags})
    ser_tags_dict = [list(x.items()) for x in ser_tags_dict]
    return render_template('reports_settings_program_services.html', program_services=program_services,
                           ser_tags_dict=ser_tags_dict)


@app.route('/reports/settings/program-services/add', methods=['GET', 'POST'])
def add_program_service():
    """Добавление программной услуги"""
    if request.method == 'POST':
        db_data.insert_program_service_in_db(request.form.to_dict())
        return redirect('/reports/settings/program-services/add')
    tags = db_data.get_tags_services()
    return render_template('reports_settings_program_services_add.html', tags=tags)


@app.route('/reports/settings/program-services/<program_service_id>', methods=['GET', 'POST'])
def program_service_page(program_service_id):
    """Страница программной услуги"""
    service = db_data.get_program_service_info(program_service_id)
    tags = get_is_active_program_service_tags(service[0][0])

    if request.method == 'POST':
        update_data = request.form.to_dict()
        print(update_data)
        db_data.update_program_service_name(update_data['service_id'], update_data['program_service_name'])
        db_data.update_relation_program_services_tags(update_data)
        db_data.commit_bd()
        return redirect(f'/reports/settings/program-services/{service[0][0]}')
    return render_template('reports_settings_program_services_page.html', service=service, tags=tags)


@app.route('/reports/settings/program-services/rel', methods=["GET", "POST"])
def change_rel_program_services_services():
    """Таблица с отношением программных услуг к фактическим"""
    if request.method == 'POST':
        db_data.set_services_program_services(request.form.to_dict())
        db_data.commit_bd()
    program_services = db_data.get_program_services_table()
    services_data = db_data.get_services_table()
    return render_template('reports_settings_program_services_rel.html', program_services=program_services,
                           services=services_data)


@app.route('/reports/settings/program-services/tags-services')
def tags_services():
    """Спиок тегов услуг"""
    tags = db_data.get_tags_services()
    return render_template('reports_settings_tags_services.html', tags=tags)


@app.route('/reports/settings/program-services/tags-services/add', methods=['GET', 'POST'])
def add_tag_services():
    if request.method == 'POST':
        db_data.add_tag_service_in_db(request.form.to_dict())
        db_data.commit_bd()
        return redirect('/reports/settings/program-services/tags-services/add')
    return render_template('reports_settings_tags_services_add.html')


@app.route('/reports/settings/program-services/tags-services/<tag_service_id>', methods=['GET', 'POST'])
def tag_service_page(tag_service_id):
    tag = db_data.get_tag_service(tag_service_id)[0]
    if request.method == 'POST':
        db_data.change_tag_in_bd(request.form.to_dict())
        db_data.commit_bd()
        return redirect(f'/reports/settings/program-services/tags-services/{tag_service_id}')
    return render_template('reports_settings_tags_services_page.html', tag=tag, tag_service_id=tag_service_id)


@app.route('/reports/specialists')
def specialists():
    specialists = db_data.get_specialists()
    return render_template('reports_settings_specialists.html', specialists=specialists)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
