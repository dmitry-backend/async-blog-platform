from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routes import users, posts
from app.cache.redis_cache import init_redis

app = FastAPI(
    title="AsyncBlog API",
    version="1.0.0",
    redirect_slashes=False
)

# --- VERY PERMISSIVE CORS FOR DEVELOPMENT ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins (safe for local dev)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Startup ---
@app.on_event("startup")
async def startup_event():
    await init_redis()
    print(f"🚀 {settings.APP_NAME} started in {settings.ENVIRONMENT} mode")

# --- Health ---
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# --- Routers ---
app.include_router(users.router)
app.include_router(posts.router)

print("✅ CORS middleware applied with allow_origins=*")
