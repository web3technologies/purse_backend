import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture(scope="function")
def get_user_token(api_client):
    user = get_user_model().objects.get(id=1)
    login_data = {
        "email": user.email,
        "password": "Testing321."
    }
    
    # get token
    token_url = reverse('token_obtain_pair')
    res = api_client.post(token_url, login_data, format='json')
    return res.data


@pytest.fixture(scope="function")
def authenticated_api_client(api_client, get_user_token):
    api_client.credentials(HTTP_AUTHORIZATION='Bearer ' + get_user_token['access'])
    return api_client