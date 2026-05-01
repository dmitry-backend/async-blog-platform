import pytest
from app.crud import users as crud_users
from app.auth.security import hash_password

@pytest.mark.asyncio
async def test_create_get_user(test_db_session):
    user = await crud_users.create_user(test_db_session, "a@test.com", hash_password("StrongPass1!"))
    fetched = await crud_users.get_user_by_email(test_db_session, "a@test.com")
    assert fetched.id == user.id
