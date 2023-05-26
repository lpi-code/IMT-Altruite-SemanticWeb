from flask import Flask, render_template
from routes.api import api_bp
from config import ontology_file_path
from models.ontology import Ontology

print("Initializing Ontology")
ontology = Ontology(ontology_file_path)
print("Ontology Initialized")

print("Initializing Flask")
app = Flask(__name__)
app.config['ONTOLOGY_INSTANCE'] = ontology
app.config.from_object('config')
app.register_blueprint(api_bp, url_prefix='/api')
print("Flask Initialized")


@app.route('/')
def index():
    return render_template('index.html.j2')


if __name__ == '__main__':
    app.debug = True
    app.run()
