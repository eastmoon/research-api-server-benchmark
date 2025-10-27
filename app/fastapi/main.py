# Import server libraries
from fastapi import FastAPI
from fastapi import __version__ as fastapi_version

# Close Garbage Collector
import gc
gc.disable()

# Import server modules
from routes import api

# Configuration server
app = FastAPI()
app.mount("/api", api.module)

# Configuration server root route
@app.get("/")
def show_fastapi_information():
    return {"Server": "FastAPI Server", "Version": f"{fastapi_version}"}
