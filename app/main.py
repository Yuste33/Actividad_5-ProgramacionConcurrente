from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager
from fastapi.responses import HTMLResponse
import os
from app.api import websockets, routes
from app.services.processor import processor

@asynccontextmanager
async def lifespan(app: FastAPI):
    processor.start()
    yield
    processor.stop()

app = FastAPI(
    title="Jurassic Park Monitor",
    version="1.0.0",
    lifespan=lifespan
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

app.include_router(routes.router, prefix="/api")

app.include_router(websockets.router, prefix="/ws")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})