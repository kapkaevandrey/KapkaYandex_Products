
def test_register(user_client):
    response = user_client.post('/auth/register', json={
        'email': 'harry@potter.grf',
        'password': 'lumusMaximus',
    })
    assert response.status_code == 201, (
        'When registering a user, the status code 201 should be returned'
    )
    data = response.json()
    keys = sorted(['id', 'email', 'is_active', 'is_superuser', 'is_verified'])
    assert sorted(list(data.keys())) == keys, (
        f'When registering a user, the response must contain the keys `{keys}`.'
    )
    data.pop('id')
    assert data == {
        'email': 'harry@potter.com',
        'is_active': True,
        'is_superuser': False,
        'is_verified': False,
    }, ('When registering a user, the API response body '
        'differs from the expected one.')


def test_register_invalid_pass(user_client):
    response = user_client.post('/auth/register', json={
        'email': 'Volan@DeMort.slz',
        'password': '$',
    })
    assert response.status_code == 400, (
        'In case of incorrect user registration, the status code 400 should be returned.'
    )
    data = response.json()
    assert list(data.keys()) == ['detail'], (
        'In case of incorrect user registration, the `detail` key must be in the response.'
    )
