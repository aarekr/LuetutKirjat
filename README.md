# Luetut kirjat

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)

Sovellus, johon voi merkata tällä hetkellä luettavat, lukulistalla olevat ja luetut kirjat.

* Ohjelmointikieli: Python Flask
* Tietokanta: PostgreSQL

## Asentaminen
* Kloonaa repositorio
* Mene juurihakemistoon
* Luo virtuaaliympäristö:
```bash
python3 -m venv venv
```
* Aktivoi virtuaaliympäristö:
```bash
source venv/bin/activate
```
* Asenna riippuvuudet:
```bash
pip install -r requirements.txt
```
* Luo .env-tiedosto ja lisää sinne PostgreSQL-tietokannan osoite ja salainen avain:
- DATABASE_URL="..."
- SECRET_KEY=...

## Käynnistäminen
```bash
flask run
```

## Testit
* Robot-testit (juurihakemistossa):
```bash
robot src/tests
```

## Pylint
Syötä komento ja tiedoston nimi, esim.:
```bash
python3 -m pylint routes.py
```
