from flask import Flask, render_template, request, redirect, url_for
import random
import sqlite3 as sql3

app = Flask(__name__)

conn = sql3.connect('baza.db')
cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS aktywne(
content TEXT NOT NULL)
""")
conn.commit()

slowo = ''
poziom = 0
bledy = 0
zaszyfrowane = ''

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
slowa = [
    "dom", "mieszkanie", "kamienica", "blok", "osiedle", "podwórko", "ogród", "altana", "garaż", "piwnica",
    "strych", "korytarz", "schody", "balkon", "taras", "ogrodzenie", "brama", "furtka", "klucz", "zamek",
    "okno", "firanka", "zasłona", "roleta", "parapet", "drzwi", "klamka", "dywan", "podłoga", "sufit",
    "ściana", "tapeta", "farba", "lampa", "żarówka", "światło", "cień", "gniazdko", "kontakt", "przedłużacz",

    "stół", "krzesło", "kanapa", "sofa", "fotel", "regał", "półka", "szafa", "komoda", "biurko",
    "materac", "kołdra", "poduszka", "koc", "pościel", "ręcznik", "lustro", "wieszak", "kosz", "pudełko",

    "człowiek", "osoba", "kobieta", "mężczyzna", "dziecko", "niemowlę", "nastolatek", "dorosły", "senior",
    "rodzina", "matka", "ojciec", "mama", "tata", "siostra", "brat", "babcia", "dziadek", "wnuk", "wnuczka",
    "kuzyn", "kuzynka", "ciocia", "wujek", "małżeństwo", "para", "znajomy", "kolega", "koleżanka", "przyjaciel",

    "emocja", "radość", "smutek", "złość", "gniew", "strach", "lęk", "nadzieja", "miłość", "zaufanie",
    "zazdrość", "duma", "wstyd", "spokój", "niepokój", "entuzjazm", "motywacja", "satysfakcja",

    "miasto", "wieś", "ulica", "aleja", "plac", "skrzyżowanie", "chodnik", "droga", "autostrada", "most",
    "tunel", "przystanek", "dworzec", "lotnisko", "port", "stacja", "metro", "tramwaj", "autobus", "taksówka",
    "samochód", "ciężarówka", "motocykl", "rower", "hulajnoga", "pociąg", "wagon", "lokomotywa",

    "podróż", "wycieczka", "wakacje", "urlop", "bilet", "rezerwacja", "hotel", "hostel", "pensjonat",
    "mapa", "kompas", "plecak", "walizka", "paszport", "granica", "turysta", "przewodnik",

    "jedzenie", "posiłek", "śniadanie", "obiad", "kolacja", "przekąska", "deser", "zupa", "rosół", "pomidorowa",
    "pierogi", "makaron", "ryż", "kasza", "ziemniaki", "sałatka", "kanapka", "pizza", "hamburger",
    "chleb", "bułka", "masło", "ser", "szynka", "jajko", "mleko", "jogurt", "śmietana", "kefir",

    "jabłko", "banan", "pomarańcza", "mandarynka", "gruszka", "śliwka", "wiśnia", "czereśnia",
    "truskawka", "malina", "borówka", "arbuz", "melon", "ananas", "kiwi",
    "marchew", "cebula", "czosnek", "papryka", "ogórek", "pomidor", "sałata", "kapusta", "brokuł", "kalafior",

    "napój", "woda", "sok", "herbata", "kawa", "kakao", "lemoniada", "oranżada", "koktajl",

    "zwierzę", "pies", "kot", "chomik", "królik", "świnka_morska", "papuga", "kanarek", "żółw",
    "ryba", "koń", "krowa", "świnia", "owca", "koza", "kura", "kogut", "kaczka", "gęś",
    "lew", "tygrys", "pantera", "gepard", "niedźwiedź", "wilk", "lis", "jeleń", "sarna", "dzik",

    "natura", "las", "drzewo", "krzew", "liść", "kora", "korzeń", "kwiat", "trawa", "łąka",
    "pole", "rzeka", "jezioro", "staw", "morze", "ocean", "plaża", "piasek", "skała", "kamień",
    "góra", "dolina", "wzgórze", "jaskinia", "wulkan",

    "pogoda", "słońce", "deszcz", "śnieg", "grad", "burza", "piorun", "wiatr", "mgła", "rosa",
    "temperatura", "upał", "mróz", "chłód", "wilgoć", "susza",

    "czas", "sekunda", "minuta", "godzina", "dzień", "noc", "tydzień", "miesiąc", "rok", "dekada", "wiek",
    "kalendarz", "data", "termin", "harmonogram",

    "szkoła", "przedszkole", "uczeń", "student", "nauczyciel", "profesor", "lekcja", "wykład", "egzamin",
    "sprawdzian", "zadanie", "odpowiedź", "notatka", "zeszyt", "podręcznik", "biblioteka",

    "nauka", "matematyka", "fizyka", "chemia", "biologia", "astronomia", "geografia", "historia",
    "filozofia", "psychologia", "socjologia", "informatyka", "programowanie", "algorytm", "baza_danych",

    "komputer", "laptop", "monitor", "klawiatura", "mysz", "drukarka", "skaner", "router", "serwer",
    "internet", "strona", "aplikacja", "oprogramowanie", "system", "plik", "folder", "hasło", "konto",

    "praca", "zawód", "firma", "biuro", "pracownik", "pracodawca", "szef", "menedżer", "projekt",
    "spotkanie", "raport", "umowa", "pensja", "premia", "awans", "rekrutacja",

    "sport", "piłka", "mecz", "turniej", "liga", "zawodnik", "trener", "stadion", "boisko",
    "bieganie", "pływanie", "jazda", "siłownia", "fitness", "rozgrzewka", "rekord",

    "kultura", "sztuka", "muzyka", "piosenka", "melodia", "instrument", "gitara", "skrzypce", "fortepian",
    "film", "kino", "aktor", "reżyser", "scenariusz", "teatr", "widownia", "wystawa", "galeria",

    "zdrowie", "ciało", "głowa", "ręka", "noga", "serce", "płuca", "mózg", "żołądek", "mięsień",
    "lekarz", "pielęgniarka", "szpital", "klinika", "apteka", "lek", "tabletka", "choroba",
    "gorączka", "ból", "leczenie", "rehabilitacja",

    "państwo", "miasto", "obywatel", "prawo", "ustawa", "konstytucja", "sąd", "policja", "wybory",
    "demokracja", "rząd", "prezydent", "parlament",

    "energia", "elektryczność", "bateria", "prąd", "napięcie", "siła", "masa", "ruch", "prędkość",
    "czasoprzestrzeń", "planeta", "gwiazda", "galaktyka", "wszechświat",

    "kolor", "czerwony", "niebieski", "zielony", "żółty", "czarny", "biały", "szary", "różowy", "fioletowy",
    "jasny", "ciemny", "ciepły", "zimny",

    "dobry", "zły", "ładny", "brzydki", "szybki", "wolny", "wysoki", "niski", "silny", "słaby",
    "łatwy", "trudny", "prosty", "złożony", "nowy", "stary", "młody", "starszy",

    'melepeta', "Grzegorz Brzęczyszczykiewicz", "Chrząszczyszewoszyce", "Łękołoda", "Grzegorz Braun"
]


def dobry_szyfr(haslo, ekonomicznosc_0do3):
    global wejscie, wyjscie
    k = len(haslo) // 2  # środek
    przes = random.randint(0, len(wejscie) - 1)
    p_1 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[:k][::-1]
    p_2 = "".join(list(map(lambda element: wyjscie[(wejscie[element] + przes) % len(wejscie)], haslo)))[k:][::-1]
    klucz = wyjscie[przes]
    wiadomosc = p_1 + klucz + p_2  # dodajemy części z kluczem
    """Mod cezar skończony, czas pododawać trochę znaków"""
    sabot = ''  # klucze do usuwania
    if not ekonomicznosc_0do3:
        liczba_fakeow = 0
    elif ekonomicznosc_0do3 == 1:
        liczba_fakeow = random.randint(1, 10)
    elif ekonomicznosc_0do3 == 2:
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
    global slowo, bledy, poziom, zaszyfrowane
    poziom = 1
    slowo = slowa[random.randint(0, len(slowa) - 1)]
    bledy = -1
    zaszyfrowane = dobry_szyfr(slowo, 0)
    return render_template("test0.html")


@app.route("/test", methods=['GET', 'POST'])
def test():
    global slowo, poziom, bledy, zaszyfrowane
    if request.method == 'POST':
        odpowiedz = request.form['wiadomosc']
        if odpowiedz == slowo:
            poziom += 1
            bledy = 0
            if poziom > 4:
                return render_template('wygrana.html')
            slowo = random.choice(slowa)
            zaszyfrowane = dobry_szyfr(slowo, poziom - 1)
        else:
            bledy += 1
            if bledy > 2:
                return render_template('test0.html')
        return redirect(url_for('test'))
    return render_template('test.html', poziom=poziom, wiadomosc=zaszyfrowane, bledy=bledy)


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
        try:
            szyfr = request.form['wiadomosc']
            odszyfrowane = deszyfr_dobry(szyfr)
            return render_template('deszyfracja_odp.html', odszyfrowane=odszyfrowane)
        except:
            return render_template('error.html')


if __name__ == "__main__":
    app.run(debug=True)
