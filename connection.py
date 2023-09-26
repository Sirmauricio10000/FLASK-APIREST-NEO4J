from flask_restx import Api
from py2neo import Graph
from neo4j.exceptions import Neo4jError


graph = Graph("neo4j+ssc://45486069.databases.neo4j.io", auth=("neo4j", "12345678"))
api = Api()


def get_all_nodes():
    try:
        response = graph.run("""MATCH (n)
            RETURN collect(n.nombre) AS nodos""").data()
        return response, 200
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500

def get_route(ruta):
    try:
        query = """MATCH (n:Parada)-[r:""" + ruta + """]->(m:Parada)
            WITH COLLECT(n) + COLLECT(m) AS nodos, r
            UNWIND nodos AS nodo
            WITH collect(DISTINCT CASE WHEN r.tipo = "ida" THEN nodo.nombre ELSE null END) AS ida, collect(DISTINCT CASE WHEN r.tipo = "vuelta" THEN nodo.nombre ELSE null END) AS vuelta
            RETURN { ida: ida, vuelta: vuelta } AS camino"""
        response = graph.run(query).data()

        if not response or not response[0]['camino']['ida']:
            error_message = "La ruta no existe"
            return {'error': error_message}, 404

        return response, 200
    
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500

def get_rutas_de_un_nodo(nodo):
    try:
        query = """ MATCH (n:Parada {nombre: '""" +nodo+ """'})-[r]-(m:Parada)
            WITH collect(DISTINCT type(r)) AS rutas
            RETURN [ruta IN rutas | REPLACE(ruta, "_", " ")] AS rutas"""

        response = graph.run(query).data()
    
        if not response or not response[0]['rutas']:
            error_message = "El nodo ingresado no existe"
            return {'error': error_message}, 404
        
        return response, 200
    
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500

def get_ruta_mas_corta(origen, destino):

    try: 

        origenExiste = get_one_node(origen)[0]
        if (origenExiste == []):
            return  {'error': 'El nodo origen no existe'}, 404
        
        destinoExiste = get_one_node(destino)[0]
        if (destinoExiste == []):
            return  {'error': 'El nodo destino no existe'}, 404


        query = """MATCH (origen:Parada {nombre: $origen}), (destino:Parada {nombre: $destino})
            WITH origen, destino, ['ruta_100', 'ruta_101', 'ruta_214', 'ruta_313', 'ruta_316', 'ruta_561', 'ruta_562'] AS rutas
            UNWIND rutas AS ruta
            CALL apoc.cypher.run('
            MATCH path = (o:Parada {nombre: $origen})-[*1..50]->(d:Parada {nombre: $destino})
            WHERE ALL(rel in relationships(path) WHERE type(rel) = $ruta)
            RETURN [node in nodes(path) | node.nombre] AS camino, $ruta AS ruta, reduce(coste = 0, rel in relationships(path) | coste + rel.coste) AS coste_total
            ORDER BY coste_total
            LIMIT 1
            ', {origen: origen.nombre, destino: destino.nombre, ruta: ruta}) YIELD value
            RETURN value.camino AS camino, value.ruta AS ruta, value.coste_total AS tiempo"""
            
        response = graph.run(query, origen=origen, destino=destino).data()
    
        
        if response == []:
            error_message = "No existe una ruta directa entre las Paradas"
            return {'error': error_message}, 404

        
        # Procesamos todas las rutas
        resultados_procesados = []
        for r in response:
            camino = r['camino']
            ruta = r['ruta']
            tiempo = r['tiempo']

            resultado = {
                'camino': camino,
                'ruta': ruta,
                'tiempo': tiempo
            }

            resultados_procesados.append(resultado)

        # Retornamos todas las rutas en un solo objeto JSON
        return {'rutas': resultados_procesados}, 200
    
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500
    

    
def get_coords(nodo):
    
    try:

        nodoExiste = get_one_node(nodo)[0]
        if (nodoExiste == []):
            return  {'error': 'El nodo no existe'}, 404
    
        query = """
        MATCH (n:Parada {nombre: $nodo})
        RETURN n.latitud AS latitud, n.longitud AS longitud
        """
        response = graph.run(query, nodo=nodo).data()
        return response, 200
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500
    
def get_list_of_coords(lista_nodos):
    try:
        query = """
            MATCH (p:Parada)
            WHERE p.nombre IN $nodos
            RETURN p.latitud AS latitud, p.longitud AS longitud, p.nombre AS nodo
        """
        response = graph.run(query, nodos=lista_nodos).data()
        
        if (response == []):
            return {'error': "La lista de nodos es invalida"}, 404

        return response, 200
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500
    

def get_one_node(nodo):
    try:
        query = """
            MATCH (p:Parada {nombre: $nodo})
            RETURN p
        """
        response = graph.run(query, nodo=nodo).data()
        return response, 200
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500


