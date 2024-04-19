from neomodel import config, StructuredNode, StringProperty, FloatProperty, db
import os
from flask import Flask
from flask_restx import Api, Resource


# Configuración de conexión a la base de datos
NEO4J_URI=os.getenv("NEO4J_URI")
config.DATABASE_URL = NEO4J_URI

# Definición del modelo de datos
class Parada(StructuredNode):
    nombre = StringProperty(unique_index=True, required=True)
    latitud = FloatProperty()
    longitud = FloatProperty()

api = Api()

def get_all_nodes():
    query = "MATCH (n:Parada) RETURN collect(n.nombre) AS nodos"
    results, meta = db.cypher_query(query)
    return {'nodos': results[0][0] if results else []}, 200

def get_route(ruta):
    try:
        query = f"""
        MATCH (n:Parada)-[r:{ruta}]->(m:Parada)
        WITH COLLECT(n) + COLLECT(m) AS nodos, r
        UNWIND nodos AS nodo
        WITH collect(DISTINCT CASE WHEN r.tipo = "ida" THEN nodo.nombre ELSE null END) AS ida,
             collect(DISTINCT CASE WHEN r.tipo = "vuelta" THEN nodo.nombre ELSE null END) AS vuelta
        RETURN {{ ida: ida, vuelta: vuelta }} AS camino
        """
        results, meta = db.cypher_query(query)
        if not results or not results[0][0]['ida']:
            return {'error': "La ruta no existe"}, 404
        return results[0][0], 200
    except Exception as e:
        return {'error': str(e)}, 500
    


def get_rutas_de_un_nodo(nodo):
    try:
        query = "MATCH (n:Parada {nombre: $nodo})-[r]-(m:Parada) RETURN collect(DISTINCT type(r)) AS rutas"
        params = {'nodo': nodo}
        results, meta = db.cypher_query(query, params)
        rutas = [r.replace('_', ' ') for r in results[0][0]] if results else []
        if not rutas:
            return {'error': "El nodo ingresado no existe"}, 404
        return {'rutas': rutas}, 200
    except Exception as e:
        return {'error': str(e)}, 500


def get_ruta_mas_corta(origen, destino):
    try:
        # Comprobamos si ambos nodos existen usando neomodel
        origen_exists = Parada.nodes.get_or_none(nombre=origen)
        destino_exists = Parada.nodes.get_or_none(nombre=destino)
        if not origen_exists or not destino_exists:
            return {'error': 'Uno o ambos nodos no existen'}, 404

        # Preparamos la consulta Cypher utilizando APOC para buscar la ruta más corta
        query = """
        MATCH (origen:Parada {nombre: $origen}), (destino:Parada {nombre: $destino})
        WITH origen, destino
        UNWIND ['ruta_100', 'ruta_101', 'ruta_214', 'ruta_313', 'ruta_316', 'ruta_561', 'ruta_562'] AS ruta
        CALL apoc.cypher.run(
            'MATCH path = (o:Parada {nombre: $origen})-[*1..50]->(d:Parada {nombre: $destino})
            WHERE ALL(rel in relationships(path) WHERE type(rel) = $ruta)
            RETURN [node in nodes(path) | node.nombre] AS camino, $ruta AS ruta, reduce(coste = 0, rel in relationships(path) | coste + rel.coste) AS coste_total
            ORDER BY coste_total
            LIMIT 1', {origen: $origen, destino: $destino, ruta: ruta}) YIELD value
        RETURN value.camino AS camino, value.ruta AS ruta, value.coste_total AS tiempo
        """
        params = {'origen': origen, 'destino': destino}
        results, meta = db.cypher_query(query, params)

        # Procesamos las rutas y formateamos la respuesta
        if not results:
            return {'error': 'No existe una ruta directa entre las paradas'}, 404
        
        resultados_procesados = [{'camino': r[0], 'ruta': r[1], 'tiempo': r[2]} for r in results]
        return {'rutas': resultados_procesados}, 200
    except Exception as e:
        return {'error': str(e)}, 500

    
    
def get_coords(nodo):
    try:
        node = Parada.nodes.get(nombre=nodo)
        return {'latitud': node.latitud, 'longitud': node.longitud}, 200
    except Parada.DoesNotExist:
        return {'error': 'El nodo no existe'}, 404
    except Exception as e:
        return {'error': str(e)}, 500

    
def get_list_of_coords(lista_nodos):
    try:
        query = "MATCH (p:Parada) WHERE p.nombre IN $nodos RETURN p.latitud AS latitud, p.longitud AS longitud, p.nombre AS nodo"
        params = {'nodos': lista_nodos}
        results, meta = db.cypher_query(query, params)
        if not results:
            return {'error': "La lista de nodos es inválida"}, 404
        return {'coordenadas': results}, 200
    except Exception as e:
        return {'error': str(e)}, 500

    

def get_one_node(nodo):
    try:
        node = Parada.nodes.get_or_none(nombre=nodo)
        return {'nodo': node.nombre} if node else {'error': 'El nodo no existe'}, 404
    except Exception as e:
        return {'error': str(e)}, 500



