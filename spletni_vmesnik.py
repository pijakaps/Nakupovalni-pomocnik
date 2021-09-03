import bottle
import os
from datetime import date
from model import Stanje, Kategorija, Nakup, Izdelek


def nalozi_uporabnikovo_stanje():
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    if uporabnisko_ime:
        return Stanje.preberi_iz_datoteke(uporabnisko_ime)
    else:
        bottle.redirect("/prijava/")


def shrani_uporabnikovo_stanje(stanje):
    uporabnisko_ime = bottle.request.get_cookie("uporabnisko_ime")
    stanje.shrani_v_datoteko(uporabnisko_ime)


@bottle.get("/")
def osnovna_stran():
    stanje = nalozi_uporabnikovo_stanje()
    return bottle.template(
        "osnovna_stran.html",
        izdelki=stanje.aktualna_kategorija.izdelki if stanje.aktualna_kategorija else [],
        kategorije=stanje.kategorije,
        aktualna_kategorija=stanje.aktualna_kategorija,
        uporabnisko_ime=bottle.request.get_cookie("uporabnisko_ime"),
    )


@bottle.get("/registracija/")
def registracija_get():
    return bottle.template("registracija.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/registracija/")
def registracija_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime že obstaja."}
        return bottle.template("registracija.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        Stanje().shrani_v_datoteko(uporabnisko_ime)
        bottle.redirect("/")


@bottle.get("/prijava/")
def prijava_get():
    return bottle.template("prijava.html", napake={}, polja={}, uporabnisko_ime=None)


@bottle.post("/prijava/")
def prijava_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    if not os.path.exists(uporabnisko_ime):
        napake = {"uporabnisko_ime": "Uporabniško ime ne obstaja."}
        return bottle.template("prijava.html", napake=napake, polja={"uporabnisko_ime": uporabnisko_ime}, uporabnisko_ime=None)
    else:
        bottle.response.set_cookie(
            "uporabnisko_ime", uporabnisko_ime, path="/")
        bottle.redirect("/")


@bottle.post("/odjava/")
def odjava_post():
    bottle.response.delete_cookie("uporabnisko_ime", path="/")
    print("piškotek uspešno pobrisan")
    bottle.redirect("/")


@bottle.post("/dodaj/")
def dodaj_izdelek():
    ime = bottle.request.forms.getunicode("ime")
    cena = int(bottle.request.forms.getunicode("cena"))
    stanje = nalozi_uporabnikovo_stanje()
    izdelek = Izdelek(ime, cena)
    stanje.dodaj_izdelek(izdelek)
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.get("/dodaj-kategorijo/")
def dodaj_kategorijo_get():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    return bottle.template("dodaj_kategorijo.html", napake={}, polja={}, uporabnisko_ime=uporabnisko_ime)


@bottle.post("/dodaj-kategorijo/")
def dodaj_kategorijo_post():
    uporabnisko_ime = bottle.request.forms.getunicode("uporabnisko_ime")
    ime = bottle.request.forms.getunicode("ime")
    polja = {"ime": ime}
    stanje = nalozi_uporabnikovo_stanje()
    napake = stanje.preveri_podatke_nove_kategorije(ime)
    if napake:
        return bottle.template("dodaj_kategorijo.html", napake=napake, polja=polja, uporabnisko_ime=uporabnisko_ime)
    else:
        kategorija = Kategorija(ime)
        stanje.dodaj_kategorijo(kategorija)
        shrani_uporabnikovo_stanje(stanje)
        bottle.redirect("/")


@bottle.post("/zamenjaj-aktualno-kategorijo/")
def zamenjaj_aktualno_kategorijo():
    print(dict(bottle.request.forms))
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_uporabnikovo_stanje()
    kategorija = stanje.kategorije[int(indeks)]
    stanje.aktualna_kategorija = kategorija
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.post("/potrebujem/")
def potrebujem():
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_uporabnikovo_stanje()
    izdelek = stanje.aktualna_kategorija.izdelki[int(indeks)]
    izdelek.kolicina = int(bottle.request.forms.getunicode("kolicina"))
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.post("/kupi/")
def kupi():
    indeks = bottle.request.forms.getunicode("indeks")
    stanje = nalozi_uporabnikovo_stanje()
    izdelek = stanje.aktualna_kategorija.izdelki[int(indeks)]
    izdelek.kolicina = 0
    shrani_uporabnikovo_stanje(stanje)
    bottle.redirect("/")


@bottle.error(404)
def error_404(error):
    return "Ta stran ne obstaja!"


bottle.run(reloader=True, debug=True)
