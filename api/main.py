from fastapi import FastAPI
from .database import engine
from .routers import task_routes,auth_routes
from . import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)
app.include_router(task_routes.router)
app.include_router(auth_routes.router)