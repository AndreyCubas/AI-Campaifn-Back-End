from fastapi import FastAPI

from app.core.database import Base, engine
from app.api.endpoints import auth, campaigns, categories, donations, misc, updates, users
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="AI-Campaign-Back-End API 🚀")
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(misc.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(campaigns.router)
app.include_router(donations.router)
app.include_router(updates.router)