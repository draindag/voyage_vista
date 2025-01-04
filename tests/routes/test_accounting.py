import pytest
from flask_jwt_extended import create_access_token, create_refresh_token

from webapp import db
from webapp.models.User import User


def test_anonymous_required_for_authenticated_user(auth_client, user):
    """Тест для декоратора anonymous_required: попытка доступа с токеном"""
    response = auth_client.post('/api/registration')

    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь уже авторизован"

def test_refresh_token(auth_client, user):
    """Тест для маршрута обновления токена"""
    refresh_token = create_refresh_token(identity=user.login)

    response = auth_client.post('/api/refresh', headers={'Authorization': f'Bearer {refresh_token}'})

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data


def test_check_token(auth_client, user):
    """Тест для маршрута проверки токена"""
    access_token = create_access_token(identity=user.login)

    response = auth_client.post('/api/check_token', headers={'Authorization': f'Bearer {access_token}'})

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Токен ещё жив"

def test_registration(client, valid_registration_data, user):
    """Тест для маршрута регистрации"""
    valid_registration_data['login'] = "difftestuser"
    valid_registration_data['email'] = "difftestuser@example.com"
    response = client.post('/api/registration', json=valid_registration_data)

    assert response.status_code == 201
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["message"] == "Пользователь успешно зарегистрирован!"


def test_registration_with_existing_email_login(client, user, valid_registration_data):
    """Тест для маршрута регистрации с уже зарегистрированным email"""
    response = client.post('/api/registration', json=valid_registration_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь с таким логином или email уже зарегистрирован!"


def test_login_auth_client(auth_client, valid_login_data):
    """Тест для маршрута регистрации с уже зарегестрированным пользователем"""
    response = auth_client.post('/api/login', json=valid_login_data)

    assert response.status_code == 403
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь уже авторизован"

def test_login(client, user, valid_login_data):
    """Тест для маршрута авторизации"""
    valid_login_data['email'] = user.email
    valid_login_data['password'] = "password123"
    response = client.post('/api/login', json=valid_login_data)

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "access_token" in data
    assert "refresh_token" in data

def test_login(client, user, valid_login_data):
    """Тест для маршрута авторизации"""

    response = client.post('/api/login', json=valid_login_data)

    assert response.status_code == 400
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неверная информация в полях авторизации"

def test_show_profile(auth_client, user):
    """Тест для маршрута профиля пользователя"""
    response = auth_client.get('/api/profile')

    assert response.status_code == 200
    data = response.get_json()
    assert data["success"] is True
    assert "user" in data
    assert data["user"]["login"] == user.login


def test_show_profile_user_not_found(client, app, db_session):
    """Тест для маршрута профиля пользователя, когда пользователь не найден"""
    with app.app_context():
        fake_login = "non_existent_user"
        token = create_access_token(identity=fake_login)

    response = client.get('/api/profile', headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь не найден"


def test_edit_email(client, auth_client, user):
    """Тест для маршрута изменения email пользователя"""

    new_email = "newemail@example.com"
    data = {
        "email": new_email,
        "password": "password123"
    }

    response = auth_client.put('/api/edit_email', json=data)

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Email успешно изменён!"

    updated_user = User.query.filter_by(login=user.login).first()
    assert updated_user.email == new_email

def test_edit_email_user_not_found(client, auth_client, app):
    """Тест для маршрута изменения email, когда пользователь не найден"""
    with app.app_context():
        fake_login = "non_existent_user"
        token = create_access_token(identity=fake_login)

    data = {
        "email": "newemail@example.com",
        "password": "password123"
    }

    response = client.put('/api/edit_email', json=data, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь не найден"

def test_edit_email_taken(client, auth_client, user, db_session):
    """Тест для маршрута изменения email, когда email уже зарегистрирован"""
    other_user = User(login="otheruser", email="otheruser@example.com", password="password123")
    other_user.set_password("password123")
    db.session.add(other_user)
    db.session.commit()

    data = {
        "email": other_user.email,
        "password": "password123"
    }

    response = auth_client.put('/api/edit_email', json=data)

    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Невозможно использовать данный email!"

def test_edit_email_wrong_password(client, auth_client, user):
    """Тест для маршрута изменения email с неверным паролем"""

    data = {
        "email": "newemail@example.com",
        "password": "wrongpassword"
    }

    response = auth_client.put('/api/edit_email', json=data)

    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неверный пароль!"

def test_edit_login(client, auth_client, user):
    """Тест для маршрута изменения логина пользователя"""
    new_login = "newlogin"
    data = {
        "new_login": new_login,
        "password": "password123"
    }

    response = auth_client.put('/api/edit_login', json=data)

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Логин успешно изменён!"

    updated_user = User.query.filter_by(login=new_login).first()
    assert updated_user is not None
    assert updated_user.login == new_login


def test_edit_login_user_not_found(client, auth_client, app):
    """Тест для маршрута изменения логина, когда пользователь не найден"""

    with app.app_context():
        fake_login = "non_existent_user"
        token = create_access_token(identity=fake_login)

    data = {
        "new_login": "newlogin",
        "password": "password123"
    }

    response = client.put('/api/edit_login', json=data, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь не найден"

def test_edit_login_wrong_password(client, auth_client, user):
    """Тест для маршрута изменения логина с неверным паролем"""

    data = {
        "new_login": "newlogin",
        "password": "wrongpassword"
    }

    response = client.put('/api/edit_login', json=data, headers={
        'Authorization': f'Bearer {auth_client.environ_base["HTTP_AUTHORIZATION"].split()[-1]}'
    })

    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неверный пароль!"

def test_edit_password(client, auth_client, user):
    """Тест для маршрута изменения пароля пользователя"""

    new_password = "newpassword123"
    data = {
        "old_password": "password123",
        "new_password": new_password
    }

    response = auth_client.put('/api/edit_password', json=data)

    assert response.status_code == 200

    data = response.get_json()
    assert data["success"] is True
    assert data["message"] == "Пароль успешно изменён!"

    updated_user = User.query.filter_by(login=user.login).first()
    assert updated_user.check_password(new_password)


def test_edit_password_user_not_found(client, auth_client, app):
    """Тест для маршрута изменения пароля, когда пользователь не найден"""

    with app.app_context():
        fake_login = "non_existent_user"
        token = create_access_token(identity=fake_login)

    data = {
        "old_password": "password123",
        "new_password": "newpassword123"
    }

    response = client.put('/api/edit_password', json=data, headers={
        'Authorization': f'Bearer {token}'
    })

    assert response.status_code == 401
    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пользователь не найден"

def test_edit_password_wrong_old_password(client, auth_client, user):
    """Тест для маршрута изменения пароля с неверным старым паролем"""

    data = {
        "old_password": "wrongpassword",
        "new_password": "newpassword123"
    }

    response = auth_client.put('/api/edit_password', json=data)

    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Неверный старый пароль!"

def test_edit_password_empty_new_password(client, auth_client, user):
    """Тест для маршрута изменения пароля с пустым новым паролем"""

    data = {
        "old_password": "password123",
        "new_password": ""
    }

    response = auth_client.put('/api/edit_password', json=data)

    assert response.status_code == 400

    data = response.get_json()
    assert data["success"] is False
    assert data["message"] == "Пароль не может быть пустым!"
