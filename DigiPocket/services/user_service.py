from repositories.user_repo import UserRepository
from models.user import UserCreate, UserInDB, UserOut
from core.security import hash_password
from core.config import settings

user_repo = UserRepository()

async def register_user(data: UserCreate) -> UserOut:
    hashed = hash_password(data.password)
    kyc_status = True if data.tier == 'premium' else False
    user_dict = data.dict()
    user_dict.update({
        'hashed_password': hashed,
        'balance': 0.0,
        'daily_spent': 0.0,
        'kyc': kyc_status
    })
    created = await user_repo.create(user_dict)
    return UserOut(id=str(created['_id']), email=created['email'], tier=created['tier'], balance=created['balance'], kyc=created['kyc'])

async def load_balance(user: UserInDB, amount: float) -> UserOut:
    user.balance += amount
    updated = await user_repo.update(user.id, {'balance': user.balance})
    return UserOut(id=str(updated['_id']), email=updated['email'], tier=updated['tier'], balance=updated['balance'], kyc=updated['kyc'])

async def check_user_balance(user: UserInDB) -> UserOut:
    return UserOut(id=user.id, email=user.email, tier=user.tier, balance=user.balance, kyc=user.kyc)

async def update_daily_spent(user: UserInDB, amount: float):
    user.daily_spent += amount
    await user_repo.update(user.id, {'daily_spent': user.daily_spent})

async def can_spend(user: UserInDB, amount: float) -> bool:
    limit = settings.basic_daily_limit if user.tier == 'basic' else settings.premium_daily_limit
    return (user.daily_spent + amount) <= limit
