import pytest

pytestmark = pytest.mark.integration


@pytest.mark.skip(reason="Requires live database — run: pytest -m integration")
@pytest.mark.asyncio
async def test_entry_repository_roundtrip():
  pass
