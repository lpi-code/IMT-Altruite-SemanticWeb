import importlib
import subprocess
import textwrap

from flask import Flask, render_template, request, jsonify, send_from_directory
from models.ontology import *
from routes.api import api_bp


def create_app():
    required_modules = ['flask', 'rdflib']
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

    @app.route('/get_query', methods=['POST'])
    def get_query():
        data = request.get_json()
        selected_route = data.get('route')

        query_functions = {
            'habitats': get_all_habitats_query,
            'poissons': get_all_poissons_query,
            'appats': get_all_appats_query,
            'predateurs': get_all_predateurs_query,
            'reproductions': get_all_reproductions_query,
            'regimes': get_all_regimes_query,
            'elements_anatomiques': get_all_elements_anatomiques_query,
            'poissons_vivipares': get_poissons_vivipares_query,
            'poissons_ovipares': get_poissons_ovipares_query,
            'poissons_mer_ocean': get_poissons_mer_ocean_query,
            'poissons_taille_petite': get_poissons_taille_petite_query,
            'poissons_vie_longue': get_poissons_vie_longue_query,
            'poissons_branchies_2_8': get_poissons_branchies_2_8_query
        }

        query_function = query_functions.get(selected_route)
        query = query_function() if query_function else None

        query = textwrap.dedent(query).strip()

        return jsonify({'query': query})

    @app.route('/', methods=['POST'])
    def execute_query():
        query_code = request.form['sparqlQuery']

        try:
            query_result = ontology.execute_sparql_query(query_code)
            print(query_result)

            if len(query_result) == 0:
                return jsonify({'message': 'Aucun résultat trouvé 😢'})
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