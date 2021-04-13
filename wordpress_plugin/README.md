# Sotetie Hakutyökalu
Hakutyökalu käy hakemassa https://opintopolku.fi/swagger/ API rajapinnasta kurssit ja niiden tiedot. Postinumerot ja kunta tiedot ovat posti.fi sivuilta saatuja tietoja ja muokattu oikeaan muotoon.
## Vaatimukset & Infoa
Asennusohjeet ovat Debian pohjaisille Linux Distribuutioille.
Tarkista mikä Python versio on asennettuna valmiina, tämä sovellus tarvitsee vähintään Python 3.6.0
Python version voit tarkistaa komennolla:
python3 -V
Mikäli asennettuna on pienempi versio kuin 3.6.0, niin suorita nämä komennot
```
sudo apt update
sudo apt upgrade
```
Nyt kokeile uudelleen. Mikäli ei vieläkään toimi (mikäli python versio ei vieläkään näy) niin kannattaa rakentaa lähdekoodista oma Python
https://realpython.com/installing-python/#how-to-build-python-from-source-code



Asennetaan NGINX, jotta voimme käyttää tämän Reverse Proxyä hyödyksi.
```
sudo apt-get install nginx
```

Asennetaan MariaDB
```
sudo apt-get install mariadb-server
```
Asennetaan uWSGI vaatimukset API rajapinnalle ja virtualenviromentti
```
sudo apt install python3-venv python3-pip python3-dev build-essential libssl-dev libffi-dev python3-setuptools
```
Ja viimeisenä kloonataan sovellus home kansioon
```
git clone https://github.com/dss285/sotetie-hakutyokalu
```


## Wordpress Plugin
Zippaa sotetie-hakutyokalu/wordpress_plugin/, ja mene wordpressin hallintasivulle asentamaan zipin avulla pluginia.
Plugini lisää oman sivun hallintapaneeliin, josta voidaan kondiguroida asetuksia.

## Tietokanta
Suorita komento
`sudo mysql`
päästäksesi hallinnoimaan tietokantaa.

```sql
CREATE DATABASE sotetie2021;
CREATE USER sotetie@localhost IDENTIFIED BY ‘salasana’;
GRANT ALL ON sotetie2021.* TO sotetie@localhost;
```

Tämän jälkeen on tietokannan osalta kaikki on kunnossa.
Sovellus itse ottaa yhteyden tietokantaan ja lisää sisällön.

## API
Luodaan kotihakemistoon virtuaaliympäristö Pythonille esimerkiksi.
Tämä komento luo `sotetie2021venv` nimisen kansion, jossa sijaitsee virtuaaliympäristön tiedostot.
```
python3 -m venv sotetie2021venv
```
Aktivoidaan virtuaaliympäristö komennolla
```
source sotetie2021venv/bin/activate
```
Mennään jo aikaisemmin kloonattuun repositoryyn, joka on vakiona nimellä `sotetie-hakutyokalu`.
```
cd sotetie-hakutyokalu
```

