from rdflib import Graph

import sys

sys.path.insert(0, '../src')
from config import ontology_file_path


def get_all_habitats_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x rdfs:subClassOf URI:Habitat
        }}
    """
    return query


def get_all_poissons_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Poisson
        }}
    """
    return query


def get_all_appats_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Appat
        }}
    """
    return query


def get_all_elements_anatomiques_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x rdfs:subClassOf URI:ElementAnatomie
        }}
    """
    return query


def get_all_predateurs_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Predateur
        }}
    """
    return query


def get_all_reproductions_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Reproduction
        }}
    """
    return query


def get_all_regimes_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:RegimeAlimentaire
        }}
    """
    return query


def get_poissons_vivipares_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Poisson ;
               URI:reproduction URI:Vivipare .
        }}
    """
    return query


def get_poissons_ovipares_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>

        SELECT ?x
        WHERE {{
            ?x a URI:Poisson ;
               URI:reproduction URI:Ovipare .
        }}
    """
    return query


def get_poissons_mer_ocean_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT DISTINCT ?x
        WHERE {{
            {{
                ?x rdf:type URI:Poisson ;
                   URI:habite ?habitat .
                ?habitat rdf:type URI:Mer .
            }}
            UNION
            {{
                ?x rdf:type URI:Poisson ;
                   URI:habite ?habitat .
                ?habitat rdf:type URI:Ocean .
            }}
        }}
    """
    return query


def get_poissons_taille_petite_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?x
        WHERE {{
            ?x rdf:type URI:Poisson ;
                URI:taille ?taille .
            FILTER (xsd:decimal(?taille) < 20)
        }}
    """
    return query

def get_poissons_vie_longue_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?x
        WHERE {{
            ?x rdf:type URI:Poisson ;
                URI:esperance ?esperance .
            FILTER (xsd:decimal(?esperance) > 10)
        }}
    """
    return query

def get_poissons_branchies_2_8_query():
    query = f"""
        PREFIX URI: <{ontology_file_path}#>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>

        SELECT ?x
        WHERE {{
            ?x rdf:type URI:Poisson ;
                URI:branchies ?branchies .
            FILTER (xsd:integer(?branchies) >= 2 && xsd:integer(?branchies) <= 8)
        }}
    """
    return query


class Ontology:
    def __init__(self):
        self.g = Graph()
        self.g.parse(ontology_file_path, format='xml')

    def execute_sparql_query(self, query_code):
        results = self.g.query(query_code)
        query_result = [str(row[0]).split('#')[1] for row in results]
        return query_result

    def get_subclasses_with_instances(self, classe):
        classe = classe.strip("'")
        query = f"""
            PREFIX URI: <{ontology_file_path}#>
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

            SELECT ?subclass ?instance
            WHERE {{
                ?subclass rdfs:subClassOf URI:{classe} .
                ?instance a ?subclass .
            }}
        """
        print(query)
        results = self.g.query(query)

        whole_dict = {}
        for row in results:
            subclass = row['subclass'].split('#')[-1]
            instance = row['instance'].split('#')[-1]

            if subclass in whole_dict:
                whole_dict[subclass].append(instance)
            else:
                whole_dict[subclass] = [instance]

        return whole_dict

    def get_all_habitats_subclass_name(self):
        return self.execute_sparql_query(get_all_habitats_query())

    def get_all_poissons_subclass_name(self):
        return self.execute_sparql_query(get_all_poissons_query())

    def get_all_appats_subclass_name(self):
        return self.execute_sparql_query(get_all_appats_query())

    def get_all_elements_anatomiques_subclass_name(self):
        return self.execute_sparql_query(get_all_elements_anatomiques_query())

    def get_all_predateurs_subclass_name(self):
        return self.execute_sparql_query(get_all_predateurs_query())

    def get_all_reproductions_subclass_name(self):
        return self.execute_sparql_query(get_all_reproductions_query())

    def get_all_regimes_subclass_name(self):
        return self.execute_sparql_query(get_all_regimes_query())

    def get_poissons_taille_petite(self):
        return self.execute_sparql_query(get_poissons_taille_petite_query())

    def get_poissons_vivipares(self):
        return self.execute_sparql_query(get_poissons_vivipares_query())

    def get_poissons_ovipares(self):
        return self.execute_sparql_query(get_poissons_ovipares_query())

    def get_poissons_mer_ocean(self):
        return self.execute_sparql_query(get_poissons_mer_ocean_query())

    def get_poissons_vie_longue(self):
        return self.execute_sparql_query(get_poissons_vie_longue_query())

    def get_poissons_branchies_2_8(self):
        return self.execute_sparql_query(get_poissons_branchies_2_8_query())
