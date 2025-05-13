import os
import json
import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="./frontend"), name="static")

STATE_FILE = os.path.join(os.path.dirname(__file__), "../data/state.json")

class TamagotchiState(BaseModel):
    satiety: int = 50
    happiness: int = 50

def load_state() -> TamagotchiState:
    if not os.path.exists(STATE_FILE):
        initial_state = TamagotchiState(satiety=50, happiness=50)
        save_state(initial_state)
        return initial_state

    with open(STATE_FILE, "r") as f:
        data = json.load(f)
    return TamagotchiState(**data)

def save_state(state: TamagotchiState):
    data_to_save = state.dict()
    with open(STATE_FILE, "w") as f:
        json.dump(data_to_save, f)

async def decrease_state():
    while True:
        state = load_state()
        state.satiety = max(state.satiety - 1, 0)
        state.happiness = max(state.happiness - 1, 0)
        save_state(state)
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(decrease_state())

@app.post("/feed", summary="Нагодувати тамагочі", description="Цей ендпоінт збільшує рівень ситості тамагочі на 10 (максимум 100).")
def feed():
    state = load_state()
    print(state)
    state.satiety = min(state.satiety + 10, 100)
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
    
    if state.satiety < 30:
        return {"emotion": "Я голодний! 😢"}
    if state.happiness < 30:
        return {"emotion": "Мені нудно... 😞"}
    return {"emotion": "Я щасливий! 😊"}

@app.get("/", response_class=HTMLResponse, summary="Головна сторінка", description="Цей ендпоінт повертає HTML-файл.")
def root():
    with open("./frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