Asennetaan vaaditut python moduulit, jotka on jo valmiiksi `api/reqs.txt` tiedostossa.
```
python3 -m pip install -r api/reqs.txt
```
Muokkaa `api/asetukset.py` tiedostosta esimerkiksi nanolla:
`nano api/asetukset.py`
```
palvelin  - Tietokannan osoite, jos samalla koneella niin localhost
kayttaja – Käyttäjä millä on oikeudet luotuun tietokantaan, tietokanta osion mukaan sotetie
salasana – Käyttäjän salasana. Tietokanta osion mukaan ’salasana’. VAIHDA EHDOTTOMASTI
tietokanta – Tietokannan nimi. Tietokanta osion mukaan ’sotetie2021’
```
Käynnistetään alustus, voi laittaa & merkin loppuun tehdäkseen siitä taustalla toimivan ja tämän jälkeen voi siirtyä vaikka NGINX konfigurointiin.
Alustus kestää ~5 min
```
python3 api/alustus.py     - Tässä pyörivä
python3 api/alustus.py &   - Taustalla pyörivä
```
Huomaa, että jos muokkasit välissä NGINX konfiguraatiota, niin nyt mene takaisin repositoryn kansioon. `cd ~/sotetie-hakutyokalu` 
Alustuksen jälkeen, muokkaa api/api.ini tiedostoa, ja muokkaa tänne virtuaaliympäristön paikka.
`nano api/api.ini`
```
[uwsgi]
module = wsgi:app
master = true
processes = 2
virtualenv = /home/KAYTTAJAKENENHOMEKANSIOONKLOONATTU/VIRTUAALIYMPÄRISTÖ
socket = api.sock
chmod-socket = 666
vacuum = true

die-on-term = true
```
Esimerkiksi:
```
[uwsgi]
module = wsgi:app
master = true
processes = 2
virtualenv = /home/tommi/sotetie2021venv
socket = api.sock
chmod-socket = 666
vacuum = true

die-on-term = true
```
Tämän jälkeen voidaan aloittaa käynnistäminen.
Käynnistä uWSGI sovellus, jos olet repositoryn kansiossa, niin pitää mennä apin kansioon, missä on myös api.ini
```
cd api/
uwsgi --ini api.ini
```


## NGINX
Mene kansioon /etc/nginx/sites-enabled/
```
cd /etc/nginx/sites-enabled/
```
Varmuuskopioidaan vanha konfiguraatiotiedosto
```
sudo cp default ../default.bak
```
Muokataan default tiedostoa, nyt esimerkiksi nanolla.
`sudo nano default`
```
server {
listen 80 default_server;
listen [::]:80 default_server;
root /var/www/html;
index index.html index.htm index.nginx-debian.html
server_name _;
location / {
      try_files $uri $uri/ =404;
   }
}

```
Tiedosto muokataan tälläisen näköiseksi.
Muokkaa uwsgi_passissa oleva tiedostolokaatio oikeaksi. `api.sock` tiedosto tulee siihen kansioon, missä `api.ini` sijaitsee, vakiona `api/` kansio
```python
server {
listen 80 default_server;
listen [::]:80 default_server;

server_name _;
        location / {
         include uwsgi_params;
         uwsgi_pass unix:/home/tommi/sotetie-hakutyokalu/api/api.sock;
         uwsgi_intercept_errors on;
      }
}
```

Konfiguraation muutoksen jälkeen testataan.
```
sudo nginx -t
```
Jos testaus menee läpi, niin käynnistetään NGINX uudelleen
```
sudo systemctl restart nginx
```
Nyt voidaan katsoa nettiselaimesta osoitetta http://OMAIPTÄHÄN/
API toimii eri rajapinnoissa.
## Linux Service
Linux servicet luodaan vakiona Debian pohjaisissa käyttöjärjestelmissä `/etc/systemd/system/`
esimerkiksi luodaan sotetie niminen palvelu
`sudo nano /etc/systemd/system/sotetie.service`
```
[Unit]
Description=uWSGI Service Flask APIlle
After=network.target

[Service]
User=aeon
Group=www-data
WorkingDirectory=/home/tommi/sotetie-hakutyokalu/api
Enviroment="PATH=/home/tommi/sotetie2021venv/bin"
ExecStart=/home/tommi/sotetie2021venv/bin/uwsgi --ini api.ini
```
Tämän jälkeen voidaan käyttää systemctl käynnistämään/sammuttamaan ja laittamaan, että käynnistyy kun palvelin käynnistyy.
## Cronjob
crontab -e
Käynnistyy sunnuntaina kello 0:00 ja päivittää kurssit tietokantaan. Voi säätää laittaa esimerkiksi tunnittain käynnistyvän päivityksen. Päivitys kestää n. 5 min.
```
0 0 * * 0 /home/tommi/sotetie2021venv/bin/python3 /home/tommi/sotetie-hakutyokalu/api/paivitys.py
```
