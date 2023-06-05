from flask import Blueprint, jsonify, current_app as app

api_bp = Blueprint('api_bp', __name__)

# Liste des routes à créer
allRoutes = {
    '/habitats': "get_subclasses_with_instances('Habitat')",
    '/appats': 'get_all_appats_subclass_name',
    '/poissons': 'get_all_poissons_subclass_name',
    '/predateurs': 'get_all_predateurs_subclass_name',
    '/reproductions': 'get_all_reproductions_subclass_name',
    '/regimes': 'get_all_regimes_subclass_name',
    '/elements_anatomiques': 'get_all_elements_anatomiques_subclass_name',
    '/poissons_vivipares': 'get_poissons_vivipares',
    '/poissons_ovipares': 'get_poissons_ovipares',
    '/poissons_mer_ocean': 'get_poissons_mer_ocean',
    '/poissons_taille_petite': 'get_poissons_taille_petite',
    '/poissons_vie_longue': 'get_poissons_vie_longue',
    '/poissons_branchies_2_8': 'get_poissons_branchies_2_8',
}


# Créer les routes dynamiquement en fonction des routes définies dans la liste allRoutes
def create_routes():
    # Pour chaque route dans la liste allRoutes
    for route, method_name in allRoutes.items():
        # Enlever le slash au début et à la fin de la route
        route_name = route.strip('/')
        # Remplacer les potentiels slashs restant par des underscores
        route_function_name = route_name.replace('/', '_')

        # Créer la fonction qui sera appelée lorsqu'on fera une requête sur la route
        def get_route_function(method_name=method_name):
            # Vérifier si la méthode est "get_subclasses_with_instances"
            if method_name.startswith("get_subclasses_with_instances(") and method_name.endswith(")"):
                # Extraire le nom de classe entre les parenthèses
                class_name = method_name.split("(", 1)[1].split(")", 1)[0]
                # Appeler la méthode avec le nom de classe
                method = getattr(app.config['ONTOLOGY_INSTANCE'], 'get_subclasses_with_instances')(class_name)
                return jsonify(method)
            else:
                # Récupérer la méthode de l'ontologie qui correspond à la route
                method = getattr(app.config['ONTOLOGY_INSTANCE'], method_name)
                return jsonify(method())

        # Ajouter la route à l'application
        api_bp.add_url_rule(route, endpoint=route_function_name, view_func=get_route_function)


create_routes()
