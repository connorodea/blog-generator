import pytest
from src.blog_generator import setup_client, generate_blog_post
from openai import OpenAI
import os

def test_setup_client_no_api_key():
    """Test that setup_client raises error when no API key is set"""
    if 'OPENAI_API_KEY' in os.environ:
        del os.environ['OPENAI_API_KEY']
    with pytest.raises(ValueError):
        setup_client()

def test_setup_client_with_api_key():
    """Test that setup_client returns OpenAI client when API key is set"""
    os.environ['OPENAI_API_KEY'] = 'test_key'
    client = setup_client()
    assert isinstance(client, OpenAI)
