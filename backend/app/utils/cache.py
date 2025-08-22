import time
from typing import Any, Optional


class TTLCache:
	def __init__(self, ttl_seconds: int = 300, max_items: int = 1000) -> None:
		self.ttl_seconds = ttl_seconds
		self.max_items = max_items
		self._store = {}

	def get(self, key: str) -> Optional[Any]:
		entry = self._store.get(key)
		if not entry:
			return None
		value, expires_at = entry
		if time.time() > expires_at:
			self._store.pop(key, None)
			return None
		return value

	def set(self, key: str, value: Any) -> None:
		if len(self._store) >= self.max_items:
			# drop oldest
			oldest_key = next(iter(self._store.keys()))
			self._store.pop(oldest_key, None)
		expires_at = time.time() + self.ttl_seconds
		self._store[key] = (value, expires_at)


result_cache = TTLCache(ttl_seconds=600, max_items=2000)