import pytest
import asyncio
from src.system.arsenal.registry import ALL_TOOLS_LIST, execute_tool

@pytest.mark.asyncio
async def test_registry_populated():
    assert len(ALL_TOOLS_LIST) > 0
    print(f"✅ Registry contains {len(ALL_TOOLS_LIST)} tools.")

@pytest.mark.asyncio
async def test_file_tool_execution():
    # Test a non-destructive read
    result = await execute_tool("read_file", file_path="requirements.txt")
    assert "[ERROR]" not in result
    print("✅ Tool execution (read_file) verified.")