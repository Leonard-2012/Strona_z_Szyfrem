from flask import Flask, render_template, request
import random
app = Flask(__name__)


wejscie = {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7, 'i': 8, 'j': 9, 'k': 10, 'l': 11,
           'm': 12,
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


def kod_cezara(haslo):
    global wejscie, wyjscie
    haslo = list(haslo)
    x = 5
    nowe = list(map(lambda i: wyjscie[(wejscie[i] + x) % len(wejscie)], haslo))
    return "".join(nowe)


def dobry_szyfr(haslo, poziom_szyfracji):
    global wejscie,wyjscie

    k = len(haslo) // 2   # środek
    przes = random.randint(1, len(wejscie) - 1)
    p_1 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[:k][::-1]
    p_2 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[k:][::-1]
    klucz = wyjscie[przes]
    wiadomosc = p_1 + klucz + p_2  # dodajemy części z kluczem
    """Mod cezar skończony, czas pododawać trochę znaków"""
    sabot = ''  # klucze do usuwania
    if poziom_szyfracji == 0:
        liczba_fakeow = 0
    elif poziom_szyfracji == 1:
        liczba_fakeow = random.randint(1, 10)
    elif poziom_szyfracji == 2:
        liczba_fakeow = random.randint(10, len(wejscie) - 1 // 2)
    else:
        liczba_fakeow = random.randint((len(wejscie) - 1) // 2, len(wejscie) - 1)
    for i in range(liczba_fakeow):
        znak = wyjscie[random.randint(0, len(wejscie) - 1)]
        klucz = random.randint(0, len(wejscie) - 1)
        sabot += wyjscie[klucz]
        x = klucz % (len(wiadomosc) + 1)
        wiadomosc = wiadomosc[:x] + znak + wiadomosc[x:]
    wiadomosc = sabot + wiadomosc + wyjscie[liczba_fakeow]
    return wiadomosc


def deszyfr_dobry(zaszyfrowane):
    global wejscie,wyjscie
    klucz = zaszyfrowane[-1]
    klucz = wejscie[klucz]
    wskazowki = zaszyfrowane[:klucz][::-1]  # slicing czy jakoś tak
    wiadomosc = zaszyfrowane[klucz:][:-1]
    for i in wskazowki:
        x = wejscie[i] % len(wiadomosc)
        wiadomosc = wiadomosc[:x] + wiadomosc[(x + 1):]
    x = (len(wiadomosc) - 1) // 2
    print(wiadomosc, x)
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


@app.route("/test")
def test():
    return render_template("test.html")


@app.route('/cwiczenia_odp', methods=['POST'])
def cwiczenia_odp():
    if request.method == 'POST':
        szyfr = request.form['wiadomosc']
        poziom = int(request.form['poziom'])
        wynik = dobry_szyfr(szyfr, poziom)
        return render_template('cwiczenia_odp.html', wynik=wynik)


@app.route('/deszyfracja_pyt')
def deszyfracja_pyt():
    return render_template('deszyfracja_pyt.html')


@app.route('/deszyfracja_odp', methods=['POST'])
def deszyfracja_odp():
    if request.method == 'POST':
        szyfr = request.form['wiadomosc']
        odszyfrowane = deszyfr_dobry(szyfr)
        return render_template('deszyfracja_odp.html', odszyfrowane=odszyfrowane)


if __name__ == "__main__":
    app.run(debug=True)