from flask import Flask, render_template, request
import random
app = Flask(__name__)


def dobry_szyfr(haslo, ekonomicznosc_0do2):
    wyjscie = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h', 8: 'i', 9: 'j', 10: 'k', 11: 'l',
               12: 'm', 13: 'n', 14: 'o', 15: 'p', 16: 'r', 17: 's', 18: 't', 19: 'u', 20: 'w', 21: 'x', 22: 'y',
               23: 'z', 24: "1", 25: "2", 26: "3", 27: "4", 28: "5", 29: "6", 30: "7", 31: "8", 32: "9", 33: "0",
               34: "!", 35: "#", 36: "$", 37: "%", 38: "^", 39: "&", 40: "*", 41: "(", 42: ")", 43: "_", 44: " "}
    wejscie = {v: k for k, v in wyjscie.items()}
    k = len(haslo) // 2 - 1  # środek
    p_1 = ''  # pierwsza część zamaiany
    p_2 = ''  # druga część zamaiany
    przes = random.randint(0, len(wyjscie) - 1)
    for i in range(k, -1, -1):
        w = (wejscie[haslo[i]] + przes) % (len(wyjscie))
        l = wyjscie[w]
        p_1 += l
    for i in range(len(haslo) - 1, k, -1):
        w = (wejscie[haslo[i]] + przes) % (len(wyjscie))
        l = wyjscie[w]
        p_2 += l
    klucz = wyjscie[przes]
    wiadomosc = p_1 + klucz + p_2  # dodajemy części z kluczem
    """Mod cezar skończony, czas pododawać trochę znaków"""
    sabot = ''    # klucze do usuwania
    if ekonomicznosc_0do2 == 0:  # liczba utrudniaczy
        return wiadomosc + "§"
    elif ekonomicznosc_0do2 == 1:
        liczba_fakeow = random.randint(0, 10)
    else:
        liczba_fakeow = random.randint(10, len(wyjscie) - 1)
    for i in range(liczba_fakeow + 1):
        znak = wyjscie[random.randint(0, len(wyjscie) - 1)]
        klucz = random.randint(0, len(wyjscie) - 1)
        sabot += wyjscie[klucz]
        x = klucz % (len(wiadomosc) + 1)
        wiadomosc = wiadomosc[:x] + znak + wiadomosc[x:]
    wiadomosc = sabot + wiadomosc + wyjscie[liczba_fakeow]
    i = 0
    for j in wiadomosc:
        if j == " ":
            wiadomosc = wiadomosc[:i] + wiadomosc[(i + 1):]
        i += 1
    return wiadomosc


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


if __name__ == "__main__":
    app.run(debug=True)


