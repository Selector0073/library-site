from django.shortcuts import render, redirect
from .forms import LoginForm
from django.db import connection
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import hashlib, base64

def login(request):
    error1 = '' #Data is not valid
    error3 = '' #Prohibited symbols
    error4 = '' #user isnt exist

    password = "!QNFA6UqRcUs6dAU1&DoppCBF8dydeRI%p5EazolFl$!j5N^!sVZu&kBz!dD@LNgVVoKakk4Cw&BzS7W503jsZCqRVJNeHjEiJTn!FR$toIyS!Jw*4zAYQoHNFn4bnhmNvopL5xpvD%hvYzVU*jlaY4@#KxVicwZ@B9mL#Ho3XJOFcd8HU@49Uv^tZfCcSEBF$xE8CtzhaEnhQzjb0f8I2oxtD9x65mHVXfQw3I4Z8&*WyXMsPgbaLIYMw4wXI3h"
    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    f = Fernet(key)

    expdat = datetime.now().strftime("%Y-%m-%d")

    cookieu = request.COOKIES.get('library-u')
    cookied = request.COOKIES.get('library-d')

    if "library-u" in request.COOKIES and "library-d" in request.COOKIES:
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM login_login WHERE username = %s;",
                [cookieu]
            )
            cek = cursor.fetchone()
            if cek:
                cek = ema[0]
        if cek > 0:
            decryptedd = f.decrypt(cookied.encode()).decode()

            date1 = datetime.strptime(decryptedd, "%Y-%m-%d")
            date2 = datetime.strptime(expdat, "%Y-%m-%d")

            if date2 >= date1 + timedelta(days=30):
                pass
            else: 
                encrypted = f.encrypt(expdat.encode()).decode()
                response = redirect("/show")
                response.set_cookie("library-d", encrypted)
                return response
    else:
        if request.method == 'POST':
            if LoginForm(request.POST).is_valid():
                usern = request.POST.get('username')
                ema = request.POST.get('email')
                pasw = request.POST.get('passw')
                blacklist = ['$', '%', '#', '"', "'", '(', ')', '[', ']', '{', '}', ':', ';', '<', '>', '?', ',']

                encryptedp = f.encrypt(pasw.encode()).decode()
                encryptedd = f.encrypt(expdat.encode()).decode()

                if any(ch in usern for ch in blacklist) or any(ch in ema for ch in blacklist) or any(ch in pasw for ch in blacklist):
                    error3 = 'Prohibited symbols: ' + ', '.join(blacklist)
                else:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT COUNT(*) FROM login_login WHERE username = %s AND email = %s AND passw = %s;",
                            [usern, ema, encryptedp]
                        )
                        count = cursor.fetchone()[0]
                    if count == 1:
                        error4 = 'User does not exist.' 
                    else:
                        response = redirect('/show')
                        response.set_cookie("library-u", usern)
                        response.set_cookie("library-d", encryptedd)
                        return response
            else:
                error1 = 'Data is not valid'

    form = LoginForm()

    data = {
        'form': form,
        'error1': error1,
        'error3': error3,
        'error4': error4
    }

    return render(request, 'login/profile.html', data)





def reg(request):
    error1 = '' #Data is not valid
    error3 = '' #Prohibited symbols
    error4 = '' #user is exist

    password = "!QNFA6UqRcUs6dAU1&DoppCBF8dydeRI%p5EazolFl$!j5N^!sVZu&kBz!dD@LNgVVoKakk4Cw&BzS7W503jsZCqRVJNeHjEiJTn!FR$toIyS!Jw*4zAYQoHNFn4bnhmNvopL5xpvD%hvYzVU*jlaY4@#KxVicwZ@B9mL#Ho3XJOFcd8HU@49Uv^tZfCcSEBF$xE8CtzhaEnhQzjb0f8I2oxtD9x65mHVXfQw3I4Z8&*WyXMsPgbaLIYMw4wXI3h"
    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    f = Fernet(key)

    if request.method == 'POST':
        if LoginForm(request.POST).is_valid():
            usern = request.POST.get('username')
            ema = request.POST.get('email')
            pasw = request.POST.get('passw')
            expdat = datetime.now().strftime("%Y-%m-%d")
            blacklist = ['$', '%', '#', '"', "'", '(', ')', '[', ']', '{', '}', ':', ';', '<', '>', '?', ',']

            encryptedp = f.encrypt(pasw.encode()).decode()

            if any(ch in usern for ch in blacklist) or any(ch in ema for ch in blacklist) or any(ch in pasw for ch in blacklist):
                error3 = 'Prohibited symbols: ' + ', '.join(blacklist)
            else:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT COUNT(*) FROM login_login WHERE username = %s OR email = %s;",
                        [usern, ema]
                    )
                    count = cursor.fetchone()[0]
                if count > 0:
                    error4 = 'User already exists'
                else:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "INSERT INTO login_login (username, email, passw, expdate) VALUES (%s, %s, %s, %s);",
                            [usern, ema, encryptedp, expdat]
                        )
                    redirect('/login')
        else:
            error1 = 'Data is not valid'


    form = LoginForm()

    data = {
        'form': form,
        'error1': error1,
        'error3': error3,
        'error4': error4
    }

    return render(request, 'login/reg.html', data)









def show(request):
    status = ''
    password = "!QNFA6UqRcUs6dAU1&DoppCBF8dydeRI%p5EazolFl$!j5N^!sVZu&kBz!dD@LNgVVoKakk4Cw&BzS7W503jsZCqRVJNeHjEiJTn!FR$toIyS!Jw*4zAYQoHNFn4bnhmNvopL5xpvD%hvYzVU*jlaY4@#KxVicwZ@B9mL#Ho3XJOFcd8HU@49Uv^tZfCcSEBF$xE8CtzhaEnhQzjb0f8I2oxtD9x65mHVXfQw3I4Z8&*WyXMsPgbaLIYMw4wXI3h"
    key = base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())
    f = Fernet(key)

    cookieu = request.COOKIES.get('library-u')

    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT Email FROM login_login WHERE Username = %s;",
            [cookieu]
        )
        ema = cursor.fetchone()
        if ema:
            ema = ema[0]

    print(cookieu)
    if request.method == "POST":
        status = request.POST.get("status")
        print("Status:", status)
        if status == "confirmed":
            response = redirect('/login')
            response.delete_cookie('library-u')
            response.delete_cookie('library-d')
            return response

    
    data = {
        'usernm': cookieu,
        'ema': ema
    }

    return render(request, 'login/show.html', data)