from flask import Flask
import os

from internal.blueprint import blueprint as InternalBlueprint
from faiss_index.blueprint import blueprint as FaissIndexBlueprint

app = Flask(__name__)

seedPath = '../resources/seedPins.json'
script_dir = os.path.dirname(__file__)
abs_file_path = os.path.join(script_dir, seedPath)
app.config['PINS_JSON_PATH'] = abs_file_path # '../../chronopin/scripts/backup/seedPins.json'

app.register_blueprint(InternalBlueprint)
app.register_blueprint(FaissIndexBlueprint)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
