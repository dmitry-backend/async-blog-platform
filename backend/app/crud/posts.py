from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func  # FIX: added func for COUNT query

from app.models import Post
from app.cache.redis_cache import clear_paginated_posts_cache


async def create_post(session: AsyncSession, title: str, content: str, user_id: int) -> Post:
    post = Post(title=title, content=content, author_id=user_id)
    session.add(post)
    await session.commit()
    await session.refresh(post)

    await clear_paginated_posts_cache()
    return post


# FIX: changed return type from list[Post] → dict (posts + total)
async def get_paginated_posts(session: AsyncSession, offset: int, limit: int):
    # FIX: fetch paginated posts
    result = await session.execute(
        select(Post)
        .order_by(Post.created_at.desc())
        .offset(offset)
        .limit(limit)
    )
    posts = result.scalars().all()

    # FIX: added total count query (needed for frontend pagination)
    total_result = await session.execute(
        select(func.count(Post.id))
    )
    total = total_result.scalar()

    # FIX: return structured response instead of raw list
    return {
        "posts": posts,
        "total": total
    }


async def get_post_by_id(session: AsyncSession, post_id: int) -> Post | None:
    return await session.get(Post, post_id)


async def update_post(session: AsyncSession, post: Post, title: str, content: str) -> Post:
    post.title = title
    post.content = content
    await session.commit()
    await session.refresh(post)

    await clear_paginated_posts_cache()
    return post


async def delete_post(session: AsyncSession, post: Post):
    await session.delete(post)
    await session.commit()

    await clear_paginated_posts_cache()
    