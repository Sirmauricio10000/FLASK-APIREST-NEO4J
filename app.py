from flask import Flask, redirect, url_for
from apis import api

app = Flask(__name__)

# Configura la instancia de Api
api.init_app(app)

# Ruta para servir la interfaz Swagger
@app.route('/api/swagger')
def render_swagger():
    # Configura el URL de la documentación Swagger
    swagger_url = url_for('api.swagger_json')
    return redirect(swagger_url)

# Resto de la configuración de Swagger UI

if __name__ == '__main__':
    app.run(debug=True, port=8080)
