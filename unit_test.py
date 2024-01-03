import unittest
import requests

class TestGetAllNodes(unittest.TestCase):

    url = "http://127.0.0.1:5000/Nodes/nodes"  

    def test_get_all_nodes_check_status_code(self):
        response = requests.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_get_all_nodes_check_list_items(self): 
        response = requests.get(self.url)
        json_data = response.json()
        self.assertIn("Amaneceres del Valle", json_data[0]["nodos"])

class TestGetCoords(unittest.TestCase):

    url = "http://127.0.0.1:5000/Nodes/nodes/get_coordenadas/"
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
        self.assertTrue(isinstance(json_data[0]["latitud"], float))
        self.assertTrue(isinstance(json_data[0]["longitud"], float))



if __name__ == '__main__':
    unittest.main()
