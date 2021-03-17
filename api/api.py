from tietokanta import Database
from flask import json, Flask, make_response
from flask_restful import Resource, Api
from flask_caching import Cache
from opintopolku import opintopolku
import asetukset

db = Database(asetukset.palvelin, asetukset.kayttaja, asetukset.salasana, asetukset.tietokanta)
def corsify(response):
    resp = make_response(json.jsonify(response))
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp

app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={
    'CACHE_TYPE':'simple'
})

rajapinnat = {
    "Asiakaslähtöisyys" : "/api/asiakaslahtoisyys",
    "Neuvontaosaaminen" : "/api/neuvontaosaaminen",
    "Palvelujärjestelmät" : "/api/palvelujarjestelmat",
    "Lainsäädäntö ja etiikka" : "/api/etiikka",
    "Tutkimus- ja kehittämisosaaminen" : "/api/tutkimusosaaminen",
    "Robotiikka ja digitalisaatio" : "/api/robotiikka",
    "Vaikuttavuus- kustannus- ja laatutietoisuus" : "/api/laatutietoisuus",
    "Kestävän kehityksen osaaminen" : "/api/kestavakehitys",
    "Viestintäosaaminen" : "/api/viestintaosaaminen",
    "Työntekijyysosaaminen" : "/api/tyontekijyysosaaminen",
    "Monialainen yhteistoiminta" : "/api/yhteistoiminta"
}

class Koulut(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        return corsify(self.db.getData("SELECT distinct koulu FROM kurssit ORDER BY koulu ASC"))
api.add_resource(Koulut, "/api/koulut", resource_class_kwargs={'db' : db})

class Kielet(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        return corsify(self.db.getData("SELECT distinct kieli FROM kurssit ORDER BY kieli ASC"))
api.add_resource(Kielet, "/api/kielet", resource_class_kwargs={'db' : db})

class Rajapinnat(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        return corsify(rajapinnat)
api.add_resource(Rajapinnat, "/api/rajapinnat", resource_class_kwargs={'db' : db})

class Asiakaslahtoisyys(Resource):
    def __init__(self, db):
        self.db = db
        self.data = None
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        """Hakee kurssit taulusta kaikki asiakaslahtoisyyteen liittyvät kurssit

        Sisältää Fail-Safe järjestelmän, joka palauttaa edellisen tuloksen 
        JOS ei palauttanut mitään nykyisellä haulla JA tietokanta on päivittymässä.

        Returns:
            (Response or None) : Palauttaa Flask Responsen tai Nonen virhetilanteissa.
        """
        tmp = self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%asiakaslähtöisyys%'") # Hakee kurssit
        if tmp: # Onko kursseja haussa
            self.data = tmp
            return corsify(self.data)
        else: #muussa tapauksessa
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivittymassa'") # tarkistetaan paivittymassa kenttä
            if paivittymassa: # onko tullut dataa haulla
                paivittymassa = paivittymassa[0] # otetaan ensimmäinen (ja ainoa) rivi
                if paivittymassa["data"] == 0: # Jos ei ole päivittymässä palautetaan tyhjä dictionary
                    self.data = tmp # Laitetaan muistiin viime haku
                    return corsify(tmp)
                else:
                    return corsify(self.data) # Jos tietokanta on päivittymässä ja on tyhjä tietokanta niin, sitten palautetaan edellinen tulos
            return None
api.add_resource(Asiakaslahtoisyys, '/api/asiakaslahtoisyys', resource_class_kwargs={'db' : db})

class Neuvontaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%ohjaus- ja neuvontaosaaminen%'"))
api.add_resource(Neuvontaosaaminen, '/api/neuvontaosaaminen', resource_class_kwargs={'db' : db})

class Palvelujarjestelmat(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelujärjestelmät%'"))
api.add_resource(Palvelujarjestelmat, '/api/palvelujarjestelmat', resource_class_kwargs={'db' : db})

class Etiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%lainsäädäntö ja etiikka%'"))
api.add_resource(Etiikka, '/api/etiikka', resource_class_kwargs={'db' : db})

class Tutkimusosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%tutkimus- ja kehittämisosaaminen%'"))
api.add_resource(Tutkimusosaaminen, '/api/tutkimusosaaminen', resource_class_kwargs={'db' : db})

class Robotiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%robotiikka ja digitalisaatio%'"))
api.add_resource(Robotiikka, '/api/robotiikka', resource_class_kwargs={'db' : db})

class Laatutietoisuus(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%vaikuttavuus- kustannus- ja laatutietoisuus%'"))
api.add_resource(Laatutietoisuus, '/api/laatutietoisuus', resource_class_kwargs={'db' : db})

class KestavaKehitys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%kestävän kehityksen osaaminen%'"))
api.add_resource(KestavaKehitys, '/api/kestavakehitys', resource_class_kwargs={'db' : db})

class Viestintaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%viestintäosaaminen%'"))
api.add_resource(Viestintaosaaminen, '/api/viestintaosaaminen', resource_class_kwargs={'db' : db})

class Tyontekijyysosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%työntekijyysosaaminen%'"))
api.add_resource(Tyontekijyysosaaminen, '/api/tyontekijyysosaaminen', resource_class_kwargs={'db' : db})

class Yhteistoiminta(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%monialainen yhteistoiminta%'"))
api.add_resource(Yhteistoiminta, '/api/yhteistoiminta', resource_class_kwargs={'db' : db})

class Kaikki(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self):
        return corsify(self.db.getData("SELECT * FROM kurssit"))
api.add_resource(Kaikki, '/', '/api/', resource_class_kwargs={'db' : db})

class Paivitys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
        @cache.cached(timeout=3600)
        def get(self):
            return corsify(self.db.getData("SELECT TOP 1 modify_date FROM sys.objects ORDER BY modify_date DESC")) #MSSQL, ei toimi vielä
api.add_resource(Paivitys, '/api/paivitys', resource_class_kwargs={'db' : db})

if __name__ == '__main__':
    app.run(debug=True)