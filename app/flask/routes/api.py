# Import server libraries
from flask import Blueprint

# Declare variable
module = Blueprint("api_routes", __name__)

# Declare function

# Declare FastAPI route
@module.route("/api/", methods=['GET'])
def show_api_information():
    return {"Server": "Flask Application"}

@module.route("/api/add/<int:number_1>/<int:number_2>", methods=['GET'])
def numeric_addition(number_1: int, number_2: int):
    return {"result": f"{number_1 + number_2}"}

@module.route("/api/str/<origin>/<target>/<replace>", methods=['GET'])
def string_replace(origin: str, target: str, replace: str):
    return {"result": f"{origin.replace(target, replace)}"}
