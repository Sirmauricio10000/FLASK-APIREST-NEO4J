from flask_restx import Api
from py2neo import Graph
from neo4j.exceptions import Neo4jError


graph = Graph("neo4j+s://45486069.databases.neo4j.io", auth=("neo4j", "12345678"))
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
            WITH collect({coste: r.coste, ruta: type(r), tipo: r.tipo}) AS rutas
            RETURN rutas"""
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
        query = """MATCH (origen:Parada {nombre: $origen}), (destino:Parada {nombre: $destino})
            WITH origen, destino, ['ruta_100', 'ruta_101', 'ruta_214', 'ruta_313', 'ruta_316', 'ruta_561', 'ruta_562'] AS rutas
            UNWIND rutas AS ruta
            CALL apoc.cypher.run('
            MATCH path = (o:Parada {nombre: $origen})-[*1..50]->(d:Parada {nombre: $destino})
            WHERE ALL(rel in relationships(path) WHERE type(rel) = $ruta)
            RETURN [node in nodes(path) | node.nombre] AS camino, $ruta AS ruta, length(path) AS longitud
            ORDER BY longitud
            LIMIT 1
            ', {origen: origen.nombre, destino: destino.nombre, ruta: ruta}) YIELD value
            RETURN value.camino AS camino, value.ruta AS ruta, value.longitud AS longitud"""
            
        result = graph.run(query, origen=origen, destino=destino).data()
        
        resultados_procesados = []
        
        for r in result:
            camino = r['camino']
            ruta = r['ruta']
            longitud = r['longitud']
            
            resultado = {
                'camino': camino,
                'ruta': ruta,
                'longitud': longitud
            }
            
            resultados_procesados.append(resultado)
        
        response = {
            'origen': origen,
            'destino': destino,
            'resultados': resultados_procesados
        }
        
        if not response or not response['resultados']:
            error_message = "El nodo origen o destino no existe"
            return {'error': error_message}, 404

        return response, 200
    
    except Neo4jError as e:
        error_message = str(e)
        return {'error': error_message}, 500