from pydantic import EmailStr


class TestHelpers:
    async def register_and_login_user_for_test(self, username: str, email: EmailStr, first_name: str, last_name: str):
        response = await self.request('post', '/api/users/register', {'username': username, 'email': email, 'first_name': first_name, 'last_name': last_name})
        assert response.status_code == 200
        data = response.json()

        password = data['password']
        response = await self.request('post', '/api/users/login', {'username': username, 'password': password})
        assert response.status_code == 200
        return response