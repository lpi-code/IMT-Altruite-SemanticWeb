from rdflib import Graph

import sys

sys.path.insert(0, '../src')
from config import ontology_file_path


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
                ?x rdfs:subClassOf URI:Habitat
            }}
        """
        return self.g.query(query)

    def get_all_poissons(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Poisson
            }}
        """
        return self.g.query(query)

    def get_all_appats(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Appat
            }}
        """
        return self.g.query(query)

    def get_all_elements_anatomiques(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:ElementAnatomie
            }}
        """
        return self.g.query(query)

    def get_all_predateurs(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Predateur
            }}
        """
        return self.g.query(query)

    def get_all_reproductions(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Reproduction
            }}
        """
        return self.g.query(query)

    def get_all_regimes(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:RegimeAlimentaire
            }}
        """
        return self.g.query(query)

    def get_poissons_vivipares(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Poisson ;
                URI:reproduction URI:Vivipare .
            }}
        """
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_poissons_ovipares(self):
        query = f"""
            PREFIX URI: <{ontology_file_path}#>

            SELECT ?x
            WHERE {{
                ?x a URI:Poisson ;
                URI:reproduction URI:Ovipare .
            }}
        """
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_poissons_mer_ocean(self):
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
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

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

    def get_poissons_taille_petite(self):
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
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_poissons_vie_longue(self):
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
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_poissons_branchies_2_8(self):
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
        query_result = self.g.query(query)
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_habitats_subclass_name(self):
        query_result = self.get_all_habitats()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_poissons_subclass_name(self):
        query_result = self.get_all_poissons()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_appats_subclass_name(self):
        query_result = self.get_all_appats()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_elements_anatomiques_subclass_name(self):
        query_result = self.get_all_elements_anatomiques()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_predateurs_subclass_name(self):
        query_result = self.get_all_predateurs()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_reproductions_subclass_name(self):
        query_result = self.get_all_reproductions()
        return [str(row[0]).split('#')[1] for row in query_result]

    def get_all_regimes_subclass_name(self):
        query_result = self.get_all_regimes()
        return [str(row[0]).split('#')[1] for row in query_result]