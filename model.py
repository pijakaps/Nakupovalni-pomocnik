class Model:
    pass

class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.izdelki = []

    def dodaj_izdelek(self, izdelek):
        self.izdelki.append(izdelek)

class Izdelek:
    def __init__(self, ime, cena_na_kos):
        self.ime = ime
        self.cena = cena_na_kos
        self.kolicina = 0

    def __repr__(self):
        return f"Izdelek({self.ime}, {self.cena})"

    def potrebujem_izdelek(self, kolicina):
        self.kolicina = kolicina

    def kupi_izdelek(self):
        self.kolicina = 0

    def strosek_izdelka(self):
        return self.kolicina * self.cena