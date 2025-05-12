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

@app.post("/feed", summary="Нагодувати тамагочі", description="Цей ендпоінт збільшує рівень ситості тамагочі на 10 (максимум 100).")
def feed():
    state = load_state()
    state.hunger = min(state.hunger + 10, 100)  # максимум 100
    save_state(state)
    return {"message": "Тамагочі нагодовано!", "state": state}

@app.post("/play", summary="Пограти з тамагочі", description="Цей ендпоінт збільшує рівень щастя тамагочі на 10 (максимум 100).")
def play():
    state = load_state()
    state.happiness = min(state.happiness + 10, 100)
    save_state(state)
    return {"message": "Тамагочі пограв!", "state": state}

@app.get("/status", summary="Перевірити стан тамагочі", description="Цей ендпоінт повертає поточний стан ситості та щастя тамагочі.")
def status():
    state = load_state()
    return {"state": state}

@app.get("/feelings", summary="Емоційний стан тамагочі", description="Цей ендпоінт на основі рівня ситості та щастя визначає емоційний стан тамагочі.")
def feelings():
    state = load_state()
    
    if state.hunger < 30:
        return {"emotion": "Я голодний! 😢"}
    if state.happiness < 30:
        return {"emotion": "Мені нудно... 😞"}
    return {"emotion": "Я щасливий! 😊"}
