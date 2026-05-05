from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, posts
from app.cache.redis_cache import init_redis
from app.config import settings

app = FastAPI(
    title="AsyncBlog API",
    version="1.0.0",
    redirect_slashes=False
)

# --- Secure CORS using settings ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,   # Only your frontend + localhost
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_redis()
    print("🚀 AsyncBlog API started")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Include routers
app.include_router(users.router)
app.include_router(posts.router)

print(f"✅ CORS configured with {len(settings.ALLOWED_ORIGINS)} allowed origins")
