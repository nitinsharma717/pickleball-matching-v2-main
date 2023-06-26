# main.py
# Import FastAPI
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from api import api

# Initialize the app
app = FastAPI()

app.include_router(api.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(api.router)

# GET operation at route '/'
@app.get('/')
def root_api():
    return {"message": "HEE HEE HEE HAW! OOH HOO HOO HUI! GRRRRR!"}
