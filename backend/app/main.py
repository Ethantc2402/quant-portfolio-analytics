from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .init_db import init_db
from .db import SessionLocal

from app.routers import analytics


app = FastAPI(
    title="Quant Portfolio Analytics API",
    version="0.1.0",
    description="Backend API for a full-stack quant portfolio analytics platform.",
)

app.include_router(analytics.router, prefix="/api", tags=["analytics"])

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    # This should CREATE TABLE instruments/prices/portfolios/holdings/trades
    init_db()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-test")
def db_test():
    db = SessionLocal()
    try:
        result = db.execute(text("SELECT COUNT(*) FROM portfolios"))
        count = result.scalar() or 0
        return {"portfolios_count": int(count)}
    finally:
        db.close()
