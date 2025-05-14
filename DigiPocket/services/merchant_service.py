from repositories.merchant_repo import MerchantRepository
from models.merchant import MerchantCreate, MerchantOut

merchant_repo = MerchantRepository()

async def create_merchant(data: MerchantCreate) -> MerchantOut:
    m = await merchant_repo.create({**data.dict(), 'balance': 0.0})
    return MerchantOut(id=str(m['_id']), name=m['name'], description=m['description'], balance=m['balance'])

async def check_merchant_balance(mid: str) -> MerchantOut:
    m = await merchant_repo.get(mid)
    return MerchantOut(id=str(m['_id']), name=m['name'], description=m['description'], balance=m['balance'])
