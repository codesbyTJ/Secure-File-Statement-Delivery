from fastapi import FastAPI
from app.routers import auth, downloads
from app.db import Base, engine

app = FastAPI(title="Secure File Statement Delivery API")

# Create database tables on startup
@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

# Register routers
app.include_router(downloads.router, prefix="/statements", tags=["Downloads"])
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])

@app.get("/")
async def root():
    return {"message": "Secure File Statement Delivery API is running "}
