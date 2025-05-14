from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

class _DatabaseClient:
    _client: AsyncIOMotorClient | None = None

    @classmethod
    def get_client(cls) -> AsyncIOMotorClient:
        if cls._client is None:
            cls._client = AsyncIOMotorClient(settings.mongodb_uri)
        return cls._client

    @classmethod
    def get_db(cls):
        return cls.get_client()[settings.mongodb_db]

db = _DatabaseClient.get_db()