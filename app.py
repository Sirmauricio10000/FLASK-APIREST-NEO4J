from aifc import Error
from flask import Flask, redirect, url_for
from flask_restx import Api, Namespace, Resource
from connection import (
    get_all_nodes,
    get_ruta_mas_corta,
    get_rutas_de_un_nodo,
    get_route,
    get_coords,
    get_list_of_coords,
)
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

api = Api(
    app,
    doc="/",
    version="0.1",
    title="TU RUTA VALLEDUPAR, API",
    description="""
  <pre>
    An application designed for managing integrated transportation routes in the city of Valledupar.
    It provides an open interface to access data related to nodes, routes, and geographical coordinates,
    allowing users to explore and obtain valuable information about the city's transportation system.
  </pre>

  <pre>
    This API provides a valuable tool for those interested in the city's transportation system.
    Developers can use this API to create applications, services, or tools that leverage the available data and provide innovative solutions
    for route planning and optimization in Valledupar's transportation network.
  </pre>
""",
)

namespace_nodes = Namespace("Nodes")
namespace_routes = Namespace("Routes")


api.add_namespace(namespace_nodes)
api.add_namespace(namespace_routes)


@namespace_nodes.route("/api/swagger", doc=False)
class Swagger(Resource):
    def get(self):
        swagger_url = url_for("api.swagger_json")
        return redirect(swagger_url)


@namespace_nodes.route("/nodes")
class AllNodes(Resource):
    def get(self):
        try:
            response, status_code = get_all_nodes()
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500
        
@namespace_nodes.route("/nodes/get_coordenadas/<string:nodo>")
class Cords(Resource):
    def get(self, nodo):
        try:
            response, status_code = get_coords(nodo)
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500


@namespace_nodes.route("/nodes/get_lista_coordenadas/<string:nodos>")
class ListOfCords(Resource):
    def get(self, nodos):
        try:
            lista_nodos = nodos.split(",")
            response, status_code = get_list_of_coords(lista_nodos)
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500


@namespace_routes.route("/rutas/ruta_mas_corta/<string:origen>/<string:destino>")
class RutaMasCorta(Resource):
    def get(self, origen, destino):
        try:
            response, status_code = get_ruta_mas_corta(origen, destino)
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500

@namespace_routes.route("/rutas/rutas_de_un_nodo/<string:nodo>")
class AllRoutes(Resource):
    def get(self, nodo):
        try:
            response, status_code = get_rutas_de_un_nodo(nodo)
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500

@namespace_routes.route("/rutas/ruta_individual/<string:ruta>")
class RutaIndividual(Resource):
    def get(self, ruta):
        try:
            response, status_code = get_route(ruta)
            return response, status_code
        except Exception as e:
            return {'error': "Ocurrió un error, " + str(e)}, 500




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

