import pytest
from app.services.security_service import SecurityService

def test_security_validation_safe():
    service = SecurityService()
    assert service.validate_sql("SELECT * FROM users") == True
    assert service.validate_sql("SELECT count(*) FROM orders WHERE id > 5") == True

def test_security_validation_unsafe():
    service = SecurityService()
    with pytest.raises(ValueError, match="Destructive command detected"):
        service.validate_sql("DROP TABLE users")
    
    with pytest.raises(ValueError, match="Destructive command detected"):
        service.validate_sql("DELETE FROM users")
        
    with pytest.raises(ValueError, match="Destructive command detected"):
        service.validate_sql("UPDATE users SET name='hacked'")
