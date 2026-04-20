from flask import Flask, render_template, request, redirect, url_for, session
import random
import sqlite3 as sql3

app = Flask(__name__)
app.secret_key = '#Super_wazny_klucz'


def init_db():
    conn, cur = polacz()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS slowa(
        content TEXT NOT NULL
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        login TEXT NOT NULL PRIMARY KEY,
        haslo TEXT NOT NULL,
        poziom INTEGER
    )
    """)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS aktywne_slowa(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()


wejscie = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11, 'm': 12,
           'n': 13, 'o': 14, 'p': 15, 'q': 16, 'r': 17, 's': 18, 't': 19, 'u': 20, 'v': 21, 'w': 22, 'x': 23,
           'y': 24,
           'z': 25, 'A': 26, 'B': 27, 'C': 28, 'D': 29, 'E': 30, 'F': 31, 'G': 32, 'H': 33, 'I': 34, 'J': 35,
           'K': 36,
           'L': 37, 'M': 38, 'N': 39, 'O': 40, 'P': 41, 'Q': 42, 'R': 43, 'S': 44, 'T': 45, 'U': 46, 'V': 47,
           'W': 48,
           'X': 49, 'Y': 50, 'Z': 51, 'ą': 52, 'ć': 53, 'ę': 54, 'ł': 55, 'ń': 56, 'ó': 57, 'ś': 58, 'ż': 59,
           'ź': 60,
           'Ą': 61, 'Ć': 62, 'Ę': 63, 'Ł': 64, 'Ń': 65, 'Ó': 66, 'Ś': 67, 'Ż': 68, 'Ź': 69, '0': 70, '1': 71,
           '2': 72,
           '3': 73, '4': 74, '5': 75, '6': 76, '7': 77, '8': 78, '9': 79, ' ': 80, '!': 81, '"': 82, '#': 83,
           '$': 84,
           '%': 85, '&': 86, "'": 87, '(': 88, ')': 89, '*': 90, '+': 91, ',': 92, '-': 93, '.': 94, '/': 95,
           ':': 96,
           ';': 97, '<': 98, '=': 99, '>': 100, '?': 101, '@': 102, '[': 103, "\\": 104, ']': 105, '^': 106,
           '_': 107,
           '`': 108, '{': 109, '|': 110, '}': 111, '~': 112}
wyjscie = {v: k for k, v in wejscie.items()}


def dobry_szyfr(haslo, ekonomicznosc_0do4):
    global wejscie, wyjscie
    k = len(haslo) // 2  # środek
    przes = random.randint(0, len(wejscie) - 1)
    p_1 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[:k][::-1]
    p_2 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[k:][::-1]
    klucz = wyjscie[przes]
    wiadomosc = p_1 + klucz + p_2  # dodajemy części z kluczem
    """Mod cezar skończony, czas pododawać trochę znaków"""
    klucze = ''  # klucze do usuwania
    if not ekonomicznosc_0do4:
        liczba_zmylek = 0
    elif ekonomicznosc_0do4 == 1:
        liczba_zmylek = random.randint(1, 10)
    elif ekonomicznosc_0do4 == 2:
        liczba_zmylek = random.randint(10, (len(wejscie) - 1) // 2)
    elif ekonomicznosc_0do4 == 3:
        liczba_zmylek = random.randint((len(wejscie) - 1) // 2, (len(wejscie) + 20) // 2)
    else:
        liczba_zmylek = random.randint((len(wejscie) + 20) // 2, len(wejscie) - 1)
    for i in range(liczba_zmylek):
        klucz = random.randint(0, len(wejscie) - 1)
        losowy = wyjscie[random.randint(0, len(wejscie) - 1)]
        id = klucz % len(wiadomosc)
        wiadomosc = wiadomosc[:id] + losowy + wiadomosc[id:]
        klucze = wyjscie[klucz] + klucze
    return klucze + wiadomosc + wyjscie[liczba_zmylek]


def deszyfr_dobry(zaszyfrowane):
    global wejscie, wyjscie
    liczba = wejscie[zaszyfrowane[-1]]
    klucze = zaszyfrowane[:liczba]
    wiadomosc = zaszyfrowane[liczba:][:-1]
    for i in klucze:
        id = wejscie[i] % (len(wiadomosc) - 1)
        wiadomosc = wiadomosc[:id] + wiadomosc[(id+1):]
    x = (len(wiadomosc) - 1) // 2
    cezar = wejscie[wiadomosc[x]]
    wiadomosc = wiadomosc[:x][::-1] + wiadomosc[x + 1:][::-1]
    wynik = ""
    for j in wiadomosc:
        litera = wyjscie[(wejscie[j] - cezar) % len(wejscie)]
        wynik += litera
    return wynik


def na_binarne(n:int):
    wynik = ""
    while n > 0:
        reszta = n % 2
        wynik = str(reszta) + wynik
        n = n // 2
    if not wynik:
        wynik = '0'
    return wynik


def sprawdz_logowanie(login, haslo):
    conn, cur = polacz()
    cur.execute(
        "SELECT * FROM users WHERE login = ?",
        (login, )
    )
    wynik = cur.fetchone()
    conn.close()
    print(haslo, wynik)
    if haslo == wynik[1]:
        wynik = 1
    else:
        wynik = 0
    return wynik


def polacz():
    conn = sql3.connect("datas/baza.db")
    # conn.row_factory = sql3.Row
    cur = conn.cursor()
    return conn, cur


@app.route('/')
def index():
    session['wynik'] = False
    session['odszyfrowane'] = False
    zalogowany = session.get('zalogowany', False)
    return render_template('index.html', status=zalogowany)


@app.route("/test0")
def test0():
    global slowa
    conn, cur = polacz()
    cur.execute("""SELECT * FROM slowa""")
    slowa = cur.fetchall()
    session['poziom'] = 1
    session['slowo'] = random.choice(slowa)[0]
    session['bledy'] = -1
    session['zaszyfrowane'] = dobry_szyfr(session['slowo'], 0)
    cur.execute('INSERT INTO aktywne_slowa(content) VALUES(?)', (session['zaszyfrowane'],))
    conn.commit()
    session['id'] = cur.lastrowid
    conn.close()
    return render_template("test0.html")


@app.route("/test", methods=['GET', 'POST'])
def test():
    global slowa
    if request.method == 'POST':
        odpowiedz = request.form['wiadomosc']
        if odpowiedz == session['slowo']:
            conn, cur = polacz()
            session['poziom'] += 1
            session['bledy'] = 0
            cur.execute("DELETE FROM aktywne_slowa WHERE id = ?", (session['id'], ))
            if session['poziom'] > 5:
                conn.close()
                return render_template('wygrana.html')
            session['slowo'] = random.choice(slowa)[0]
            session['zaszyfrowane'] = dobry_szyfr(session['slowo'], session['poziom'] - 1)
            cur.execute('INSERT INTO aktywne_slowa(content) VALUES(?)', (session['zaszyfrowane'],))
            conn.commit()
            session['id'] = cur.lastrowid
            conn.close()
        else:
            session['bledy'] += 1
            if session['bledy'] > 2:
                conn, cur = polacz()
                cur.execute("DELETE FROM aktywne_slowa WHERE id = ?", (session['id'],))
                conn.close()
                return redirect(url_for('test0'))
        return redirect(url_for('test'))
    return render_template('test.html', poziom=session['poziom'], wiadomosc=session['zaszyfrowane'], bledy=session['bledy'])


@app.route('/cwiczenia_odp', methods=['POST', 'GET'])
def cwiczenia_odp():
    if request.method == 'POST':
        session['poziom'] = int(request.form['poziom'])
        session['szyfr'] = request.form['wiadomosc']
        session['wynik'] = dobry_szyfr(session['szyfr'], session['poziom'])
        return redirect(url_for('cwiczenia_odp'))
    wynik_koniec = session.get('wynik', False)
    return render_template('cwiczenia_odp.html', wynik=wynik_koniec)


@app.route('/deszyfracja_odp', methods=['POST', 'GET'])
def deszyfracja_odp():
    if request.method == 'POST':
        try:
            conn, cur = polacz()
            cur.execute("""SELECT * FROM aktywne_slowa""")
            aktualne = cur.fetchall()
            aktualne_2 = []
            for i in aktualne:
                aktualne_2.append(i[1])
            conn.close()
            session['szyfr'] = request.form['wiadomosc']
            if session['szyfr'] not in aktualne_2:
                session['odszyfrowane'] = deszyfr_dobry(session['szyfr'])
                return redirect(url_for('deszyfracja_odp'))
            else:
                return render_template('oszustwo.html')
        except:
            return render_template('error.html')
    odszyfrowane_koniec = session.get('odszyfrowane', False)
    return render_template('deszyfracja_odp.html', odszyfrowane=odszyfrowane_koniec)


@app.route("/logowanie",  methods=['GET', 'POST'])
def logowanie():
    if request.method == 'POST':
        try:
            if sprawdz_logowanie(request.form['login'], request.form['haslo']):
                session['zalogowany'] = True
                return render_template('administracja.html')
            else:
                return render_template('logowanie.html', zle=1)
        except:
            return render_template('logowanie.html', zle=1)
    else:
        return render_template('logowanie.html', zle=0)


@app.route("/rejestracja")
def rejestracja():
    return render_template('rejestracja.html')


@app.route("/administracja")
def administracja():
    return render_template('administracja.html')


@app.route("/logout")
def logout():
    try:
        session['zalogowany'] = False
    except:
        pass
    return redirect(url_for("index"))
@app.route("/cleanup", methods=["POST"])
def cleanup():
    conn, cur = polacz()
    cur.execute("DELETE FROM aktywne_slowa")
    conn.commit()
    conn.close()
    return "", 204


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
