from setuptools import setup, find_packages


install_requires = [
    "boto3 ~= 1.26.151",
    "botocore ~= 1.29.151",
    "celery ~= 5.2.7",
    "celery[sqs] ~= 5.2.3",
    "coinbase ~= 2.1.0",
    "django ~= 4.2",
    "django-cors-headers ~= 3.13.0",
    "django_celery_beat ~= 2.5.0",
    "django_celery_results ~= 2.4.0",
    "django-extensions ~= 3.2.1",
    "django-phonenumber-field ~= 7.0.1",
    "djangorestframework ~= 3.14.0",
    "djangorestframework-simplejwt ~= 5.2.1",
    "plaid-python ~= 9.9.0",
    "phonenumbers ~= 8.13.3",
    "psycopg2-binary ~= 2.9.3",
    "python-decouple ~= 3.6",
    "requests ~= 2.28.1",
    "twilio ~= 7.16.0"
]

tests_require = [
    "pytest",
    "pytest-django",
    "pytest-cov",
    "pytest-freezegun",
    "pytest-mock",
    "pytest-celery",
    "pytest-check",
    "moto[s3]"
]

setup(
    name="purse_backend",
    version="0.1.2",
    description="Purse Backend Application",
    author="Web3Technologies LLC",
    author_email="zach@web3technologies.io",
    install_requires=install_requires,
    include_package_data=True,
    packages=find_packages("purse_backend"),
    test_suite="tests",
    tests_require=tests_require,
    extras_require={
        "test": tests_require,
    },
    package_dir={"":"purse_backend"},
    )