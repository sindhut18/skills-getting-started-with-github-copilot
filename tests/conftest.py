from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module

_ORIGINAL_ACTIVITIES = deepcopy(app_module.activities)


def _restore_activities() -> None:
    app_module.activities.clear()
    app_module.activities.update(deepcopy(_ORIGINAL_ACTIVITIES))


@pytest.fixture(autouse=True)
def reset_activities_state():
    _restore_activities()
    yield
    _restore_activities()


@pytest.fixture
def client() -> TestClient:
    return TestClient(app_module.app)


@pytest.fixture
def signup_email() -> str:
    return "newstudent@mergington.edu"
