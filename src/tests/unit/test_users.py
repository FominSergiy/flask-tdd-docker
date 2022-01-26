import json

def test_add_user(test_app, test_database):
    client = test_app.test_client()
    username, email = 'sergey', 'sergiy.awesome@gmail.com'

    resp = client.post(
        '/users',
        data=json.dumps({
            'username' : username,
            'email' : email
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 201
    assert f'{email} was added!' in data['message']


def test_add_user_invalid_json(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_user_invalid_json_key(test_app, test_database):
    client = test_app.test_client()
    resp = client.post(
        '/users',
        data=json.dumps({'email':'sergiy.awesome@gmail.com'}),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert 'Input payload validation failed' in data['message']


def test_add_duplicate_user(test_app, test_database):
    client = test_app.test_client()
    username, email = 'sergey', 'sergiy.awesome@gmail.com'

    client.post(
        '/users',
        data=json.dumps({
            'username' : username,
            'email' : email
        }),
        content_type='application/json'
    )

    resp = client.post(
        '/users',
        data=json.dumps({
            'username' : username,
            'email' : email
        }),
        content_type='application/json'
    )
    data = json.loads(resp.data.decode())

    assert resp.status_code == 400
    assert 'Sorry. That email already exists.' in data['message']