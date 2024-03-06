import pytest
from django.test import Client
from django.urls import reverse

from django_deep_link.models import App, Visit


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def app():
    return App.objects.create(code="5314fe4e-facf-49a8-9cda-c76ac0db673e")


@pytest.mark.django_db
def test_app_download_view(client, app):
    url = reverse("django_deep_link:deep-link", kwargs={"code": app.code})
    response = client.get(url)
    assert response.status_code == 200

    assert Visit.objects.filter(deep_link=app).exists()

    visit = Visit.objects.get(deep_link=app)
    assert visit.ip_address is not None
    assert visit.ua_data is not None
    assert visit.ip_data is not None
    assert visit.query_data is not None
