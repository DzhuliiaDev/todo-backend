from typing import Union
from fastapi import FastAPI
from pydantic_settings import BaseSettings
from resources import EntryManager, Entry
import uvicorn
from typing import List
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://wexler.io"  # адрес на котором работает фронт-энд
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,    # Список разрешенных доменов
    allow_credentials=True,   # Разрешить Cookies и Headers
    allow_methods=["*"],      # Разрешить все HTTP методы
    allow_headers=["*"],      # Разрешить все хедеры
)



class Settings(BaseSettings):
    data_folder: str = '/tmp/'

settings = Settings()

@app.get("/")
async def hello_world():
    return {"Hello": "World"}


@app.get("/api/entries/")
async def get_entries():
    data_path = settings.data_folder
    entry_manager = EntryManager(data_path)
    entry_manager.load()
    entries = entry_manager.entries
    res = [entry.json() for entry in entries]
    return res

@app.get("/api/get_data_folder/")
async def get_data_folder():
    return {'folder': settings.data_folder}

@app.post('/api/save_entries/')
async def save_entries(data: List[dict]):
    entry_manager = EntryManager(settings.data_folder)
    for item in data:
        entry = Entry.from_json(item)
        entry_manager.entries.append(entry)
    entry_manager.save()
    return {'status': 'success'}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)