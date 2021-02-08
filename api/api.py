import json
import time
import pymysql.cursors
from tietokanta import Database
from flask import json
from flask import Flask
from flask_restful import Resource, Api
from flask_caching import Cache

app = Flask(__name__)
api = Api(app)
cache = Cache(app, config={
    'CACHE_TYPE':'simple'
})

db = Database("localhost", "root", "", "wordpress")

class News(Resource):
    def __init__(self,):
        super().__init__()
    @cache.cached(timeout=60)
    def get(self,):
        return json.jsonify(db.getData("SELECT * FROM news ORDER BY timestamp DESC"))
api.add_resource(News, '/api', '/api/etiikka')
if __name__ =='__main__':
    app.run(host="0.0.0.0", debug=True)