import os

SECRET_KEY = os.urandom(32)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

# ontology_file_path = "basedir/../FishOntologyMtx.rdf"
ontology_file_path = "https://mtx.dev/ontology/fishes"
