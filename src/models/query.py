from rdflib import Graph

# Chemin vers votre fichier RDF/OWL
ontology_file_path = 'chemin/vers/votre/fichier.owl'


def execute_sparql_query(query_code):
    # Charger l'ontologie RDF/OWL dans un graphe RDF
    g = Graph()
    g.parse(ontology_file_path, format='xml')

    # Exécuter la requête SPARQL sur le graphe RDF
    results = g.query(query_code)

    # Traiter les résultats et les renvoyer
    # ...

    return results
