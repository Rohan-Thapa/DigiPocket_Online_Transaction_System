from .base import BaseRepository
from core.database import db
from bson import ObjectId

class MerchantRepository(BaseRepository):
    collection = db.get_collection("merchants")

    async def create(self, data: dict) -> dict:
        res = await self.collection.insert_one(data)
        return await self.get(str(res.inserted_id))

    async def get(self, id: str) -> dict | None:
        return await self.collection.find_one({"_id": ObjectId(id)})

    async def update(self, id: str, data: dict) -> dict | None:
        await self.collection.update_one({"_id": ObjectId(id)}, {"$set": data})
        return await self.get(id)

    async def list(self, skip: int = 0, limit: int = 100) -> list[dict]:
        return await self.collection.find().skip(skip).limit(limit).to_list(limit)
