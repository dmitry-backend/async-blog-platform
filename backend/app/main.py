from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import users, posts
from app.cache.redis_cache import init_redis
from app.config import settings

app = FastAPI(title="Async Blog Platform", version="1.0.0")

# === CHANGE 1: CORS Middleware - Must be at the very top ===
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,   # Uses your config list
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],                     # New: allows headers to be read by frontend
    max_age=3600,                             # New: caches preflight (OPTIONS) requests
)

# === CHANGE 2: Better startup logging for debugging ===
@app.on_event("startup")
async def startup_event():
    await init_redis()
    print("🚀 Async Blog Platform started successfully")
    print("Allowed CORS origins:", settings.ALLOWED_ORIGINS)   # ← This will show us what origins are allowed

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# === CHANGE 3: Routers must come AFTER CORS middleware ===
app.include_router(users.router)
app.include_router(posts.router)

# === CHANGE 4: Explicit port handling for Render ===
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    