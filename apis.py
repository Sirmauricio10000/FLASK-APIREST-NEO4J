from flask import jsonify
from flask_restx import Namespace, Resource, Api
from validation import *

api = Api()

# Crea un Namespace para tus APIs
namespace = Namespace('api', description='API endpoints')
api.add_namespace(namespace)


@namespace.route('/nodes')
class NodesResource(Resource):
    @api.doc(description='Obtiene todas las Paradas')
    def get(self):
        response = get_all_nodes()
        return response

@namespace.route('/rutas/ruta_mas_corta/<string:origen>/<string:destino>')
class RutaResources(Resource):
    @api.doc(description='Obtiene los caminos directos más cortos de una ruta en base a un origen y destino')
    def get(self, origen, destino):
       response = get_ruta_mas_corta(origen, destino)
       return jsonify(response)

@namespace.route('/rutas/rutas_de_un_nodo/<string:nodo>')
class RutaResources(Resource):
    @api.doc(description='Obtiene todas las rutas de un nodo')
    def get(self, nodo):
       response = get_rutas_de_un_nodo(nodo)
       return jsonify(response)

@namespace.route('/rutas/ruta_individual/<string:ruta>')
class RutaResource(Resource):
    @api.doc(description='Obtiene información de una ruta individual')
    def get(self, ruta):     
        response = get_route(ruta)
        return jsonify(response)


