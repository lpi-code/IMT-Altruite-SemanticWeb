import rdflib
from rdflib import Graph, Namespace, URIRef, Literal


class Ontology:
    def __init__(self, ontology_file_path):
        self.g = Graph()
        self.g.parse(ontology_file_path, format='xml')

    def execute_sparql_query(self, query_code):
        results = self.g.query(query_code)
        query_result = [str(row[0]).split('#')[1] for row in results]
        return query_result

    def get_all_habitats(self):
        return self.g.query("""
            PREFIX URI: <https://mtx.dev/ontology/fishes#>
            SELECT ?s
            WHERE {
                ?s rdfs:subClassOf <https://mtx.dev/ontology/fishes#Habitat> .
            }
        """)

    def get_all_poissons(self):
        return self.g.query("""
            PREFIX URI: <https://mtx.dev/ontology/fishes#>
            
            SELECT ?x
            WHERE {
                ?x a URI:Poisson .
            }
        """)

    def get_all_appats(self):
        return self.g.query("""
            PREFIX URI: <https://mtx.dev/ontology/fishes#>

            SELECT ?x
            WHERE {
                ?x a URI:Appat .
            }
        """)

    def get_all_habitats_subclass_name(self):
        query_result = self.get_all_habitats()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_poissons_subclass_name(self):
        query_result = self.get_all_poissons()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_appats_subclass_name(self):
        query_result = self.get_all_appats()
        return [str(row[0]).split('#')[1] for row in query_result]