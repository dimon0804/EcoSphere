import asyncio
from fastapi import FastAPI
import uvicorn
import admin
import admin.routers
from database import Base, engine
from routers import *
from models import *
from fastapi.middleware.cors import CORSMiddleware
import routers

app = FastAPI(title="EcoSphere API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Для разработки. В проде укажите домен фронта.
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, OPTIONS и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)

async def init_db():
    print("Initializing the database...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            print("Database initialized successfully.")
    except Exception as e:
        print(f"Error initializing the database: {e}") 

async def startup():
    print("Starting DB initialization...")
    await init_db()
    print("Database setup complete or skipped.")

@app.on_event("startup")
async def on_startup():
    await startup()

# Подключаем роутеры
app.include_router(routers.user.router)
app.include_router(routers.project.router)
# app.include_router(donation.router)
app.include_router(routers.organization.router) 
app.include_router(admin.routers.admin_router)

# Добавьте это для статических файлов
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="admin/static"), name="static")