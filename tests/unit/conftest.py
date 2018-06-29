import pytest

@pytest.fixture()
def mocker(request, mocker):
    request.cls.mocker = mocker
    return mocker
