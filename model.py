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

    def pobrisi_izdelek(self, izdelek):
        self.aktualna_kategorija.izbrisi_izdelek(izdelek)

    def potrebujem_izdelek(self, izdelek):
        self.aktualna_kategorija.potrebujem_izdelek(izdelek)
    
    def kupi_izdelek(self, izdelek):
        self.aktualna_kategorija.kupi_izdelek(izdelek)

    def dodaj_nakup(self, nakup):
        self.nakupi.append(nakup)
        if not self.aktualni_nakup:
            self.aktualni_nakup = nakup

    def pobrisi_nakup(self, nakup):
        self.nakupi.remove(nakup)

    def zamenjaj_nakup(self, nakup):
        self.aktualni_nakup = nakup

    def zabelezi_izdelek(self, izdelek):
        self.aktualni_nakup.zabelezi_izdelek(izdelek)


class Nakup:
    def __init__(self):
        self.ime = date.today()
        self.kupljeni_izdelki = []

    def __repr__(self):
        return f"Nakup({self.ime})"

    def strosek(self):
        skupaj = 0
        for izdelek in self.kupljeni_izdelki:
            skupaj += izdelek.strosek_izdelka()
        return skupaj

    def zabelezi_izdelek(self, izdelek):
        self.kupljeni_izdelki.append(izdelek)


class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.izdelki = []
        self.potrebujem =[]

    def __repr__(self):
        return f"Kategorija({self.ime})"

    def dodaj_izdelek(self, izdelek):
        self.izdelki.append(izdelek)

    def izbrisi_izdelek(self, izdelek):
        self.izdelki.remove(izdelek)
    
    def potrebujem_izdelek(self, izdelek):
        self.potrebujem.append(izdelek)
    
    def kupi_izdelek(self, izdelek):
        self.potrebujem.remove(izdelek)

    def stevilo_potrebujem(self):
        return len(self.potrebujem)


class Izdelek:
    def __init__(self, ime, cena_na_kos, kolicina=0):
        self.ime = ime
        self.cena = cena_na_kos
        self.kolicina = kolicina

    def __repr__(self):
        return f"Izdelek({self.ime}, {self.cena})"

    def strosek_izdelka(self):
        return self.kolicina * self.cena
