import os
import json
import asyncio

from fastapi import FastAPI, Body
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

class TamagotchiState(BaseModel):
    name: str  # Ім'я тамагочі
    satiety: int = 50
    happiness: int = 50

def load_state(user_id: str) -> TamagotchiState:
    state_file = os.path.join(os.path.dirname(__file__), f"../data/state_{user_id}.json")
    if not os.path.exists(state_file):
        raise FileNotFoundError(f"Файл стану для користувача {user_id} не знайдено.")

    with open(state_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    return TamagotchiState(**data)

def save_state(user_id: str, state: TamagotchiState):
    state_file = os.path.join(os.path.dirname(__file__), f"../data/state_{user_id}.json")
    data_to_save = state.dict()
    with open(state_file, "w", encoding="utf-8") as f:
        json.dump(data_to_save, f, ensure_ascii=False, indent=4)

async def decrease_state():
    while True:
        # Отримуємо список усіх файлів стану користувачів
        data_dir = os.path.join(os.path.dirname(__file__), "../data")
        user_files = [f for f in os.listdir(data_dir) if f.startswith("state_") and f.endswith(".json")]

        for user_file in user_files:
            # Витягуємо user_id з імені файлу
            user_id = user_file.replace("state_", "").replace(".json", "")
            state = load_state(user_id)

            # Зменшуємо рівень ситості та щастя
            state.satiety = max(state.satiety - 1, 0)
            state.happiness = max(state.happiness - 1, 0)

            # Зберігаємо оновлений стан
            save_state(user_id, state)

        # Чекаємо 60 секунд перед наступним циклом
        await asyncio.sleep(60)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(decrease_state())

@app.post("/feed/{user_id}", summary="Нагодувати тамагочі")
def feed(user_id: str):
    state = load_state(user_id)
    state.satiety = min(state.satiety + 10, 100)
    save_state(user_id, state)
    return {"message": "Тамагочі нагодовано!", "state": state}

@app.post("/play/{user_id}", summary="Пограти з тамагочі")
def play(user_id: str):
    state = load_state(user_id)
    state.happiness = min(state.happiness + 10, 100)
    save_state(user_id, state)
    return {"message": "Тамагочі пограв!", "state": state}

@app.get("/status/{user_id}", summary="Перевірити стан тамагочі")
def status(user_id: str):
    try:
        state = load_state(user_id)
        return {"state": state}
    except FileNotFoundError:
        return {"error": f"Тамагочі з UID {user_id} не знайдено."}

@app.get("/feelings/{user_id}", summary="Емоційний стан тамагочі")
def feelings(user_id: str):
    state = load_state(user_id)
    if state.satiety < 30:
        return {"emotion": "Я голодний! 😢"}
    if state.happiness < 30:
        return {"emotion": "Мені нудно... 😞"}
    return {"emotion": "Я щасливий! 😊"}

@app.post("/create", summary="Створити нового тамагочі")
def create_tamagochi(data: dict = Body(...)):
    user_id = data.get("user_id")
    name = data.get("name")

    if not user_id or not name:
        return {"message": "UID та ім'я обов'язкові."}

    state_file = os.path.join(os.path.dirname(__file__), f"../data/state_{user_id}.json")
    if os.path.exists(state_file):
        return {"message": "Тамагочі з таким UID вже існує."}

    # Створюємо початковий стан з ім'ям
    state = TamagotchiState(name=name, satiety=50, happiness=50)
    save_state(user_id, state)

    return {"message": f"Тамагочі '{name}' створено!"}

@app.get("/", response_class=HTMLResponse, summary="Головна сторінка", description="Цей ендпоінт повертає HTML-файл.")
def root():
    with open("./frontend/index.html", "r", encoding="utf-8") as f:
        html_content = f.read()
    return HTMLResponse(content=html_content)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
