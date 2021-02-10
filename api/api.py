from tietokanta import Database
from flask import json
from flask import Flask
from flask import Flask
from flask_restful import Resource, Api
from flask_caching import Cache
from opintopolku import opintopolku

db = Database("localhost", "root", "", "wordpress")



app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={
    'CACHE_TYPE':'simple'
})
class News(Resource):
    def __init__(self, db):
        super().__init__()
    @cache.cached(timeout=3600)
    def get(self,):
        return json.jsonify(db.getData("SELECT * FROM kurssit"))
api.add_resource(News, '/', '/api', '/api/etiikka', resource_class_kwargs={'db' : db})
if __name__ == '__main__':
    app.run(debug=True)