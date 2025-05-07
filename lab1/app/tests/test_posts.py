# -*- coding: utf-8 -*-
import pytest
from datetime import datetime
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_post_page_template(client):
    """Test that post page uses correct template"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'blog-post' in response.get_data(as_text=True)

def test_post_page_contains_title(client):
    """Test that post page contains post title"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Заголовок поста' in response.get_data(as_text=True)

def test_post_page_contains_author(client):
    """Test that post page contains author name"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Автор:' in response.get_data(as_text=True)

def test_post_page_contains_date(client):
    """Test that post page contains formatted date"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Дата публикации:' in response.get_data(as_text=True)

def test_post_page_contains_image(client):
    """Test that post page contains post image"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'img-fluid' in response.get_data(as_text=True)

def test_post_page_contains_text(client):
    """Test that post page contains post text"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'blog-post-content' in response.get_data(as_text=True)

def test_post_page_contains_comments_section(client):
    """Test that post page contains comments section"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Комментарии' in response.get_data(as_text=True)

def test_post_page_contains_comment_form(client):
    """Test that post page contains comment form"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'Оставьте комментарий' in response.get_data(as_text=True)
    assert 'textarea' in response.get_data(as_text=True)
    assert 'Отправить' in response.get_data(as_text=True)

def test_post_page_contains_comments(client):
    """Test that post page contains comments"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'card-title' in response.get_data(as_text=True)  # Comment author
    assert 'card-text' in response.get_data(as_text=True)   # Comment text

def test_post_page_contains_replies(client):
    """Test that post page contains comment replies"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'replies' in response.get_data(as_text=True)

def test_post_page_404(client):
    """Test that non-existent post returns 404"""
    response = client.get('/posts/999')
    assert response.status_code == 404

def test_post_page_negative_index(client):
    """Test that negative post index returns 404"""
    response = client.get('/posts/-1')
    assert response.status_code == 404

def test_post_page_invalid_index(client):
    """Test that invalid post index returns 404"""
    response = client.get('/posts/invalid')
    assert response.status_code == 404

def test_post_page_comment_form_method(client):
    """Test that comment form uses POST method"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'method="POST"' in response.get_data(as_text=True)

def test_post_page_comment_form_required(client):
    """Test that comment form textarea is required"""
    response = client.get('/posts/0')
    assert response.status_code == 200
    assert 'required' in response.get_data(as_text=True)

def test_posts_index(client):
    response = client.get("/posts")
    assert response.status_code == 200
    assert "Последние посты" in response.text

def test_posts_index_template(client, captured_templates, mocker, posts_list):
    with captured_templates as templates:
        mocker.patch(
            "app.posts_list",
            return_value=posts_list,
            autospec=True
        )
        
        _ = client.get('/posts')
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == 'posts.html'
        assert context['title'] == 'Посты'
        assert len(context['posts']) == 1
