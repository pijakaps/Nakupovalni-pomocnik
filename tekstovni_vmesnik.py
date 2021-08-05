from model import Stanje, Kategorija, Nakup, Izdelek


DODAJ_KATEGORIJO = 1
POBRISI_KATEGORIJO = 2
ZAMENJAJ_KATEGORIJO = 3
ZAMENJAJ_NAKUP = 4
DODAJ_IZDELEK = 5
IZBRISI_IZDELEK = 6
POTREBUJEM_IZDELEK = 7
KUPI_IZDELEK = 8
IZHOD = 9


def preberi_stevilo():
    while True:
        vnos = input("> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def izberi_moznost(moznosti):
    for i, (_moznost, opis) in enumerate(moznosti, 1):
        print(f"{i}) {opis}")
    while True:
        i = preberi_stevilo()
        if 1 <= i <= len(moznosti):
            moznost, _opis = moznosti[i - 1]
            return moznost
        else:
            print(f"Vnesti morate število med 1 in {len(moznosti)}.")


def tekstovni_vmesnik():
    prikazi_pozdravno_sporocilo()
    while True:
        prikazi_aktualno_stanje()
        ukaz = izberi_moznost(
            [
                (DODAJ_KATEGORIJO, "dodaj novo kategorijo"),
                (POBRISI_KATEGORIJO, "pobriši kategorijo"),
                (ZAMENJAJ_KATEGORIJO, "prikaži drugo kategorijo"),
                (ZAMENJAJ_NAKUP, "prikaži drug nakup"),
                (DODAJ_IZDELEK, "dodaj nov izdelek"),
                (IZBRISI_IZDELEK, "izbriši izdelek"),
                (POTREBUJEM_IZDELEK, "potrebujem izdelek"),
                (KUPI_IZDELEK, "kupi izdelek"),
                (IZHOD, "zapri program"),
            ]
        )
        if ukaz == DODAJ_KATEGORIJO:
            dodaj_kategorijo()
        elif ukaz == POBRISI_KATEGORIJO:
            pobrisi_kategorijo()
        elif ukaz == ZAMENJAJ_KATEGORIJO:
            zamenjaj_kategorijo()
        elif ukaz == ZAMENJAJ_NAKUP:
            zamenjaj_nakup()
        elif ukaz == DODAJ_IZDELEK:
            dodaj_izdelek()
        elif ukaz == IZBRISI_IZDELEK:
            izbrisi_izdelek()
        elif ukaz == POTREBUJEM_IZDELEK:
            potrebujem_izdelek()
        elif ukaz == KUPI_IZDELEK:
            kupi_izdelek()
        elif ukaz == IZHOD:
            print("Nasvidenje!")
            break


tekstovni_vmesnik()
