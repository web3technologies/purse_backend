from purse_backend.settings.settings import *



DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = [
    "https://purse.health"
]


STATIC_ROOT = f"/personal_assistant_frontend_prod/src"   #collectstatic places all files found here in prod
STATICFILES_DIRS = [
    f"/personal_assistant_frontend_prod/build" 
]

TEMPLATES[0]['DIRS'] = [STATIC_ROOT]

SECURE_CROSS_ORIGIN_OPENER_POLICY=None

PLAID_API_ENVIRONMENT_CONFIGURATION = configuration = Configuration(
        host=Environment.Development,
            api_key={
                'clientId': PLAID_CLIENT_ID,
                'secret': PLAID_SECRET,
                'plaidVersion': '2020-09-14'
            }
        )