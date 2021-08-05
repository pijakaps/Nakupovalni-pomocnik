from datetime import date

class Stanje:
    def __init__(self):
        self.kategorije = []
        self.aktualna_kategorija = None
        self.nakupi = []
        self.aktualni_nakup = None

    def dodaj_kategorijo(self, kategorija):
        self.kategorije.append(kategorija)
        if not self.aktualna_kategorija:
            self.aktualna_kategorija = kategorija

    def pobrisi_kategorijo(self, kategorija):
        self.kategorije.remove(kategorija)

    def zamenjaj_kategorijo(self, kategorija):
        self.aktualna_kategorija = kategorija

    def dodaj_izdelek(self, izdelek):
        self.aktualna_kategorija.dodaj_izdelek(izdelek)

    def pobrisi_opravilo(self, izdelek):
        self.aktualna_kategorija.izbrisi_izdelek(izdelek)

    def dodaj_nakup(self, nakup):
        self.nakupi.append(nakup)
        if not self.aktualni_nakup:
            self.aktualni_nakup = nakup

    def pobrisi_nakup(self, nakup):
        self.nakupi.remove(nakup)

    def zamenjaj_nakup(self, nakup):
        self.aktualni_nakup = nakup

    def zabelezi_izdelek(self, izdelek):
        self.aktualni_nakup.dodaj_izdelek(izdelek)

class Nakup:
    def __init__(self):
        self.datum = date.today()
        self.kupljeni_izdelki = []

    def strosek(self):
        skupaj = 0
        for izdelek in self.kupljeni_izdelki:
            skupaj += izdelek.strosek_izdelka
        return skupaj 

    def zabelezi_izdelek(self, izdelek):
        self.kupljeni_izdelki.append(izdelek)

class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.spisek_izdelkov = []
        self.potrebujem_izdelke = []

    def dodaj_izdelek(self, izdelek):
        self.spisek_izdelkov.append(izdelek)

    def izbrisi_izdelek(self, izdelek):
        self.spisek_izdelkov.remove(izdelek)

    def potrebujem(self, izdelek):
        self.spisek_izdelkov.remove(izdelek)
        self.potrebujem_izdelke.append(izdelek)

    def kupi(self, izdelek):
        self.potrebujem_izdelke.remove(izdelek)
        self.spisek_izdelkov.append(izdelek)

class Izdelek:
    def __init__(self, ime, cena_na_kos, kolicina=0, kupljeno=False):
        self.ime = ime
        self.cena = int(cena_na_kos)
        self.kolicina = kolicina
        self.kupljeno = kupljeno

    def __repr__(self):
        return f"Izdelek({self.ime}, {self.cena})"

    def potrebujem(self, kolicina):
        self.kolicina = kolicina

    def kupi(self):
        self.kupljeno = True 

    def vrni_na_spisek(self):
        self.kolicina = 0
        self.kupljeno = False

    def strosek_izdelka(self):
        return self.kolicina * self.cena