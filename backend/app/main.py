from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import users, posts
from app.cache.redis_cache import init_redis

app = FastAPI(title="AsyncBlog API")

# --- PERMISSIVE CORS FOR PRODUCTION ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Allow all origins
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

app.include_router(users.router)
app.include_router(posts.router)

print("✅ CORS middleware with * applied")
