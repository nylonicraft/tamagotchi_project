from fastapi import FastAPI
from pydantic import BaseModel
import json
import os

app = FastAPI()

STATE_FILE = "state.json"

class TamagotchiState(BaseModel):
    hunger: int
    happiness: int

def load_state() -> TamagotchiState:
    if not os.path.exists(STATE_FILE):
        # Створюємо початковий стан, якщо файл відсутній
        initial_state = TamagotchiState(hunger=50, happiness=50)
        save_state(initial_state)
        return initial_state

    with open(STATE_FILE, "r") as f:
        data = json.load(f)
    return TamagotchiState(**data)

def save_state(state: TamagotchiState):
    with open(STATE_FILE, "w") as f:
        json.dump(state.dict(), f)

@app.post("/feed")
def feed():
    state = load_state()
    state.hunger = min(state.hunger + 10, 100)  # максимум 100
    save_state(state)
    return {"message": "Тамагочі нагодовано!", "state": state}

@app.post("/play")
def play():
    state = load_state()
    state.happiness = min(state.happiness + 10, 100)
    save_state(state)
    return {"message": "Тамагочі пограв!", "state": state}

@app.get("/status")
def status():
    state = load_state()
    return {"state": state}
