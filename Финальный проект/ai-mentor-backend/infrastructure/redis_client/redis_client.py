import redis.asyncio as aioredis
from redis.connection import ConnectionPool
from typing import Any
import json
import asyncio

from internal import interface


class RedisClient(interface.IRedis):
    def __init__(
            self,
            host: str,
            port: int,
            db: int,
            password: str,
            max_connections: int = 20,
            socket_connect_timeout: int = 5,
            socket_timeout: int = 5,
            decode_responses: bool = True,
            retry_on_timeout: bool = True,
            health_check_interval: int = 30
    ):
        self.pool = ConnectionPool(
            host=host,
            port=port,
            db=db,
            password=password,
            max_connections=max_connections,
            socket_connect_timeout=socket_connect_timeout,
            socket_timeout=socket_timeout,
            decode_responses=decode_responses,
            retry_on_timeout=retry_on_timeout,
            health_check_interval=health_check_interval
        )

        self.async_pool = None
        self.async_client = None

    async def set(self, key: str, value: Any, ttl: int = None) -> bool:
        try:
            client = await self.get_async_client()
            serialized_value = self._serialize_value(value)
            if ttl:
                return await client.setex(key, ttl, serialized_value)
            return await client.set(key, serialized_value)
        except Exception as e:
            raise e

    async def get(self, key: str, default: Any = None) -> Any:
        try:
            client = await self.get_async_client()
            value = await client.get(key)
            if value is None:
                return default
            return self._deserialize_value(value)
        except Exception as e:
            return default

    async def get_async_client(self) -> aioredis.Redis:
        if self.async_client is None:
            self.async_pool = aioredis.ConnectionPool.from_url(
                f"redis://:{self.pool.connection_kwargs.get('password')}@{self.pool.connection_kwargs['host']}:{self.pool.connection_kwargs['port']}/{self.pool.connection_kwargs['db']}",
                max_connections=self.pool.max_connections,
                decode_responses=True
            )
            self.async_client = aioredis.Redis(connection_pool=self.async_pool)
        return self.async_client

    def _serialize_value(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        return json.dumps(value, default=str, ensure_ascii=False)

    def _deserialize_value(self, value: str) -> Any:
        if not isinstance(value, str):
            return value
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value

    def close(self):
        try:
            if self.async_client:
                asyncio.create_task(self.async_client.aclose())
            if self.async_pool:
                asyncio.create_task(self.async_pool.aclose())
            self.pool.disconnect()
        except Exception as e:
            pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
