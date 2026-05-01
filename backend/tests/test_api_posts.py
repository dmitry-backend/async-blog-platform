import pytest

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "email,password,title,content",
    [
        ("api1@test.com", "StrongPass1!", "First", "Post"),
        ("api2@test.com", "StrongPass1!", "Second", "Post"),
    ],
)
async def test_create_and_get_post(
    test_async_client,
    email,
    password,
    title,
    content,
):
    # register
    response = await test_async_client.post(
        "/users/register",
        json={"email": email, "password": password},
    )
    assert response.status_code in (200, 201)

    # login
    response = await test_async_client.post(
        "/users/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    data = response.json()
    token = data["access_token"]
    token_type = data["token_type"]
    headers = {"Authorization": f"{token_type} {token}"}

    # create post
    response = await test_async_client.post(
        "/posts/",
        json={"title": title, "content": content},
        headers=headers,
    )
    assert response.status_code in (200, 201)
    post_id = response.json()["id"]

    # get post
    response = await test_async_client.get(
        f"/posts/{post_id}",
        headers=headers,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == title
    assert data["content"] == content
    