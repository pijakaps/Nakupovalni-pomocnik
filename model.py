from datetime import date
import json


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

    def v_slovar(self):
        return {
            "kategorije": [kategorija.v_slovar() for kategorija in self.kategorije],
            "aktualna_kategorija": self.kategorije.index(self.aktualna_kategorija)
            if self.aktualna_kategorija
            else None,
            "nakupi": [nakup.v_slovar() for nakup in self.nakupi],
            "aktualni_nakup": self.nakupi.index(self.aktualni_nakup)
            if self.aktualni_nakup
            else None,
        }

    @staticmethod
    def iz_slovarja(slovar):
        stanje = Stanje()
        stanje.kategorije = [
            Kategorija.iz_slovarja(sl_kategorije) for sl_kategorije in slovar["kategorije"]
        ]
        if slovar["aktualna_kategorija"] is not None:
            stanje.aktualna_kategorija = stanje.kategorije[slovar["aktualna_kategorija"]]
        stanje.nakupi = [
            Nakup.iz_slovarja(sl_nakupa) for sl_nakupa in slovar["nakupi"]
        ]
        if slovar["aktualni_nakup"] is not None:
            stanje.aktualni_nakup = stanje.nakupi[slovar["aktualni_nakup"]]
        return stanje

    def shrani_v_datoteko(self, ime_datoteke):
        with open(ime_datoteke, "w") as dat:
            slovar = self.v_slovar()
            json.dump(slovar, dat)

    @staticmethod
    def preberi_iz_datoteke(ime_datoteke):
        with open(ime_datoteke) as dat:
            slovar = json.load(dat)
            return Stanje.iz_slovarja(slovar)

    def preveri_podatke_nove_kategorije(self, ime):
        napake = {}
        if not ime:
            napake["ime"] = "Ime mora biti neprazno."
        else:
            for kategorija in self.kategorije:
                if kategorija.ime == ime:
                    napake["ime"] = "Ime je že zasedeno."
        return napake


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

    def v_slovar(self):
        return {
            "ime": date.isoformat(self.ime),
            "kupljeni_izdelki": [izdelek.v_slovar() for izdelek in self.kupljeni_izdelki],
        }

    @staticmethod
    def iz_slovarja(slovar):
        nakup = Nakup(slovar["ime"])
        nakup.kupljeni_izdelki = [
            Izdelek.iz_slovarja(sl_izdelki) for sl_izdelki in slovar["izdelki"]
        ]
        return nakup


class Kategorija:
    def __init__(self, ime):
        self.ime = ime
        self.izdelki = []
        self.potrebujem = []

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

    def strosek(self):
        skupaj = 0
        for izdelek in self.izdelki:
            if izdelek.kolicina != 0:
                skupaj += izdelek.strosek_izdelka()
            else:
                pass
        return skupaj

    def stevilo_potrebujem(self):
        potrebujem = 0
        for izdelek in self.izdelki:
            if izdelek.kolicina != 0:
                potrebujem += 1
            else:
                pass
        return potrebujem

    def v_slovar(self):
        return {
            "ime": self.ime,
            "izdelki": [izdelek.v_slovar() for izdelek in self.izdelki],
        }

    @staticmethod
    def iz_slovarja(slovar):
        kategorija = Kategorija(slovar["ime"])
        kategorija.izdelki = [
            Izdelek.iz_slovarja(sl_izdelka) for sl_izdelka in slovar["izdelki"]
        ]
        return kategorija


class Izdelek:
    def __init__(self, ime, cena_na_kos, kolicina=0):
        self.ime = ime
        self.cena = cena_na_kos
        self.kolicina = kolicina

    def __repr__(self):
        return f"Izdelek({self.ime}, {self.cena})"

    def strosek_izdelka(self):
        return self.kolicina * self.cena

    def v_slovar(self):
        return {
            "ime": self.ime,
            "cena_na_kos": self.cena,
            "količina": self.kolicina,
        }

    @staticmethod
    def iz_slovarja(slovar):
        return Izdelek(
            slovar["ime"],
            slovar["cena_na_kos"],
            slovar["količina"],
        )
