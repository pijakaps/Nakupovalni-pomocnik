from model import Stanje, Kategorija, Nakup, Izdelek
from datetime import date

IME_DATOTEKE = "stanje.json"
try:
    moj_model = Stanje.preberi_iz_datoteke(IME_DATOTEKE)
except FileNotFoundError:
    moj_model = Stanje()


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


def prikaz_kategorije(kategorija):
    potrebujem = kategorija.stevilo_potrebujem()
    if potrebujem:
        return f"{kategorija.ime} ({potrebujem}!)"
    else:
        return f"{kategorija.ime} (/)"


def prikaz_izdelka(izdelek):
    if izdelek.kolicina == 0:
        return f"{izdelek.ime}; {izdelek.cena} EUR"
    else:
        return f"{izdelek.ime}; {izdelek.cena} EUR ({izdelek.kolicina}x)"


def prikaz_nakupa(nakup):
    return f"{nakup.ime}: {nakup.strosek} EUR"


def izberi_kategorijo(model):
    return izberi_moznost(
        [
            (kategorija, prikaz_kategorije(kategorija))
            for kategorija in model.kategorije
        ]
    )


def izberi_izdelek(model):
    return izberi_moznost(
        [
            (izdelek, prikaz_izdelka(izdelek))
            for izdelek in model.aktualna_kategorija.izdelki
        ]
    )


def izberi_nakup(model):
    return izberi_moznost(
        [
            (nakup, prikaz_nakupa(nakup))
            for nakup in model.nakupi
        ]
    )


def preberi_ceno():
    while True:
        vnos = input("Cena izdelka na kos> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


def preberi_kolicino():
    while True:
        vnos = input("Količina> ")
        try:
            return int(vnos)
        except ValueError:
            print("Vnesti morate število.")


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
            pobrisi_izdelek()
        elif ukaz == POTREBUJEM_IZDELEK:
            potrebujem_izdelek()
        elif ukaz == KUPI_IZDELEK:
            kupi_izdelek()
        elif ukaz == IZHOD:
            moj_model.shrani_v_datoteko(IME_DATOTEKE)
            print("Nasvidenje!")
            break


def prikazi_pozdravno_sporocilo():
    print("Pozdravljeni!")


def prikazi_aktualno_stanje():
    if moj_model.aktualna_kategorija:
        for izdelek in moj_model.aktualna_kategorija.izdelki:
            print(f"- {prikaz_izdelka(izdelek)}")
    else:
        print("Ker nimate še nobene kategorije, morate ustvariti novo. Primeri kategorij so: HRANA, PIJAČA, OBLAČILA ...")
        dodaj_kategorijo()


def dodaj_kategorijo():
    print("Vnesite podatke, da lahko ustvarite novo kategorijo.")
    ime = input("Ime> ")
    if moj_model.kategorije == []:
        nova_kategorija = Kategorija(ime)
        moj_model.dodaj_kategorijo(nova_kategorija)
    else:
        for kategorija in moj_model.kategorije:
            if kategorija.ime == ime:
                print(
                    "Ta kategorija že obstaja, poskusite ustvariti drugo kategorijo ali storite kaj drugega.")
                tekstovni_vmesnik()
            else:
                pass
        nova_kategorija = Kategorija(ime)
        moj_model.dodaj_kategorijo(nova_kategorija)


def pobrisi_kategorijo():
    if moj_model.kategorije == []:
        print("Trenutno nimate nobene kategorije, zato ustvarite novo.")
        dodaj_kategorijo()
    else:
        kategorija = izberi_kategorijo(moj_model)
        moj_model.pobrisi_kategorijo(kategorija)


def zamenjaj_kategorijo():
    print("Izberite kategorijo, na katero želite preklopiti.")
    kategorija = izberi_kategorijo(moj_model)
    moj_model.zamenjaj_kategorijo(kategorija)


def zamenjaj_nakup():
    print("Izberite nakup, na katerega želite preklopiti.")
    nakup = izberi_nakup(moj_model)
    moj_model.zamenjaj_nakup(nakup)


def dodaj_izdelek():
    print("Vnesite podatke za nov izdelek.")
    ime = input("Ime> ")
    cena_na_kos = preberi_ceno()
    kolicina = 0
    if moj_model.aktualna_kategorija.izdelki == []:
        nov_izdelek = Izdelek(ime, cena_na_kos, kolicina)
        moj_model.dodaj_izdelek(nov_izdelek)
    else:
        for izdelek in moj_model.aktualna_kategorija.izdelki:
            if izdelek.ime == ime:
                print(
                    "Ta izdelek je že na vašem seznamu, poskusite dodati novega ali pa storite kaj drugega.")
                tekstovni_vmesnik()
            else:
                pass
        nov_izdelek = Izdelek(ime, cena_na_kos, kolicina)
        moj_model.dodaj_izdelek(nov_izdelek)


def pobrisi_izdelek():
    if moj_model.aktualna_kategorija.izdelki == []:
        print(
            "V tej kategoriji nimate zabeleženih nobenih izdelkov. Poskusite kaj drugega.")
        tekstovni_vmesnik()
    else:
        izdelek = izberi_izdelek(moj_model)
        moj_model.pobrisi_izdelek(izdelek)


def potrebujem_izdelek():
    if moj_model.aktualna_kategorija.izdelki == []:
        print("V tej kategoriji nimate zabeleženih nobenih izdelkov. Najprej poskusite dodati izdelek.")
        dodaj_izdelek()
    else:
        izdelek = izberi_izdelek(moj_model)
        print("Vnesite podatek o količini, ki jo potrebujete.")
        izdelek.kolicina = preberi_kolicino()
        moj_model.aktualna_kategorija.potrebujem_izdelek(izdelek)


def kupi_izdelek():
    if moj_model.aktualna_kategorija.izdelki == []:
        print("V tej kategoriji nimate zabeleženih nobenih izdelkov. Najprej poskusite dodati izdelek.")
        dodaj_izdelek()
    elif moj_model.aktualna_kategorija.potrebujem == []:
        print("Trenutno ne potrebujete nobenega od izdelkov iz te kategorije. Najprej izberite, kaj potrebujete")
        potrebujem_izdelek()
    else:
        izdelek = izberi_izdelek(moj_model)
        if izdelek not in moj_model.aktualna_kategorija.potrebujem:
            print(
                "Tega izdelka ne potrebujete, zato ga ne morete kupiti. Poskusite storiti kaj drugega.")
            tekstovni_vmesnik()
        else:
            if moj_model.nakupi == []:
                nakup = Nakup()
                moj_model.dodaj_nakup(nakup)
                moj_model.aktualni_nakup.zabelezi_izdelek(izdelek)
            else:
                moj_model.aktualni_nakup = moj_model.nakupi[-1]
                if moj_model.aktualni_nakup.ime == date.today():
                    moj_model.aktualni_nakup.zabelezi_izdelek(izdelek)
                else:
                    nakup = Nakup()
                    moj_model.dodaj_nakup(nakup)
                    moj_model.aktualni_nakup = nakup
                    moj_model.aktualni_nakup.zabelezi_izdelek(izdelek)
            izdelek.kolicina = 0


tekstovni_vmesnik()
