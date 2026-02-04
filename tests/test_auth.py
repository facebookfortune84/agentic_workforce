import pytest
import asyncio
from src.auth.gatekeeper import generate_key, validate_key

@pytest.mark.asyncio
async def test_key_lifecycle():
    key = await generate_key(user_id="TEST_USER", tier="PRO")
    assert key.startswith("rf_pro_")
    
    lic = await validate_key(key)
    assert lic is not None
    assert lic.user_id == "TEST_USER"
    print(f"✅ Security Lifecycle verified for key: {key[:15]}...")