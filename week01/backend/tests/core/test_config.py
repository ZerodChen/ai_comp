from app.core.config import Settings

def test_cors_origins_str():
    settings = Settings(BACKEND_CORS_ORIGINS="http://localhost,http://example.com")
    assert isinstance(settings.BACKEND_CORS_ORIGINS, list)
    assert len(settings.BACKEND_CORS_ORIGINS) == 2
    assert str(settings.BACKEND_CORS_ORIGINS[0]) == "http://localhost/"
    assert str(settings.BACKEND_CORS_ORIGINS[1]) == "http://example.com/"

def test_cors_origins_list():
    settings = Settings(BACKEND_CORS_ORIGINS=["http://localhost", "http://example.com"])
    assert len(settings.BACKEND_CORS_ORIGINS) == 2

def test_cors_origins_invalid():
    import pytest
    with pytest.raises(ValueError):
        Settings(BACKEND_CORS_ORIGINS=123)
