# Import server libraries
from fastapi import FastAPI, Request

# Import algorithm-service-application command-interface-line pacakge

# Declare variable
module = FastAPI()

# Declare function

# Declare FastAPI route
@module.get("/")
def show_api_information():
    return {"Server": "FastAPI Application"}

@module.get("/add/{number_1}/{number_2}")
def numeric_addition(number_1: int, number_2: int):
    return {"result": f"{number_1 + number_2}"}

@module.get("/str/{origin}/{target}/{replace}")
def string_replace(origin: str, target: str, replace: str):
    return {"result": f"{origin.replace(target, replace)}"}
