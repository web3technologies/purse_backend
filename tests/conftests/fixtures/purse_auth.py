import pytest

from purse_auth.models import User

@pytest.fixture
def user():
    return User.objects.create_user(email='testuser@example.com', password='password')
