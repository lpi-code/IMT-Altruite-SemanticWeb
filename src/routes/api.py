from flask import Blueprint, jsonify, current_app as app

api_bp = Blueprint('api_bp', __name__)

allRoutes = [
    '/habitats',
    '/appats',
    '/poissons'
]


def create_routes():
    for route in allRoutes:
        route_name = route.strip('/')
        route_function_name = route_name.replace('/', '_')

        def get_route_function(route_name=route_function_name):
            method_name = 'get_all_{}_subclass_name'.format(route_name)
            method = getattr(app.config['ONTOLOGY_INSTANCE'], method_name)
            return jsonify(method())

        api_bp.add_url_rule(route, endpoint=route_function_name, view_func=get_route_function)


create_routes()
