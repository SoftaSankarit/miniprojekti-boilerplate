## Ohtu miniprojekti viitesovellus

[Projektin Backlog](https://github.com/orgs/SoftaSankarit/projects)

[Työaikakirjanpito](https://docs.google.com/spreadsheets/d/1HUKBMod-LS23XXH-n89fmx3qXItWrgfJhurG-o4Alno/edit?usp=sharing)

[Testikattavuusraportti](https://app.codecov.io/gh/SoftaSankarit/miniprojekti-boilerplate)

[Projektin loppuraportti](https://helsinkifi-my.sharepoint.com/:b:/g/personal/rautiais_ad_helsinki_fi/EVwVIBB-a1hNq41eOt33eoEBOsiygglDlgdG77qx968ZPw?e=lYl7XR)

[![GHA workflow badge](https://github.com/SoftaSankarit/miniprojekti-boilerplate/workflows/CI/badge.svg)](https://github.com/SoftaSankarit/miniprojekti-boilerplate/actions)
[![codecov](https://codecov.io/gh/SoftaSankarit/miniprojekti-boilerplate/graph/badge.svg?token=1HIWHK3N7W)](https://codecov.io/gh/SoftaSankarit/miniprojekti-boilerplate)

### Definition of Done
"Vaatimus on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu, dokumentoitu, integroitu muuhun ohjelmistoon ja viety tuotantoympäristöön."

### Ohjelman asennus- ja käyttöohje

Esivaatimukset: Varmista, että sinulla on Python3 ja PostgreSQL asennettuna tietokoneellesi.

Kloonaa seuraava repositorio koneellesi:
```
git clone https://github.com/SoftaSankarit/miniprojekti-boilerplate.git
```
Luo juurihakemistoon .env-tiedosto ja määritä sen sisältö seuraavasti:
```
DATABASE_URL=<database-local-address>
TEST_ENV=true
SECRET_KEY=<secret-key>
```
Mene projektin juurikansioon ja asennan poetryn riippuvuudet komennolla:
```
poetry install
```
Mene virtuaaliympäristöön komennolla:
```
poetry shell
```
Luo sql-taulukko komennolla:
```
python3 src/db_helper.py
```
Käynnistä sovellus komennolla:
```
python3 src/index.py
```
