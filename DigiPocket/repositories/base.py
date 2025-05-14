from abc import ABC, abstractmethod

class BaseRepository(ABC):
    @abstractmethod
    async def create(self, data: dict) -> dict:
        ...

    @abstractmethod
    async def get(self, id: str) -> dict | None:
        ...

    @abstractmethod
    async def list(self, skip: int = 0, limit: int = 100) -> list[dict]:
        ...
