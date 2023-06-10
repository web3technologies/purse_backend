from purse_backend.settings.settings import *


DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = [
    "http://int.personalassistant.com",
    "http://int.purse.com"
]

STATIC_ROOT = f"/personal_assistant_frontend_int/src"   #collectstatic places all files found here in prod
STATICFILES_DIRS = [
    f"/personal_assistant_frontend_int/build" 
]

TEMPLATES[0]['DIRS'] = [STATIC_ROOT]

SECURE_CROSS_ORIGIN_OPENER_POLICY=None


PLAID_API_ENVIRONMENT_CONFIGURATION = configuration = Configuration(
        host=Environment.Sandbox,
            api_key={
                'clientId': PLAID_CLIENT_ID,
                'secret': PLAID_SECRET,
                'plaidVersion': '2020-09-14'
            }
        )