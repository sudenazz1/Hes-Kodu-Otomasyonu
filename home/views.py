from django.shortcuts import render, redirect
from .utils import custom_sql_query, authenticate_user, daily_table_list, generate_random_value
import sqlite3
from django.contrib import messages


def home(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        return render(request, 'index.html', {'tc': tc_no})
    else:
        return redirect('login')


def relatives(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_no,)) 
        row = cursor.fetchone() 
        if row: 
            user_id = row[0] 
        else: 
            user_id = None

        error_message = None
        relativeser = []

        if request.method == 'POST':
            tc_relative = request.POST.get('tc')
            cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_relative,))
            row = cursor.fetchone()
            if row:
                relative_id = row[0]
                if relative_id == user_id:
                    error_message = 'Kendinizi ekleyemezsiniz.'
                elif cursor.execute("SELECT relative_users_id2 FROM relative_table WHERE relative_users_id=?", (user_id,)).fetchone() == relative_id:
                    error_message = 'Zaten ekli.'
                else:
                    cursor.execute("INSERT INTO relative_table (relative_users_id, relative_users_id2) VALUES (?, ?)", (user_id, relative_id))
                    connection.commit()
                    return redirect('relatives')
            else:
                error_message = 'Kullanıcı bulunamadı.'

        cursor.execute("SELECT relative_table.id, users_table.tc_no, users_table.first_name, users_table.last_name FROM users_table INNER JOIN relative_table ON users_table.id = relative_table.relative_users_id2 WHERE relative_users_id=?", (user_id,))
        rows = cursor.fetchall()
        for row in rows:
            ids, tc, first_name, last_name = row
            relativeser.append({'tc': tc, 'first_name': first_name, 'last_name': last_name , 'ids': ids})
        connection.close()
        
        context = {'tc': tc_no, 'relatives': relativeser, 'error_message': error_message}
        return render(request, 'relatives.html', context)
    else:
        return redirect('login')

def questionary(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        return render(request, 'questionary.html', {'tc': tc_no})
    else:
        return redirect('login')

def profile(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT tc_no, first_name, last_name, e_mail, phone_no FROM users_table WHERE tc_no=?", (tc_no,))
        row = cursor.fetchone()
        if row:
            tc_no, first_name, last_name, email, phone_no = row
            context = {
                'tc_no': tc_no,
                'first_name': first_name,
                'last_name': last_name,
                'e_mail': email,
                'phone_no': phone_no,
            }
            return render(request, 'profile.html', context)
    else:
        return redirect('login')   

def daily_table(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        context = daily_table_list()
        return render(request, 'daily-table.html', context)
    else:
        return redirect('login')

def get_hes_code(request):
    user_id = None
    hes_code = None
    if 'tc' in request.session:
        tc_no = request.session['tc']
        if request.method == 'POST':
            hes_code = generate_random_value()
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_no,)) 
            row = cursor.fetchone() 
            if row: 
                user_id = row[0] 
            else: 
                user_id = None
            while cursor.execute("SELECT hes_codu FROM hes_codu_table WHERE hes_codu=?", (hes_code,)).fetchone(): 
                hes_code = generate_random_value()
            cursor.execute("INSERT INTO hes_codu_table (hes_users_id, hes_codu,creation_date) VALUES (?, ?, CURRENT_DATE)", (user_id, hes_code))
            connection.commit()
            connection.close()
            return render(request, 'get-hes-code.html', {'tc': tc_no, 'hes_code': hes_code})
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_no,)) 
        row = cursor.fetchone() 
        if row: 
            user_id = row[0] 
        else: 
            user_id = None
        cursor.execute("SELECT creation_date, hes_codu FROM hes_codu_table WHERE hes_users_id=?", (user_id,))
        row = cursor.fetchone()
        if row:
            hes_date = row[0]
            hes_code = row[1]
        cursor.execute("DELETE FROM hes_codu_table WHERE date(creation_date) <= date('now', '-7 day')")
        connection.commit()
        connection.close()
        if hes_code:
            return render(request, 'get-hes-code.html', {'tc': tc_no, 'hes_code': hes_code})
        else:
            return render(request, 'get-hes-code.html', {'tc': tc_no})
    else:
        return redirect('login')

def covidinfo(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']

        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_no,))
        row = cursor.fetchone()
        
        vaccine_info_list = []
        
        if row:
            user_id = row[0]
            
            cursor.execute("SELECT vaccine_table.vaccine_name, vaccine_status_table.vaccine_status_date FROM vaccine_status_table INNER JOIN users_table ON vaccine_status_table.users_id = users_table.id  INNER JOIN vaccine_table ON vaccine_status_table.vaccine_id = vaccine_table.id  WHERE users_table.id =?", (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                vaccine_name, vaccine_status_date = row
                vaccine_info_list.append([vaccine_name, vaccine_status_date])

        return render(request, 'co19-info.html', {'vaccine_info_list': vaccine_info_list, 'tc': tc_no})
    else:
        return redirect('login')






def passport(request):
    if 'tc' in request.session:
        tc_no = request.session['tc']
        return render(request, 'passport.html', {'tc': tc_no})
    else:
        return redirect('login')

def report(request):
    if 'tc' in request.session:
        if request.method == 'POST':
            address = request.POST['address']
            city = request.POST['city']
            county = request.POST['county']
            description = request.POST['description']
            notice_users_id = None
            
            tc_no = request.session['tc']
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()

            cursor.execute("SELECT id FROM users_table WHERE tc_no=?", (tc_no,))
            row = cursor.fetchone()
            if row:
                notice_users_id = row[0]

                cursor.execute("INSERT INTO notice_table (notice_users_id, city, county, address, description) VALUES (?, ?, ?, ?, ?)", 
                                                    (notice_users_id, city, county, address, description))
                connection.commit()
                connection.close()
        return render(request, 'report.html', {'tc': request.session['tc']})
    else:
        return redirect('login')


def login(request):
    if request.method == 'POST':
        tc_no = request.POST.get('tc')
        password = request.POST.get('password')
        if authenticate_user(tc_no, password):
            request.session['tc'] = tc_no
            return redirect('home')
        else:
            error_message = 'Hatalı TC Kimlik Numarası veya Şifre.'
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        tc = request.POST['tc']
        phone = request.POST['phone']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute("SELECT * FROM users_table WHERE tc_no=?", (tc,))
            if cursor.fetchone():
                messages.error(request, 'Bu TC kimlik numarası zaten kayıtlı.')
                connection.close()
                return redirect('register')
            else:
                cursor.execute("INSERT INTO users_table (tc_no, first_name, last_name, e_mail, phone_no, password) VALUES (?, ?, ?, ?, ?, ?)", 
                                                        (tc, firstname, lastname, email, phone, password))
                connection.commit()
                connection.close()
                messages.success(request, 'Başarıyla kayıt oldunuz. Lütfen giriş yapın.')
                return redirect('login')
        else:
            messages.error(request, 'Şifreler eşleşmiyor.')
            return redirect('register')
    else:
        return render(request, 'register.html')

def logout(request):
    if 'tc' in request.session:
        del request.session['tc']
    return redirect('login')

def deleterelative(request):
    if request.method == 'POST':
        relative_id = request.POST.get('relative_id')
        if relative_id:
            connection = sqlite3.connect('db.sqlite3')
            cursor = connection.cursor()
            cursor.execute("DELETE FROM relative_table WHERE id=?",(relative_id,))
            connection.commit()
            connection.close()
    return redirect ('relatives')