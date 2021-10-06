DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS specialist_statuses (
    status_id SERIAL,
    status_name TEXT NOT NULL,
    PRIMARY KEY (status_id)
);

CREATE TABLE IF NOT EXISTS specialists (
    specialist_id SERIAL,
    specialist_name TEXT NOT NULL,
    rating REAL,
    fk_status_specialist INTEGER,
    PRIMARY KEY (specialist_id),
    FOREIGN KEY (fk_status_specialist) REFERENCES specialist_statuses (status_id)
);

CREATE TABLE IF NOT EXISTS group_services (
    group_id SERIAL,
    group_name TEXT NOT NULL,
    PRIMARY KEY (group_id)
);

CREATE TABLE IF NOT EXISTS tags_services (
    tag_id SERIAL,
    tag_name TEXT NOT NULL,
    tag_description TEXT,
    PRIMARY KEY (tag_id)
);

CREATE TABLE IF NOT EXISTS services (
    service_id SERIAL,
    fk_group_service INTEGER,
    service_name TEXT NOT NULL,
    PRIMARY KEY (service_id),
    FOREIGN KEY (fk_group_service) REFERENCES group_services (group_id)
);

CREATE TABLE IF NOT EXISTS program_services (
    program_service_id SERIAL,
    program_service_name TEXT NOT NULL,
    fk_tag_service INTEGER,
    program_service_description TEXT,
    PRIMARY KEY (program_service_id),
    FOREIGN KEY (fk_tag_service) REFERENCES tags_services (tag_id)
);

CREATE TABLE IF NOT EXISTS program_services_tags (
    fk_program_service INTEGER,
    fk_tag INTEGER,
    FOREIGN KEY (fk_program_service) REFERENCES program_services (program_service_id),
    FOREIGN KEY (fk_tag) REFERENCES tags_services (tag_id)
);

CREATE TABLE IF NOT EXISTS services_program_services (
    fk_service INTEGER,
    fk_program_service INTEGER,
    FOREIGN KEY (fk_service) REFERENCES services (service_id),
    FOREIGN KEY (fk_program_service) REFERENCES program_services (program_service_id)
);

CREATE TABLE IF NOT EXISTS reception_table (
    reception_id BIGSERIAL,
    date_reception DATE NOT NULL,
    fk_specialist INTEGER NOT NULL,
    fk_service INTEGER NOT NULL,
    count_reception INTEGER,
    PRIMARY KEY (reception_id),
    FOREIGN KEY (fk_specialist) REFERENCES specialists (specialist_id),
    FOREIGN KEY (fk_service) REFERENCES program_services (program_service_id)
);