from datetime import datetime
from tietokanta import Database
import json
import flask
from flask import Flask, make_response, g
from flask_restful import Resource, Api
from flask_caching import Cache
from opintopolku import opintopolku
import asetukset

db = Database(asetukset.palvelin, asetukset.kayttaja, asetukset.salasana, asetukset.tietokanta, asetukset.portti)
def corsify(response):
    resp = make_response(flask.json.jsonify(response))
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
cache_query_ins = "INSERT INTO cache (`key`, `value`) VALUES('{key}', '{value}') ON DUPLICATE KEY UPDATE `value`='{value}'"
cache_query_sel = "SELECT value FROM cache WHERE `key`='{}'"

class Koulut(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        tmp = self.db.getData("SELECT kurssit.koulu AS koulu, maakunnat.maakunta AS maakunta FROM kurssit JOIN postinumerot ON postinumerot.postinumero=kurssit.postinumero JOIN maakunnat ON postinumerot.postitoimipaikka=maakunnat.kunta GROUP BY kurssit.koulu ORDER BY maakunnat.maakunta;")
        if tmp:
            self.db.query(cache_query_ins.format(key="koulut", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="koulut", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("koulut",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Koulut, "/api/koulut", resource_class_kwargs={'db' : db})

class Kielet(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        tmp = self.db.getData("SELECT distinct kieli FROM kurssit ORDER BY kieli ASC")
        if tmp:
            self.db.query(cache_query_ins.format(key="kielet", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="kielet", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("kielet",))
                    return corsify(json.loads(data[0]["value"]))
            return None        
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
        super().__init__()
    
    def get(self):
        """Hakee kurssit taulusta kaikki asiakaslahtoisyyteen liittyvät kurssit

        Sisältää Fail-Safe järjestelmän, joka palauttaa edellisen tuloksen 
        JOS ei palauttanut mitään nykyisellä haulla JA tietokanta on päivittymässä.

        Returns:
            (Response or None) : Palauttaa Flask Responsen tai Nonen virhetilanteissa.
        """
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%asiakaslähtöisyys%' ORDER BY nimi") # Hakee kurssit
        if tmp: # Onko kursseja haussa
            self.db.query(cache_query_ins.format(key="asiakaslähtöisyys", value=json.dumps(tmp)))
            return corsify(tmp)
        else: #muussa tapauksessa
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'") # tarkistetaan paivittymassa kenttä
            if paivittymassa: # onko tullut dataa haulla
                paivittymassa = paivittymassa[0] # otetaan ensimmäinen (ja ainoa) rivi
                if paivittymassa["data"] == 0: # Jos ei ole päivittymässä palautetaan tyhjä dictionary
                    self.db.query(cache_query_ins.format(key="asiakaslähtöisyys", value=json.dumps(tmp)))# Laitetaan muistiin viime haku
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("asiakaslähtöisyys",))
                    return corsify(json.loads(data[0]["value"])) # Jos tietokanta on päivittymässä ja on tyhjä tietokanta niin, sitten palautetaan edellinen tulos
            return None
api.add_resource(Asiakaslahtoisyys, '/api/asiakaslahtoisyys', resource_class_kwargs={'db' : db})

class Neuvontaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%ohjaus- ja neuvontaosaaminen%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="neuvontaosaaminen", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="neuvontaosaaminen", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("neuvontaosaaminen",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Neuvontaosaaminen, '/api/neuvontaosaaminen', resource_class_kwargs={'db' : db})

class Palvelujarjestelmat(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelujärjestelmät%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="palvelujarjestelmat", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="palvelujarjestelmat", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("palvelujarjestelmat",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Palvelujarjestelmat, '/api/palvelujarjestelmat', resource_class_kwargs={'db' : db})

class Etiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%lainsäädäntö ja etiikka%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="etiikka", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="etiikka", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("etiikka",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Etiikka, '/api/etiikka', resource_class_kwargs={'db' : db})

class Tutkimusosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%tutkimus- ja kehittämisosaaminen%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="tutkimusosaaminen", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="tutkimusosaaminen", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("tutkimusosaaminen",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Tutkimusosaaminen, '/api/tutkimusosaaminen', resource_class_kwargs={'db' : db})

class Robotiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%robotiikka ja digitalisaatio%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="robotiikka", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="robotiikka", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("robotiikka",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Robotiikka, '/api/robotiikka', resource_class_kwargs={'db' : db})

class Laatutietoisuus(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%vaikuttavuus- kustannus ja laatutietoisuus%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="laatutietoisuus", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="laatutietoisuus", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("laatutietoisuus",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Laatutietoisuus, '/api/laatutietoisuus', resource_class_kwargs={'db' : db})

class KestavaKehitys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%kestävän kehityksen osaaminen%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="kestavakehitys", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="kestavakehitys", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("kestavakehitys",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(KestavaKehitys, '/api/kestavakehitys', resource_class_kwargs={'db' : db})

class Viestintaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%viestintäosaaminen%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="viestintäosaaminen", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="viestintäosaaminen", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("viestintaosaaminen",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Viestintaosaaminen, '/api/viestintaosaaminen', resource_class_kwargs={'db' : db})

class Tyontekijyysosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%työntekijyysosaaminen%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="tyontekijyysosaaminen", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="tyontekijyysosaaminen", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("tyontekijyysosaaminen",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Tyontekijyysosaaminen, '/api/tyontekijyysosaaminen', resource_class_kwargs={'db' : db})

class Yhteistoiminta(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit WHERE osaamiset LIKE '%monialainen yhteistoiminta%' ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="yhteistoiminta", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="yhteistoiminta", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("yhteistoiminta",))
                    return corsify(json.loads(data[0]["value"]))
            return None
api.add_resource(Yhteistoiminta, '/api/yhteistoiminta', resource_class_kwargs={'db' : db})

class Kaikki(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    
    def get(self):
        tmp = self.db.getData("SELECT * FROM kurssit ORDER BY nimi")
        if tmp:
            self.db.query(cache_query_ins.format(key="kaikki", value=json.dumps(tmp)))
            return corsify(tmp)
        else:
            paivittymassa = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.kaynnissa'")
            if paivittymassa:
                paivittymassa = paivittymassa[0]
                if paivittymassa["data"] == 0:
                    self.db.query(cache_query_ins.format(key="kaikki", value=json.dumps(tmp)))
                    return corsify(tmp)
                else:
                    data = self.db.getData(cache_query_sel.format("kaikki",))
                    return corsify(json.loads(data[0]["value"]))
            return {}
        return corsify(self.db.getData("SELECT * FROM kurssit"))
api.add_resource(Kaikki, '/', '/api/', resource_class_kwargs={'db' : db})

class Paivitys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    def get(self):
        tmp = self.db.getData("SELECT * FROM asetukset WHERE tyyppi='paivitetty.timestamp' OR tyyppi='paivitetty.kaynnissa'")
        return corsify(tmp)
api.add_resource(Paivitys, '/api/paivitys', resource_class_kwargs={'db' : db})

if __name__ == '__main__':
    app.run(debug=True)