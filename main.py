from fastapi import FastAPI
from routers import user, project, donation
from database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="GreenFinance API")

app.include_router(user.router)
app.include_router(project.router)
app.include_router(donation.router)