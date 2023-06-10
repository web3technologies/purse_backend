import pytest


@pytest.mark.django_db
class TestTokenView:

    def test_get_token(self, get_user_token):
        assert get_user_token.get("refresh") and get_user_token.get("access")