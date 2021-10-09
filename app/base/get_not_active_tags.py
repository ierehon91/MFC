from app.base.data_base_class import Base


def get_not_active_tags(service_id):
    db = Base()

    sql_script_active_tags = f"""SELECT tag_name, fk_program_service FROM tags_services
    LEFT JOIN program_services_tags ON program_services_tags.fk_tag = tags_services.tag_id
    WHERE fk_program_service = {service_id}"""

    active_tags_data = db.consumer_select_script(sql_script_active_tags)
    active_tags = []

    for row in active_tags_data:
        active_tags.append(row[0])

    active_tags = tuple(active_tags)

    sql_script_all_tags = """SELECT tag_name FROM tags_services"""
    all_tags_data = db.consumer_select_script(sql_script_all_tags)
    all_tags = []

    for row in all_tags_data:
        all_tags.append(row[0])

    all_tags = tuple(all_tags)

    not_active_tags = []
    for tag in all_tags:
        if tag not in active_tags:
            not_active_tags.append(tag)
    not_active_tags = tuple(not_active_tags)
    return not_active_tags
