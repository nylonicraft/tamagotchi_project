from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Дозвіл на запити з фронтенду
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # для dev-режиму
    allow_methods=["*"],
    allow_headers=["*"],
)

# Початковий стан тамагочі
tamagochi_state = {
    "hunger": 5,
    "mood": 5
}

@app.get("/status")
def get_status():
    return tamagochi_state

@app.post("/feed")
def feed():
    tamagochi_state["hunger"] = max(0, tamagochi_state["hunger"] - 1)
    return {"message": "You fed the Tamagochi!"}

@app.post("/play")
def play():
    tamagochi_state["mood"] = min(10, tamagochi_state["mood"] + 1)
    return {"message": "You played with the Tamagochi!"}