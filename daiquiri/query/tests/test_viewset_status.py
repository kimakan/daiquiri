import pytest
from django.urls import reverse

users = (
    ('admin', 'admin'),
    ('user', 'user'),
    ('evil', 'evil'),
    ('anonymous', None),
)

status_map = {
    'list': {
        'admin': 200, 'user': 200, 'evil': 200, 'anonymous': 403
    }
}

urlnames = {
    'list': 'query:status-list'
}


@pytest.mark.parametrize('username,password', users)
def test_list(db, client, username, password):
    client.login(username=username, password=password)

    url = reverse(urlnames['list'])
    response = client.get(url)
    assert response.status_code == status_map['list'][username], response.json()

    if response.status_code == 200:
        assert len(response.json()) == 1
        assert response.json()[0].get('guest') is False
