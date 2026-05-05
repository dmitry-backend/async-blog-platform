from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

from app.routes import users, posts
from app.cache.redis_cache import init_redis
from app.config import settings

app = FastAPI(
    title="AsyncBlog API",
    version="1.0.0"
)

# Secure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    await init_redis()
    print(f"🚀 AsyncBlog API started on port {os.getenv('PORT', 'unknown')}")

@app.get("/health")
async def health_check():
    return {"status": "ok", "port": os.getenv("PORT")}

app.include_router(users.router)
app.include_router(posts.router)


# This is important for Render
if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
    