# Import server libraries
from flask import Flask
import importlib.metadata

# Import server modules
from routes import api

# Configuration server
app = Flask(__name__)
app.register_blueprint(api.module)

# Configuration server root route
@app.route("/", methods=['GET'])
def show_flask_information():
    flask_version=importlib.metadata.version("flask")
    return {"Server": "Flask Server", "Version": f"{flask_version}"}
