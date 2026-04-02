from flask import Flask, render_template, request, redirect, url_for
import random
import sqlite3 as sql3

app = Flask(__name__)

'''Baza sqla'''
conn = sql3.connect('datas/baza.db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS slowa(
content TEXT NOT NULL)
""")
cur.execute("""
CREATE TABLE IF NOT EXISTS admini(
login TEXT NOT NULL,
haslo TEXT NOT NULL)
""")
conn.commit()
conn.close()

conn = sql3.connect('datas/aktywne.db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS aktywne_slowa(
id INTEGER PRIMARY KEY AUTOINCREMENT,
content TEXT NOT NULL)
""")

''' ZMIENNE '''
slowo = ''
poziom = 0
bledy = 0
zaszyfrowane = ''
id = 0

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
    sabot = ''  # klucze do usuwania
    if not ekonomicznosc_0do4:
        liczba_fakeow = 0
    elif ekonomicznosc_0do4 == 1:
        liczba_fakeow = random.randint(1, 10)
    elif ekonomicznosc_0do4 == 2:
        liczba_fakeow = random.randint(10, len(wejscie) - 1 // 2)
    elif ekonomicznosc_0do4 == 3:
        liczba_fakeow = random.randint((len(wejscie) - 1) // 2, (len(wejscie) + 20) // 2)
    else:
        liczba_fakeow = random.randint((len(wejscie) + 20) // 2, len(wejscie) - 1)
    for i in range(liczba_fakeow):
        znak = wyjscie[random.randint(0, len(wejscie) - 1)]
        klucz = random.randint(0, len(wejscie) - 1)
        sabot += wyjscie[klucz]
        x = klucz % len(wiadomosc)
        wiadomosc = wiadomosc[:x] + znak + wiadomosc[x:]
    wiadomosc = sabot + wiadomosc + wyjscie[liczba_fakeow]
    return wiadomosc


def deszyfr_dobry(zaszyfrowane):
    global wejscie, wyjscie
    klucz = zaszyfrowane[-1]
    klucz = wejscie[klucz]
    wskazowki = zaszyfrowane[:klucz][::-1]  # slicing czy jakoś tak
    wiadomosc = zaszyfrowane[klucz:][:-1]
    for i in wskazowki:
        x = wejscie[i] % len(wiadomosc)
        wiadomosc = wiadomosc[:x] + wiadomosc[(x + 1):]
    x = (len(wiadomosc) - 1) // 2
    # faki usunięte
    cezar = wejscie[wiadomosc[x]]
    wiadomosc = wiadomosc[:x][::-1] + wiadomosc[x + 1:][::-1]
    wynik = ""
    for j in wiadomosc:
        litera = wyjscie[(wejscie[j] - cezar) % len(wejscie)]
        wynik += litera
    return wynik


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/cwiczenia_pyt')
def cwiczenia_pyt():
    return render_template('cwiczenia_pyt.html')


@app.route("/test0")
def test0():
    global slowo, bledy, poziom, zaszyfrowane, slowa, id
    conn = sql3.connect('datas/baza.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM slowa""")
    slowa = cur.fetchall()
    conn.close()
    poziom = 1
    slowo = random.choice(slowa)[0]
    bledy = -1
    conn = sql3.connect('datas/aktywne.db')
    cur = conn.cursor()
    zaszyfrowane = dobry_szyfr(slowo, 0)
    cur.execute('INSERT INTO aktywne_slowa(content) VALUES(?)', (zaszyfrowane,))
    conn.commit()
    id = cur.lastrowid
    conn.close()
    return render_template("test0.html")


@app.route("/test", methods=['GET', 'POST'])
def test():
    global slowo, poziom, bledy, zaszyfrowane, id
    if request.method == 'POST':
        odpowiedz = request.form['wiadomosc']
        if odpowiedz == slowo:
            conn = sql3.connect('datas/aktywne.db')
            cur = conn.cursor()
            poziom += 1
            bledy = 0
            cur.execute("DELETE FROM aktywne_slowa WHERE id = ?", (id,))
            if poziom > 5:
                conn.close()
                return render_template('wygrana.html')
            slowo = random.choice(slowa)[0]
            zaszyfrowane = dobry_szyfr(slowo, poziom - 1)
            cur.execute('INSERT INTO aktywne_slowa(content) VALUES(?)', (zaszyfrowane,))
            conn.commit()
            id = cur.lastrowid
            conn.close()
        else:
            bledy += 1
            if bledy > 2:
                conn = sql3.connect('datas/aktywne.db')
                cur = conn.cursor()
                poziom += 1
                bledy = 0
                cur.execute("DELETE FROM aktywne_slowa WHERE id = ?", (id,))
                conn.close()
                return render_template('test0.html')
        return redirect(url_for('test'))
    return render_template('test.html', poziom=poziom, wiadomosc=zaszyfrowane, bledy=bledy)


@app.route('/cwiczenia_odp', methods=['POST'])
def cwiczenia_odp():
    if request.method == 'POST':
        poziom = int(request.form['poziom'])
        szyfr = request.form['wiadomosc']
        wynik = dobry_szyfr(szyfr, poziom)
        return render_template('cwiczenia_odp.html', wynik=wynik)


@app.route('/deszyfracja_pyt')
def deszyfracja_pyt():
    return render_template('deszyfracja_pyt.html')


@app.route('/deszyfracja_odp', methods=['POST'])
def deszyfracja_odp():
    if request.method == 'POST':
        try:
            conn = sql3.connect('datas/aktywne.db')
            cur = conn.cursor()
            cur.execute("""SELECT * FROM aktywne_slowa""")
            aktualne = cur.fetchall()
            print(aktualne)
            aktualne_2 = []
            for i in aktualne:
                aktualne_2.append(i[1])
            conn.close()
            szyfr = request.form['wiadomosc']
            if szyfr not in aktualne_2:
                odszyfrowane = deszyfr_dobry(szyfr)
                return render_template('deszyfracja_odp.html', odszyfrowane=odszyfrowane)
            else:
                return render_template('oszustwo.html')
        except:
            return render_template('error.html')


@app.route("/cleanup", methods=["POST"])
def cleanup():
    conn = sql3.connect('datas/aktywne.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM aktywne_slowa")
    conn.commit()
    conn.close()
    return "", 204


if __name__ == "__main__":
    app.run(debug=True)
