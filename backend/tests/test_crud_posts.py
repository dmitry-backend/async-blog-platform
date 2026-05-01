import pytest
from app.crud import posts as crud_posts
from app.crud import users as crud_users
from app.auth.security import hash_password

@pytest.mark.asyncio
async def test_post_crud(test_db_session):
    user = await crud_users.create_user(test_db_session, "b@test.com", hash_password("StrongPass1!"))
    post = await crud_posts.create_post(test_db_session, "Title", "Content", user.id)
    assert post.title == "Title"

    post = await crud_posts.update_post(test_db_session, post, "New", "Updated")
    assert post.title == "New"

    await crud_posts.delete_post(test_db_session, post)
    assert await crud_posts.get_post_by_id(test_db_session, post.id) is None
