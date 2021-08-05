class Stanje:
    def __init__(self):
        self.kategorije = []
        self.aktualna_kategorija = None

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

class Nakup:
    pass

class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.spisek_izdelkov = []
        self.potrebujem = []

    def dodaj_izdelek(self, izdelek):
        self.spisek_izdelkov.append(izdelek)

    def izbrisi_izdelek(self, izdelek):
        self.spisek_izdelkov.remove(izdelek)

class Izdelek:
    def __init__(self, ime, cena_na_kos, kolicina=0, kupljeno=False):
        self.ime = ime
        self.cena = cena_na_kos
        self.kolicina = kolicina
        self.kupljeno = kupljeno

    def __repr__(self):
        return f"Izdelek({self.ime}, {self.cena})"

    def potrebujem(self, kolicina):
        self.kolicina = kolicina

    def kupi(self):
        self.kolicina = 0
        self.kupljeno = True 

    def vrni_na_spisek(self):
        self.kupljeno = False

    def strosek_izdelka(self):
        return self.kolicina * self.cena