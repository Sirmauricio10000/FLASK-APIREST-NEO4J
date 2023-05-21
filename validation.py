from flask_restx import Api
from py2neo import Graph


graph = Graph("bolt://localhost:7687", auth=("neo4j", "12345678"))
api = Api()


def get_all_nodes():
    response = graph.run("MATCH (n) RETURN n").data()
    return response

def get_route(ruta):
    query = "MATCH (n:Parada)-[r:" + ruta + "]->(m:Parada) RETURN collect(n.nombre) AS camino"
    result = graph.run(query).data()
    response = {
        'nodes': result
    }
    return response

def get_ruta_mas_corta(origen, destino):
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

    print(result)
    
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
    
    return response