from purse_backend.settings.settings import *



DEBUG = False

ALLOWED_HOSTS = ["*"]

CORS_ORIGIN_WHITELIST = [
    "https://app.ideajet.ai"
]


MEDIA_ROOT = "/applications/purse_media/"
STATIC_ROOT = f"/applications/purse_backend/static/"

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

CELERY_BROKER_URL = "sqs://"
CELERY_TASK_DEFAULT_QUEUE = 'purse_prod'


CELERY_BROKER_TRANSPORT_OPTIONS = {
    'region': 'us-east-2',
    'is_secure': True,
    'predefined_queues': {
        'purse_prod': {
            'url': 'https://sqs.us-east-2.amazonaws.com/490305332793/purse_prod',
        },
    },
    'visibility_timeout': 3600,
    'polling_interval': 5.0,
}