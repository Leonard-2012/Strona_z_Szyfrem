import sqlite3 as sql3


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
    "demokracja", "rząd", "prezydent", "parlament","totalitaryzm","Komunizm"

    "energia", "elektryczność", "bateria", "prąd", "napięcie", "siła", "masa", "ruch", "prędkość",
    "czasoprzestrzeń", "planeta", "gwiazda", "galaktyka", "wszechświat",

    "kolor", "czerwony", "niebieski", "zielony", "żółty", "czarny", "biały", "szary", "różowy", "fioletowy",
    "jasny", "ciemny", "ciepły", "zimny",

    "dobry", "zły", "ładny", "brzydki", "szybki", "wolny", "wysoki", "niski", "silny", "słaby",
    "łatwy", "trudny", "prosty", "złożony", "nowy", "stary", "młody", "starszy",

    'melepeta', "Grzegorz Brzęczyszczykiewicz", "Chrząszczyszewoszyce", "Łękołoda", "Grzegorz Braun"
]

if __name__ == '__main__':
    conn = sql3.connect('datas/baza.db')
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS slowa(
    content TEXT NOT NULL)
    """)
    conn.commit()
    for i in slowa:
        cur.execute('INSERT INTO slowa(content) VALUES(?)', (i, ))
        print(i)
    conn.commit()
    conn.close()