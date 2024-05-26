import pytest
import requests

# Definir la URL base de la API
BASE_URL = "http://api.tu-ruta-valledupar.site:5000"

def test_get_all_nodes():
    url = f"{BASE_URL}/Nodes/nodes"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert "Amaneceres del Valle" in json_data["nodos"]

def test_get_coords():
    nodo = "Amaneceres del Valle"
    url = f"{BASE_URL}/Nodes/nodes/get_coordenadas/{nodo}"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert isinstance(json_data["latitud"], float)
    assert isinstance(json_data["longitud"], float)

def test_get_route():
    ruta = "ruta_101"
    url = f"{BASE_URL}/Routes/rutas/ruta_individual/{ruta}"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert "ida" in json_data
    assert "vuelta" in json_data
    assert isinstance(json_data["ida"], list)
    assert isinstance(json_data["vuelta"], list)
    assert "Amaneceres del Valle" in json_data["ida"]
    assert "Amaneceres del Valle" in json_data["vuelta"]

def test_get_shortest_route():
    origen = "UPC Sabanas"
    destino = "UPC Hurtado"
    url = f"{BASE_URL}/Routes/rutas/ruta_mas_corta/{origen}/{destino}"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert "rutas" in json_data
    assert isinstance(json_data["rutas"], list)
    assert isinstance(json_data["rutas"][0]["camino"], list)
    assert origen in json_data["rutas"][0]["camino"]
    assert destino in json_data["rutas"][0]["camino"]
    assert isinstance(json_data["rutas"][0]["tiempo"], int)

def test_get_routes_from_node():
    nodo = "Amaneceres del Valle"
    url = f"{BASE_URL}/Routes/rutas/rutas_de_un_nodo/{nodo}"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert "rutas" in json_data
    assert isinstance(json_data["rutas"], list)
    assert "ruta 101" in json_data["rutas"]
    assert "ruta 100" in json_data["rutas"]

@pytest.mark.parametrize("origen,destino", [
    ("UPC Sabanas", "UPC Hurtado"),
    ("Amaneceres del Valle", "Hospital de La Nevada")
])
def test_multiple_shortest_routes(origen, destino):
    url = f"{BASE_URL}/Routes/rutas/ruta_mas_corta/{origen}/{destino}"
    response = requests.get(url)
    assert response.status_code == 200
    json_data = response.json()
    assert "rutas" in json_data
    assert isinstance(json_data["rutas"], list)
    assert origen in json_data["rutas"][0]["camino"]
    assert destino in json_data["rutas"][0]["camino"]
    assert isinstance(json_data["rutas"][0]["tiempo"], int)
