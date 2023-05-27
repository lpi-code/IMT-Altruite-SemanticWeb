from flask import Flask, render_template, request, jsonify

from config import ontology_file_path
from models.ontology import Ontology
from routes.api import api_bp

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


@app.route('/')
def index():
    all_routes = [str(rule) for rule in app.url_map.iter_rules() if str(rule).startswith('/api/')]
    all_routes = [route[5:] for route in all_routes]
    return render_template('index.html.j2', routes=all_routes)


if __name__ == '__main__':
    app.debug = True
    app.run()
