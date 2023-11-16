from httpx import AsyncClient
import pytest
import pytest_asyncio


@pytest.mark.parametrize('username, email, password, status_code', [
    ('Lena', 'Lena@example.com', 'Lena', 200),  # normal case
    ('Lena', 'Lena@example.com', 'Lena1', 409),  # case with existing username
    ('Igor', 'Igor', 'Igor', 422),  # case with invalid email
    ('Igor', 'Igor@example.com', 123, 422),  # case with invalid type of pass or another params
])
async def test_register_user(
        username: str,
        email: str,
        password: str,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.post('/auth/register', json={
        'username': username,
        'email': email,
        'password': password,
    })

    assert response.status_code == status_code


@pytest.mark.parametrize('username, password, status_code', [
    ('Lena', 'Lena', 200),  # normal case
    ('Lena', 'Lena', 200),  # repeated case
    ('Lena', 'Lenaa', 404),  # case with incorrect pass
    ('', '', 422),  # case with no params
])
async def test_login_user(
        username: str,
        password: str,
        status_code: int,
        async_client: AsyncClient,
):
    response = await async_client.post('/auth/login', data={
        'username': username,
        'password': password,
    })
    assert response.status_code == status_code
