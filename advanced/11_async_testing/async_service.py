import asyncio
from typing import Optional


class AsyncUserService:
    def __init__(self):
        self._store: dict = {}

    async def create_user(self, user_id: str, name: str) -> dict:
        await asyncio.sleep(0)  # simulate I/O
        if user_id in self._store:
            raise ValueError(f"User {user_id!r} already exists")
        user = {"id": user_id, "name": name, "active": True}
        self._store[user_id] = user
        return user

    async def get_user(self, user_id: str) -> Optional[dict]:
        await asyncio.sleep(0)
        return self._store.get(user_id)

    async def deactivate_user(self, user_id: str) -> bool:
        await asyncio.sleep(0)
        if user_id not in self._store:
            return False
        self._store[user_id]["active"] = False
        return True

    async def list_active_users(self) -> list:
        await asyncio.sleep(0)
        return [u for u in self._store.values() if u["active"]]


async def fetch_with_timeout(coro, timeout: float):
    """Runs a coroutine with a timeout; raises asyncio.TimeoutError on expiry."""
    return await asyncio.wait_for(coro, timeout=timeout)


async def gather_users(service: AsyncUserService, user_ids: list) -> list:
    """Fetches multiple users concurrently."""
    tasks = [service.get_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return [r for r in results if r is not None]
