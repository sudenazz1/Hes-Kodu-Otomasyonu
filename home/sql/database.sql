CREATE TABLE users_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tc_no INT NOT NULL UNIQUE,
    first_name NVARCHAR(20),
    last_name NVARCHAR(20), 
    e_mail NVARCHAR(50), 
    phone_no SMALLINT,
    password NVARCHAR(60)
);

CREATE TABLE vaccine_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    vaccine_name NVARCHAR(20)
);

CREATE TABLE vaccine_status_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    users_id INT,
    vaccine_id INT,
    how_many_vaccine INT,
    vaccine_status_date DATE,
    FOREIGN KEY (users_id) REFERENCES users_table(id),
    FOREIGN KEY (vaccine_id) REFERENCES vaccine_table(id)
);

CREATE TABLE hes_codu_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    hes_users_id INT,
    hes_codu INT,
    creation_date DATE,
    FOREIGN KEY (hes_users_id) REFERENCES users_table(id)
);

CREATE TABLE notice_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    notice_users_id INT,
    city NVARCHAR(20),
    county NVARCHAR(20),
    address NVARCHAR(20),
    description NVARCHAR(50),
    FOREIGN KEY (notice_users_id) REFERENCES users_table(id)
);

CREATE TABLE case_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    case_users_id INT,
    status BOOLEAN,
    case_date DATE,
    FOREIGN KEY (case_users_id) REFERENCES users_table(id)
);

CREATE TABLE death_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    death_users_id INT,
    status BOOLEAN,
    death_date DATE,
    FOREIGN KEY (death_users_id) REFERENCES users_table(id)
);

CREATE TABLE relative_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    relative_users_id INT,
    relative_users_id2 INT,
    FOREIGN KEY (relative_users_id) REFERENCES users_table(id),
    FOREIGN KEY (relative_users_id2) REFERENCES users_table(id)
);
