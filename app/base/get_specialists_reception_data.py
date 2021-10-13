from app.base.data_base_class import Base
from pprint import pprint


def get_specialists_reception_data(first_date, last_date):
    db = Base()
    sql_script = f"""SELECT 
    status_id, status_name, specialist_id, specialist_name,
    
    ((SELECT sum(count_reception) FROM reception_table 
     JOIN program_services ON reception_table.fk_service = program_services.program_service_id
     JOIN program_services_tags ON program_services.program_service_id = program_services_tags.fk_program_service
     JOIN tags_services ON tags_services.tag_id = program_services_tags.fk_tag
     WHERE fk_specialist = specialist_id AND tags_services.tag_id = 2
     AND date_reception >= '{first_date}' AND date_reception <= '{last_date}')
     +
    (SELECT sum(count_reception) FROM reception_table 
     JOIN program_services ON reception_table.fk_service = program_services.program_service_id
     JOIN program_services_tags ON program_services.program_service_id = program_services_tags.fk_program_service
     JOIN tags_services ON tags_services.tag_id = program_services_tags.fk_tag
     WHERE fk_specialist = specialist_id AND tags_services.tag_id = 3
     AND date_reception >= '{first_date}' AND date_reception <= '{last_date}')) as pvd,
    
     (SELECT sum(count_reception) FROM reception_table 
     JOIN program_services ON reception_table.fk_service = program_services.program_service_id
     JOIN program_services_tags ON program_services.program_service_id = program_services_tags.fk_program_service
     JOIN tags_services ON tags_services.tag_id = program_services_tags.fk_tag
     WHERE fk_specialist = specialist_id AND tags_services.tag_id = 1
     AND date_reception >= '{first_date}' AND date_reception <= '{last_date}') as Kapella,
     
     (SELECT count(DISTINCT program_service_id) FROM reception_table 
     JOIN program_services ON reception_table.fk_service = program_services.program_service_id
     JOIN program_services_tags ON program_services.program_service_id = program_services_tags.fk_program_service
     JOIN tags_services ON tags_services.tag_id = program_services_tags.fk_tag
     WHERE fk_specialist = specialist_id
     AND date_reception >= '{first_date}' AND date_reception <= '{last_date}') as types_services,
     
    (SELECT sum(count_reception) FROM reception_table 
     JOIN program_services ON reception_table.fk_service = program_services.program_service_id
     JOIN program_services_tags ON program_services.program_service_id = program_services_tags.fk_program_service
     JOIN tags_services ON tags_services.tag_id = program_services_tags.fk_tag
     WHERE fk_specialist = specialist_id AND tags_services.tag_id = 4
     AND date_reception >= '{first_date}' AND date_reception <= '{last_date}') as dop_services
     
    FROM specialists
    JOIN reception_table ON specialists.specialist_id = reception_table.fk_specialist
    JOIN specialist_statuses ON specialists.fk_status_specialist = specialist_statuses.status_id
    GROUP BY status_id, status_name, specialist_id, specialist_id
    ORDER BY status_id;
    """
    return db.consumer_select_script(sql_script)


def append_row(row):
    return {'status_id': row[0], 'status_name': row[1], 'specialist_id': row[2], 'specialist_name': row[3],
            'pvd': row[4], 'kapella': row[5], 'types': row[6], 'dop': row[7]}


def seporat_tables(first_date, last_date):
    windows = []
    admins = []
    tosp_account = []
    specialists_tosp = []
    specialist_cou = []
    no_work = []
    other = []
    for row in get_specialists_reception_data(first_date, last_date):
        if row[0] in [x for x in range(1, 20 + 1)]:
            windows.append(append_row(row))
        elif row[0] == 21:
            admins.append(append_row(row))
        elif row[0] == 26:
            tosp_account.append(append_row(row))
        elif row[0] == 27:
            specialists_tosp.append(append_row(row))
        elif row[0] == 28:
            specialist_cou.append(append_row(row))
        elif row[0] == 29:
            no_work.append(append_row(row))
        else:
            other.append(append_row(row))
    return {'windows': windows, 'admins': admins, 'tosp_account': tosp_account, 'specialists_tosp': specialists_tosp,
            'specialist_cou': specialist_cou, 'no_work': no_work, 'other': other}


pprint(seporat_tables('2021-10-12', '2021-10-12'))
