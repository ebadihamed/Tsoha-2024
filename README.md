# Blogisovellus

Suunnitelmana on tehdä sovellus, jolla voi helposti jakaa blogeja, mielipiteitä tai mitä vain tulee mieleen.

Sovelluksen ominaisuuksia:
 - Käyttäjä voi luoda uuden tunnuksen, jonka jälkeen pystyy kirjautua sisään sekä ulos.
 - Etusivulla näytetään julkaistut blogit järjestyksessä niin, että uusin blogi on ensimmäisenä.
 - Kaikki voivat nähdä blogit, vaikka eivät olisi kirjautuneet sisään. Kuitenkin blogin luominen ja tykkääminen edellyttää sisäänkirjautumista.
 - Käyttäjä voi etsiä kaikki blogit, joiden osana on annettu sana tai kirjoittajan nimellä.
 - Blogien ominaisuudet:
    - Käyttäjät voivat antaa tykkäyksiä blogeille, ja tykkäysten määrä näkyy blogin alapuolella.
    - Blogin tekijällä on oikeus poistaa ja muokata blogiaan.
    - Blogin alapuolella näkyy julkaisuaika.
 - Ylläpitäjä voi poistaa blogeja ja piilottaa niitä muiden käyttäjien näkyvistä.

Käynnistysohjeet:

Luo kansioon .env tiedosto ja määritä sen sisältö seuraavanlaiseksi:
```
DATABASE_URL=(tietokannan-paikallinen-osoite)
SECRET_KEY=(salainen-avain)
```

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r ./requirements.txt
```

Määritä vielä tietokannan skeema komennolla
```
$ psql < schema.sql
```
Nyt voit käynnistää sovelluksen komennolla
```
$ flask run
```
