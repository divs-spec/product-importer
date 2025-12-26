from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from .database import Base, engine
from .api import products, upload, jobs, webhooks

app = FastAPI()

@app.on_event("startup")
def create_tables():
    Base.metadata.create_all(bind=engine)

app.include_router(products.router)
app.include_router(upload.router)
app.include_router(jobs.router)
app.include_router(webhooks.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/")
def home():
    return templates.TemplateResponse("index.html", {"request": {}})
