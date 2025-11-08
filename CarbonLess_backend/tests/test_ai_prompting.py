from config.test_helpers import TestHelpers
from tests.config.test_base import TestBase


class TestAIPrompting(TestBase, TestHelpers):

    async def setup(self):
        await super().setup()

        user = await self.register_and_login_user_for_test('testuser', 'test@example.com', '123')

        self.user_token = user.json()['token']

    async def test_healthy(self):
        response = await self.request(
            method='get',
            path='/api/scoring/healthy'
        )
        assert response.status_code == 200

    # async def test_submit_transportation_form(self):
    #     from src.services.tenants.models.models import Users, Tenants
    #
    #     tenant = await Tenants.create(
    #         display_name="Test Tenant",
    #         address="Djordja Stanojevica 9b, Belgrade, Serbia",
    #         address_coords="44.8066889954, 20.406828577"
    #     )
    #
    #     user = await Users.create(
    #         id_tenant=tenant.id,
    #         first_name="Test",
    #         last_name="User",
    #         username="testuser",
    #         email="test@example.com",
    #         password="securepassword",
    #         address="Bulevar Mihajla Pupina 171, Belgrade, Serbia",
    #         addres_coords="44.826618702, 20.4116531259"
    #     )
    #
    #     response = await self.request(
    #         method='get',
    #         path='/api/scoring/transportation',

