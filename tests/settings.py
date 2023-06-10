from purse_backend.settings.settings import *
import os
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent

FIXTURES_DIRS = os.path.join(BASE_DIR, "fixtures/")
REF_FIXTURES_DIR = os.path.join(BASE_DIR, "ref_fixtures/")

PLAID_API_ENVIRONMENT_CONFIGURATION = Configuration(
        host=Environment.Sandbox,
            api_key={
                'clientId': None,
                'secret': None,
                'plaidVersion': '2020-09-14'
            }
        )

DATABASES = {
    'default': {
        "NAME": "purse_finance_unittest",
        "ENGINE": "django.db.backends.postgresql",
        "USER": "personal_assistant",
        "HOST": "localhost",
        'PASSWORD': "testing321"
    }
}