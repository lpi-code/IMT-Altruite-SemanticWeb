import rdflib
from rdflib import Graph, Namespace, URIRef, Literal


class Ontology:
    def __init__(self, ontology_file_path):
        self.g = Graph()
        self.g.parse(ontology_file_path, format='xml')

    def get_all_habitats(self):
        return self.g.query("""
            PREFIX URI: <https://mtx.dev/ontology/fishes#>
            SELECT ?s
            WHERE {
                ?s rdfs:subClassOf <https://mtx.dev/ontology/fishes#Habitat> .
            }
        """)

    def get_all_habitats_subclass_name(self):
        query_result = self.get_all_habitats()
        return [str(row[0]).split('#')[1] for row in query_result]
