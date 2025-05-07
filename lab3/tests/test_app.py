import pytest
from app import app, users
from flask_login import current_user

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    with app.test_client() as client:
        with app.app_context():
            yield client

def test_visit_counter(client):
    """Тест счётчика посещений"""
    # Первое посещение
    response = client.get('/')
    assert '1' in response.get_data(as_text=True)

    # Второе посещение
    response = client.get('/')
    assert '2' in response.get_data(as_text=True)

def test_login_page(client):
    """Тест страницы входа"""
    response = client.get('/login')
    assert response.status_code == 200
    assert 'Вход в систему' in response.get_data(as_text=True)

def test_successful_login(client):
    """Тест успешного входа"""
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    assert 'Вы успешно вошли в систему' in response.get_data(as_text=True)

def test_failed_login(client):
    """Тест неудачного входа"""
    response = client.post('/login', data={
        'username': 'user',
        'password': 'wrong'
    }, follow_redirects=True)
    assert 'Неверное имя пользователя или пароль' in response.get_data(as_text=True)

def test_secret_page_access(client):
    """Тест доступа к секретной странице"""
    # Попытка доступа без авторизации
    response = client.get('/secret', follow_redirects=True)
    assert 'Для доступа к этой странице необходимо войти в систему' in response.get_data(as_text=True)

    # Вход в систему
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })

    # Попытка доступа после авторизации
    response = client.get('/secret')
    assert 'Секретная страница' in response.get_data(as_text=True)

def test_remember_me(client):
    """Тест функционала 'Запомнить меня'"""
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty',
        'remember': 'on'
    })
    assert 'remember_token' in response.headers.get('Set-Cookie', '')

def test_logout(client):
    """Тест выхода из системы"""
    # Сначала входим
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })

    # Затем выходим
    response = client.get('/logout', follow_redirects=True)
    assert 'Вы вышли из системы' in response.get_data(as_text=True)

def test_navbar_links_authenticated(client):
    """Тест отображения ссылок в навбаре для авторизованного пользователя"""
    # Входим в систему
    client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    })

    response = client.get('/')
    assert 'Секретная страница' in response.get_data(as_text=True)
    assert 'Выйти' in response.get_data(as_text=True)
    assert 'Войти' not in response.get_data(as_text=True)

def test_navbar_links_unauthenticated(client):
    """Тест отображения ссылок в навбаре для неавторизованного пользователя"""
    response = client.get('/')
    assert 'Секретная страница' not in response.get_data(as_text=True)
    assert 'Выйти' not in response.get_data(as_text=True)
    assert 'Войти' in response.get_data(as_text=True)

def test_redirect_after_login(client):
    """Тест перенаправления после входа"""
    # Пытаемся получить доступ к секретной странице
    client.get('/secret')
    
    # Входим в систему
    response = client.post('/login', data={
        'username': 'user',
        'password': 'qwerty'
    }, follow_redirects=True)
    
    # Должны быть перенаправлены на секретную страницу
    assert 'Секретная страница' in response.get_data(as_text=True) 