from flask import Blueprint, jsonify, current_app as app

api_bp = Blueprint('api_bp', __name__)

# Liste des routes à créer
allRoutes = [
    '/habitats',
    '/appats',
    '/poissons'
]


# Créer les routes dynamiquement en fonction des routes définies dans la liste allRoutes
def create_routes():
    # Pour chaque route dans la liste allRoutes
    for route in allRoutes:
        # Enlever le slash au début et à la fin de la route
        route_name = route.strip('/')
        # Remplacer les potentiels slashs restant par des underscores
        route_function_name = route_name.replace('/', '_')

        # Créer la fonction qui sera appelée lorsqu'on fera une requête sur la route
        def get_route_function(route_name=route_function_name):
            # Récupérer la méthode de l'ontologie qui correspond à la route
            method_name = 'get_all_{}_subclass_name'.format(route_name)
            method = getattr(app.config['ONTOLOGY_INSTANCE'], method_name)
            return jsonify(method())

        # Ajouter la route à l'application
        api_bp.add_url_rule(route, endpoint=route_function_name, view_func=get_route_function)


create_routes()


@api_bp.route('/test')
def test():
    return jsonify(app.config['ONTOLOGY_INSTANCE'].get_subclasses_with_instances('Poisson'))