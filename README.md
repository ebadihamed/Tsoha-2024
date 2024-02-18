# Blogisovellus

Suunnitelmana on tehdä sovellus, jolla voi helposti jakaa blogeja, mielipiteitä tai mitä vain tulee mieleen.

Sovelluksen ominaisuuksia:
 - Käyttäjä voi luoda uuden tunnuksen, jonka jälkeen pystyy kirjautua sisään sekä ulos.
 - Etusivulla näytetään julkaistut blogit järjestyksessä niin, että eniten tykkäyksiä saanut blogi on ensimmäisenä ja ..
 - Kaikki voivat nähdä blogit, vaikka eivät olisi kirjautuneet sisään. Kuitenkin blogin luominen ja tykkääminen edellyttää sisäänkirjautumista.
 - Käyttäjä voi etsiä kaikki blogit, joiden osana on annettu sana tai kirjoittajan nimellä.
 - Blogien ominaisuudet:
    - Käyttäjät voivat antaa tykkäyksiä blogeille, ja tykkäysten määrä näkyy blogin alapuolella.
    - Blogin tekijällä on oikeus poistaa ja muokata blogiaan.
    - Blogin alapuolella näkyy julkaisuaika.
 - Ylläpitäjä voi poistaa blogeja ja piilottaa niitä muiden käyttäjien näkyvistä.

Välipalautus 3:

Sovellus on tällä hetkellä 60% valmis. Aion lisätä siihen vielä paljon uusia toimintoja ja tehdä muokkauksia. Tässä on vasta perusversio, koska aikaa ei ollut tarpeeksi. Toivottavasti saan sen valmiiksi ajoissa. Aluksi tietokannassa ei ole mitään blogeja ja siihen kannattaa lisätä pari ja sitten testailla toimintoja.

Käynnistysohjeet:

Luo kansioon .env tiedosto ja määritä sen sisältö seuraavanlaiseksi:
   DATABASE_URL=<tietokannan-paikallinen-osoite>
   SECRET_KEY=<salainen-avain>

Seuraavaksi aktivoi virtuaaliympäristö ja asenna sovelluksen riippuvuudet komennoilla
   $ python3 -m venv venv
   $ source venv/bin/activate
   $ pip install -r ./requirements.txt

Määritä vielä tietokannan skeema komennolla
   $ psql < schema.sql

Nyt voit käynnistää sovelluksen komennolla
   $ flask run

