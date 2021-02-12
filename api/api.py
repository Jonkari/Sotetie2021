from tietokanta import Database
from flask import json, Flask, session, request, make_response
from flask_restful import Resource, Api
from flask_caching import Cache
from opintopolku import opintopolku

db = Database("localhost", "root", "", "wordpress")
def corsify(response):
    resp = make_response(json.jsonify(response))
    resp.headers.add('Access-Control-Allow-Origin', '*')
    return resp



app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={
    'CACHE_TYPE':'simple'
})

class Asiakaslahtoisyys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%asiakaslähtöisyys%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%asiakaslähtöi%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%osallisuus%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kohtaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelutar%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%asiakasprosessi%'"))
api.add_resource(Asiakaslahtoisyys, '/api/asiakaslahtoisyys', resource_class_kwargs={'db' : db})

class Neuvontaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%ohjaus- ja neuvontaosaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%ohjaus%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%neuvonta%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelujärjestelmä%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%vuorovaikutus%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kommunikaatio%'"))
api.add_resource(Neuvontaosaaminen, '/api/neuvontaosaaminen', resource_class_kwargs={'db' : db})

class Palvelujarjestelmat(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelujärjestelmät%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%palvelujärjestelmä%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%palveluohjaus%'"))
api.add_resource(Palvelujarjestelmat, '/api/palvelujarjestelmat', resource_class_kwargs={'db' : db})

class Etiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%etiikka%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%lainsäädäntö%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tietosuoja%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%vastuu%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%eettinen%'"))
api.add_resource(Etiikka, '/api/etiikka', resource_class_kwargs={'db' : db})

class Tutkimusosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%tutkimus- ja kehittämisosaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tutkimus%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%innovaatio%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kehittäminen%'"))
api.add_resource(Tutkimusosaaminen, '/api/tutkimusosaaminen', resource_class_kwargs={'db' : db})

class Robotiikka(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%robotiikka ja digitalisaatio%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%robotiikka%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%digi%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tekoäly%"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%sote-palvelut%"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tietoturva%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tietosuoja%'"))
api.add_resource(Robotiikka, '/api/robotiikka', resource_class_kwargs={'db' : db})

class Laatutietoisuus(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%vaikuttavuus- kustannus- ja laatutietoisuus%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%laatu%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%laadun%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%vaikuttavuu%"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%vaikutusten%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kustannukset%"))
api.add_resource(Laatutietoisuus, '/api/laatutietoisuus', resource_class_kwargs={'db' : db})

class KestavaKehitys(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%kestävä%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%ekolog%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kestävyys%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%kierrätys%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%ympäristö%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%energiankulutus%"))
api.add_resource(KestavaKehitys, '/api/kestavakehitys', resource_class_kwargs={'db' : db})

class Viestintaosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%viestintäosaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%viestintä%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%tunnetila%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%empatia%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%selkokieli%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%selko%'"))
api.add_resource(Viestintaosaaminen, '/api/viestintaosaaminen', resource_class_kwargs={'db' : db})

class Tyontekijyysosaaminen(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%työntekijyysosaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%osaamisen%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%johtaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%työhyvinvointi%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%muutososaaminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%muutosjoustavuus%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%urakehitys%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%verkostotyö%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%työyhteisö%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%moniammatillisuus%'"))
api.add_resource(Tyontekijyysosaaminen, '/api/tyontekijyysosaaminen', resource_class_kwargs={'db' : db})

class Yhteistoiminta(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData(
            "SELECT * FROM kurssit WHERE osaamiset LIKE '%monialainen yhteistoiminta%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%monialaisuu%'" 
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%moniammatillisuu%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%monitiet%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%yhteistyö%"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%verkostoituminen%'"
        or "SELECT * FROM kurssit WHERE osaamiset LIKE '%asiantuntijuus%'"))
api.add_resource(Yhteistoiminta, '/api/yhteistoiminta', resource_class_kwargs={'db' : db})

class Kaikki(Resource):
    def __init__(self, db):
        self.db = db
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self, id=None):
        if id:
            return corsify(self.db.getData("SELECT * FROM kurssit WHERE id={id}"))
        return corsify(self.db.getData("SELECT * FROM kurssit"))
api.add_resource(Kaikki, '/', '/api/', resource_class_kwargs={'db' : db})

if __name__ == '__main__':
    app.run(debug=True)