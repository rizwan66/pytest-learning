# ADVANCED LEVEL — LESSON 11: Async Testing with pytest-asyncio
#
# KEY CONCEPTS:
#   - pytest-asyncio lets you write `async def test_...` functions
#   - asyncio_mode = "auto" in pytest.ini removes the need for @pytest.mark.asyncio
#   - Async fixtures work exactly like sync fixtures — just add `async def`
#   - Use asyncio.gather in tests to verify concurrent behavior
#
# SETUP: pip install pytest-asyncio
# RUN:   pytest advanced/11_async_testing/ -v

import asyncio
import pytest
from async_service import AsyncUserService, fetch_with_timeout, gather_users


# --- Async fixtures ---

@pytest.fixture
async def service():
    return AsyncUserService()


@pytest.fixture
async def service_with_users(service):
    await service.create_user("u1", "Alice")
    await service.create_user("u2", "Bob")
    await service.create_user("u3", "Carol")
    return service


# --- Basic async tests ---

async def test_create_user(service):
    user = await service.create_user("u1", "Alice")
    assert user["id"] == "u1"
    assert user["name"] == "Alice"
    assert user["active"] is True


async def test_get_user_returns_correct_data(service):
    await service.create_user("u1", "Alice")
    user = await service.get_user("u1")
    assert user is not None
    assert user["name"] == "Alice"


async def test_get_nonexistent_user_returns_none(service):
    user = await service.get_user("does-not-exist")
    assert user is None


async def test_duplicate_user_raises(service):
    await service.create_user("u1", "Alice")
    with pytest.raises(ValueError, match="already exists"):
        await service.create_user("u1", "Alice Again")


async def test_deactivate_user(service):
    await service.create_user("u1", "Alice")
    result = await service.deactivate_user("u1")
    assert result is True
    user = await service.get_user("u1")
    assert user["active"] is False


async def test_deactivate_nonexistent_returns_false(service):
    result = await service.deactivate_user("ghost")
    assert result is False


async def test_list_active_users(service_with_users):
    await service_with_users.deactivate_user("u2")
    active = await service_with_users.list_active_users()
    names = [u["name"] for u in active]
    assert "Alice" in names
    assert "Carol" in names
    assert "Bob" not in names


# --- Concurrent behavior ---

async def test_gather_users_concurrently(service_with_users):
    results = await gather_users(service_with_users, ["u1", "u2", "u3"])
    assert len(results) == 3


async def test_gather_skips_missing_users(service_with_users):
    results = await gather_users(service_with_users, ["u1", "ghost", "u3"])
    assert len(results) == 2  # ghost was skipped


async def test_concurrent_creates(service):
    # All three create operations run concurrently
    await asyncio.gather(
        service.create_user("a", "Alpha"),
        service.create_user("b", "Beta"),
        service.create_user("c", "Gamma"),
    )
    active = await service.list_active_users()
    assert len(active) == 3


# --- Timeouts ---

async def test_fetch_within_timeout(service):
    await service.create_user("u1", "Alice")
    # get_user is nearly instant — 1s timeout is plenty
    user = await fetch_with_timeout(service.get_user("u1"), timeout=1.0)
    assert user["name"] == "Alice"


async def test_fetch_timeout_raises():
    async def slow():
        await asyncio.sleep(10)
        return "done"

    with pytest.raises(asyncio.TimeoutError):
        await fetch_with_timeout(slow(), timeout=0.01)


# EXERCISE:
# 1. Write an async fixture with scope="module" — what changes?
# 2. Create an AsyncPostService that depends on AsyncUserService.
#    Write tests that create a post and verify the author exists.
# 3. Test that concurrent creates with the SAME id — one succeeds, one raises.
