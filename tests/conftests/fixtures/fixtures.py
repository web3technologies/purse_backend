import os
import pytest
from django.conf import settings

from django.core.management import call_command


@pytest.fixture(scope="session")
def django_db_setup(django_db_setup, django_db_blocker):

    ref_fixtures = sorted([
        os.path.join(settings.REF_FIXTURES_DIR, file)
        for file in os.listdir(settings.REF_FIXTURES_DIR)
    ])


    fixtures = sorted([
        os.path.join(settings.FIXTURES_DIRS, file)
        for file in os.listdir(settings.FIXTURES_DIRS)
    ])
    with django_db_blocker.unblock():
        call_command("loaddata", *ref_fixtures)
        call_command("loaddata", *fixtures)


