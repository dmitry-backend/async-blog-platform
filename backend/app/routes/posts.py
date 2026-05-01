from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.crud import posts as crud_posts
from app.cache.redis_cache import (
    get_cache,
    set_cache,
    clear_paginated_posts_cache,
    create_paginated_posts_cache_key,
    create_post_id_key,
)
from app.schemas import PostCreate, PostRead, PostUpdate
from app.routes.dependencies import get_current_user
from app.models import User


router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostRead)
async def create_post(
    payload: PostCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    post = await crud_posts.create_post(
        session,
        payload.title,
        payload.content,
        current_user.id,
    )

    cache_key = create_post_id_key(post.id)
    await set_cache(cache_key, {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "created_at": post.created_at.isoformat(),
        "is_public": post.is_public,
    })

    return post


@router.get("/", response_model=list[PostRead])
async def list_posts(
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1),
    session: AsyncSession = Depends(get_session),
):
    """Simple version without cache for now"""
    offset = (page - 1) * size
    
    result = await crud_posts.get_paginated_posts(session, offset, size)
    
    # Extract only the posts list (ignore total for now)
    posts = result["posts"] if isinstance(result, dict) else result
    
    return posts


@router.get("/{post_id}", response_model=PostRead)
async def get_post(
    post_id: int,
    session: AsyncSession = Depends(get_session),
):

    cache_key = create_post_id_key(post_id)
    cached = await get_cache(cache_key)
    if cached:
        return PostRead(**cached)

    post = await crud_posts.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    await set_cache(cache_key, {
        "id": post.id,
        "title": post.title,
        "content": post.content,
        "author_id": post.author_id,
        "created_at": post.created_at.isoformat(),
        "is_public": post.is_public,
    })

    return post


@router.put("/{post_id}", response_model=PostRead)
async def update_post(
    post_id: int,
    payload: PostUpdate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    post = await crud_posts.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    updated = await crud_posts.update_post(
        session,
        post,
        payload.title,
        payload.content,
    )

    await set_cache(create_post_id_key(post_id), {
        "id": updated.id,
        "title": updated.title,
        "content": updated.content,
        "author_id": updated.author_id,
        "created_at": updated.created_at.isoformat(),
        "is_public": updated.is_public,
    })

    return updated


@router.delete("/{post_id}")
async def delete_post(
    post_id: int,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):

    post = await crud_posts.get_post_by_id(session, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    if post.author_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")

    await crud_posts.delete_post(post)

    await set_cache(create_post_id_key(post_id), None, ttl=1)

    return {"detail": "Deleted"}
