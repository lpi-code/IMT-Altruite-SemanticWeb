from rdflib import Graph
from src.config import ontology_file_path


class Ontology:
    def __init__(self):
        self.g = Graph()
        self.g.parse(ontology_file_path, format='xml')

    def execute_sparql_query(self, query_code):
        results = self.g.query(query_code)
        query_result = [str(row[0]).split('#')[1] for row in results]
        return query_result

    def get_all_habitats(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>
        
            SELECT ?x
            WHERE {{
                ?x rdfs:subClassOf URI:Habitat .
            }}
        """
        return self.g.query(query)

    def get_all_poissons(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Poisson .
            }}
        """
        return self.g.query(query)

    def get_all_appats(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Appat .
            }}
        """
        return self.g.query(query)

    def get_all_habitats_subclass_name(self):
        query_result = self.get_all_habitats()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_poissons_subclass_name(self):
        query_result = self.get_all_poissons()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_appats_subclass_name(self):
        query_result = self.get_all_appats()
        return [str(row[0]).split('#')[1] for row in query_result]
