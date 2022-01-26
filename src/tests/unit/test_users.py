import json

from src import db
from src.api.models import User

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

def test_single_user(test_app, test_database):
    user = User(username='jeffrey', email='jeffrey@awesomeme.com')
    db.session.add(user)
    db.session.commit()

    client = test_app.test_client()
    resp = client.get(f'/users/{user.id}')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 200
    assert 'jeffrey' in data['username']
    assert 'jeffrey@awesomeme.com' in data['email']

def test_single_user_incorrect_id(test_app, test_database):
    client = test_app.test_client()

    bad_id = 999
    resp = client.get(f'/users/{bad_id}')
    data = json.loads(resp.data.decode())

    assert resp.status_code == 404
    assert f'User {bad_id} does not exist' in data['message']
