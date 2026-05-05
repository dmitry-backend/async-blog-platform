from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import users, posts
from app.cache.redis_cache import init_redis
from app.config import settings

app = FastAPI(
    title="Async Blog Platform",
    version="1.0.0"
)

# CORS - Must be added BEFORE including routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_redis()
    print("🚀 Async Blog Platform started successfully")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Important: Include routers AFTER CORS middleware
app.include_router(users.router)
app.include_router(posts.router)

# For Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    