from flask import Flask

from internal.blueprint import blueprint as InternalBlueprint
from faiss_index.blueprint import blueprint as FaissIndexBlueprint

app = Flask(__name__)
# app.config['INDEX_PATH'] = '/opt/faiss-web-service/resources/index'
# app.config['IDS_VECTORS_PATH'] = '/opt/faiss-web-service/resources/ids_vectors.p'
app.config['PINS_JSON_PATH'] = '../scripts/seedPins.json' # '../../chronopin/scripts/backup/seedPins.json'

app.register_blueprint(InternalBlueprint)
app.register_blueprint(FaissIndexBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
