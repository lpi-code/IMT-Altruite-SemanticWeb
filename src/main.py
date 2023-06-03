import importlib
import subprocess
from flask import Flask, render_template, request, jsonify, send_from_directory
from models.ontology import Ontology
from routes.api import api_bp


def create_app():
    required_modules = ['flask', 'rdflib', 'os', 'gunicorn']
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"{module} est installé.")
        except ImportError:
            print(f"{module} n'est pas installé. Installation en cours...")
            subprocess.check_call(['pip', 'install', module])
            print(f"{module} a été installé avec succès.")

    ontology = Ontology()

    app = Flask(__name__)
    app.config['ONTOLOGY_INSTANCE'] = ontology
    app.config.from_object('config')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/', methods=['POST'])
    def execute_query():
        query_code = request.form['sparqlQuery']

        try:
            query_result = ontology.execute_sparql_query(query_code)
            print(query_result)

            if len(query_result) == 0:
                return jsonify({'message': 'Aucun résultat trouvé.'})
            else:
                return jsonify({'result': query_result})

        except Exception as e:
            error_message = str(e)
            return jsonify({'error': error_message})

    @app.route('/css/<path:path>')
    def send_css(path):
        return send_from_directory('css', path)

    @app.route('/img/<path:path>')
    def send_logo(path):
        return send_from_directory('img', path)

    @app.route('/')
    def index():
        all_routes = [str(rule) for rule in app.url_map.iter_rules() if str(rule).startswith('/api/')]
        all_routes = [route[5:] for route in all_routes]
        return render_template('index.html.j2', routes=all_routes)

    return app


if __name__ == '__main__':
    app = create_app()
    app.debug = True
    app.run('0.0.0.0', 30029)