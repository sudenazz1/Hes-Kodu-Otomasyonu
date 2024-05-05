import sqlite3
import random
import string

def generate_random_value():
    all_characters = string.ascii_letters + string.digits
    return ''.join(random.choices(all_characters, k=8))

def custom_sql_query():
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users_table")
    result = cursor.fetchall()
    connection.close()
    return result

def authenticate_user(tc, password):
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT password FROM users_table WHERE tc_no=?", (tc,))
        row = cursor.fetchone()
        if row:
            db_password = row[0]
            if password == db_password:
                return True
    except Exception as e:
        print("Error:", e)
    finally:
        cursor.close()
        connection.close()
    return False

def daily_table_list():
    vaka = 0
    olum = 0
    gunluk_vaka = 0
    gunluk_olum = 0
    doz1 = 0
    doz2 = 0
    doz3 = 0
    doztoplam = 0
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(status) FROM case_table WHERE status = 1")
    row = cursor.fetchone()
    if row:
        vaka = row[0]
    cursor.execute("SELECT COUNT(status) FROM death_table WHERE status = 1")
    row = cursor.fetchone()
    if row:
        olum = row[0]
    cursor.execute("SELECT COUNT(status) FROM case_table WHERE status = 1 AND case_date = CURRENT_DATE")
    row = cursor.fetchone()
    if row:
        gunluk_vaka = row[0]
    cursor.execute("SELECT COUNT(status) FROM death_table WHERE status = 1 AND death_date = CURRENT_DATE")
    row = cursor.fetchone()
    if row:
        gunluk_olum = row[0]
    cursor.execute("SELECT COUNT(how_many_vaccine) FROM vaccine_status_table WHERE how_many_vaccine = 1")
    row = cursor.fetchone()
    if row:
        doz1 = row[0]
    cursor.execute("SELECT COUNT(how_many_vaccine) FROM vaccine_status_table WHERE how_many_vaccine = 2")
    row = cursor.fetchone()
    if row:
        doz2 = row[0]
    cursor.execute("SELECT COUNT(how_many_vaccine) FROM vaccine_status_table WHERE how_many_vaccine = 3")
    row = cursor.fetchone()
    if row:
        doz3 = row[0]
    cursor.execute("SELECT COUNT(*) FROM vaccine_status_table")
    row = cursor.fetchone()
    if row:
        doztoplam = row[0]
    connection.close()
    context = {
        'toplam_vaka': vaka,
        'toplam_olum': olum,
        'gunluk_vaka': gunluk_vaka,
        'gunluk_olum': gunluk_olum,
        'doz1': doz1,
        'doz2': doz2,
        'doz3': doz3,
        'doztoplam': doztoplam,
    }
    return context



