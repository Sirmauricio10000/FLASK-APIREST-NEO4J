import unittest
import requests

class TestGetAllNodes(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Nodes/nodes"  

    def test_get_all_nodes_check_status_code(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_all_nodes_check_list_items(self): 
        response = requests.get(self.url)
        json_data = response.json()
        self.assertIn("Amaneceres del Valle", json_data["nodos"])

class TestGetCoords(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Nodes/nodes/get_coordenadas/"
    
    def test_get_coordenadas_check_status_code(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 200)

    def test_get_coordenadas_invalid_node_status_code(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 404)

    def test_get_coordenadas_invalid_node_error_message(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertEqual("El nodo no existe", json_data["error"])

    def test_get_coordenadas_body(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertTrue(isinstance(json_data["latitud"], float))
        self.assertTrue(isinstance(json_data["longitud"], float))

class TestGetLisOfCoords(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Nodes/nodes/get_lista_coordenadas/"
    
    def test_get_coordenadas_check_status_code(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 200)

    def test_get_coordenadas_invalid_node_status_code(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 404)

    def test_get_coordenadas_invalid_node_error_message(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertEqual("La lista de nodos es inválida", json_data["error"])

    def test_get_coordenadas_body(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertTrue(isinstance(json_data["coordenadas"][0][0], float))
        self.assertTrue(isinstance(json_data["coordenadas"][0][1], float))

class TestGetRoutes(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Routes/rutas/ruta_individual/"
    
    def test_get_route_check_status_code(self):
        ruta = "ruta_101"
        response = requests.get(self.url + ruta)
        self.assertEqual(response.status_code, 200)

    def test_get_route_invalid_route_status_code(self):
        ruta = "Invalid"
        response = requests.get(self.url + ruta)
        self.assertEqual(response.status_code, 404)

    def test_get_routes_invalid_route_error_message(self):
        ruta = "Invalid"
        response = requests.get(self.url + ruta)
        json_data = response.json()
        self.assertEqual("La ruta no existe", json_data["error"])

    def test_get_route_body(self):
        ruta = "ruta_101"
        response = requests.get(self.url + ruta)
        json_data = response.json()
        self.assertIn("ida", json_data)
        self.assertIn("vuelta", json_data)
        self.assertTrue(isinstance(json_data["ida"], list))
        self.assertTrue(isinstance(json_data["vuelta"], list))
        self.assertIn("Amaneceres del Valle", json_data["ida"])
        self.assertIn("Amaneceres del Valle", json_data["vuelta"])

class TestGetShortestRoute(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Routes/rutas/ruta_mas_corta/"
    
    def test_get_shortest_route_check_status_code(self):
        origen = "UPC Sabanas"
        destino = "UPC Hurtado"
        response = requests.get(self.url + origen + "/" + destino)
        self.assertEqual(response.status_code, 200)

    def test_get_shortest_route_invalid_nodes_status_code(self):
        origen = "Invalid Origin"
        destino = "Invalid Destination"
        response = requests.get(self.url + origen + "/" + destino)
        self.assertEqual(response.status_code, 404)

    def test_get_shortest_route_invalid_nodes_error_message(self):
        origen = "Invalid Origin"
        destino = "Invalid Destination"
        response = requests.get(self.url + origen + "/" + destino)
        json_data = response.json()
        self.assertEqual("Uno o ambos nodos no existen", json_data["error"])

    def test_get_shortest_route_body(self):
        origen = "UPC Sabanas"
        destino = "UPC Hurtado"
        response = requests.get(self.url + origen + "/" + destino)
        json_data = response.json()
        self.assertIn("rutas", json_data)
        self.assertTrue(isinstance(json_data["rutas"], list))
        self.assertTrue(isinstance(json_data["rutas"][0]["camino"], list))
        self.assertIn("UPC Sabanas", json_data["rutas"][0]["camino"])
        self.assertIn("UPC Hurtado", json_data["rutas"][0]["camino"])
        self.assertTrue(isinstance(json_data["rutas"][0]["tiempo"], int))

class TestGetRoutesFromNode(unittest.TestCase):

    url = "http://api.tu-ruta-valledupar.site:5000/Routes/rutas/rutas_de_un_nodo/"
    
    def test_get_routes_from_node_check_status_code(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 200)

    def test_get_routes_from_node_invalid_node_status_code(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        self.assertEqual(response.status_code, 404)

    def test_get_routes_from_node_invalid_node_error_message(self):
        nodo = "Invalid Node"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertEqual("El nodo ingresado no existe", json_data["error"])

    def test_get_routes_from_node_body(self):
        nodo = "Amaneceres del Valle"
        response = requests.get(self.url + nodo)
        json_data = response.json()
        self.assertIn("rutas", json_data)
        self.assertTrue(isinstance(json_data["rutas"], list))
        self.assertIn("ruta 101", json_data["rutas"])
        self.assertIn("ruta 100", json_data["rutas"])

if __name__ == '__main__':
    unittest.main()
