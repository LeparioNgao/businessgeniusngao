# Building the Python Backend(FastAPI)

# FastAPI is a Python web framework that turns Python functions into API endpoints.
# It handles JSON automatically. Each route is a function decorated with the HTTP method and path.

# main.py - run with: uvicorn main:app --reload
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

# Allow requests from your HTML file (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory store (replace with database in production)
checkins = []

class CheckIn(BaseModel):
    name:  str
    sleep: float
    water: int
    steps: int

# GET: return all check-ins
@app.get("/api/checkins")
def get_checkins():
    return checkins

# POST: receive a new check-in
@app.post("/api/checkins")
def add_checkin(data: CheckIn):
    entry = data.dict()
    entry["hit_goal"] = data.steps >= 10000
    checkins.append(entry)
    return {"success": True, "stored": entry}