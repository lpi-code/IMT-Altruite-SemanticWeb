from flask import Blueprint, jsonify, current_app as app

api_bp = Blueprint('api_bp', __name__)


# /habitats json
@api_bp.route('/habitats')
def get_habitats():
    return jsonify(app.config['ONTOLOGY_INSTANCE'].get_all_habitats_subclass_name())

# /poisson json
@api_bp.route('/poisson')
def get_poisson():
    return jsonify(app.config['ONTOLOGY_INSTANCE'].get_all_poisson_subclass_name())