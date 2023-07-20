from flask import Flask, redirect, url_for
from flask_restx import Api, Resource
from connection import get_all_nodes, get_ruta_mas_corta, get_rutas_de_un_nodo, get_route, get_coords, get_list_of_coords
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
api = Api(app)

@api.route('/api/swagger', doc=False)
class Swagger(Resource):
    def get(self):
        swagger_url = url_for('api.swagger_json')
        return redirect(swagger_url)

@api.route('/nodes')
class AllNodes(Resource):
    def get(self):
        response, status_code = get_all_nodes()
        return response, status_code
    
@api.route('/nodes/get_coordenadas/<string:nodo>')
class RutaIndividual(Resource):
    def get(self, nodo):
        response, status_code = get_coords(nodo)
        return response, status_code
    
@api.route('/nodes/get_lista_coordenadas/<string:nodos>')
class RutaIndividual(Resource):
    def get(self, nodos):
        lista_nodos = nodos.split(',')
        response, status_code = get_list_of_coords(lista_nodos)
        return response, status_code


@api.route('/rutas/ruta_mas_corta/<string:origen>/<string:destino>')
class RutaMasCorta(Resource):
    def get(self, origen, destino):
        response, status_code = get_ruta_mas_corta(origen, destino)
        return response, status_code

@api.route('/rutas/rutas_de_un_nodo/<string:nodo>')
class AllRoutes(Resource):
    def get(self, nodo):
        response, status_code = get_rutas_de_un_nodo(nodo)
        return response, status_code

@api.route('/rutas/ruta_individual/<string:ruta>')
class RutaIndividual(Resource):
    def get(self, ruta):
        response, status_code = get_route(ruta)
        return response, status_code

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)