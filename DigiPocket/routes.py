from fastapi import APIRouter, HTTPException, Depends
from models.user import UserCreate, UserOut, UserInDB, LoginRequest
from models.merchant import MerchantCreate, MerchantOut
from models.transaction import TransactionCreate, TransactionOut
from services.user_service import register_user, load_balance, check_user_balance
from services.merchant_service import create_merchant, check_merchant_balance
from services.transaction_service import transfer
from core.security import authenticate_user, create_access_token, get_current_user

router = APIRouter()

@router.post("/users", response_model=UserOut)
async def api_register_user(payload: UserCreate):
    return await register_user(payload)

@router.post("/login")
async def api_login(credentials: LoginRequest):
    user = await authenticate_user(credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token = create_access_token(subject=user.email)
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/load", response_model=UserOut)
async def api_load_balance(amount: float, current: UserInDB = Depends(get_current_user)):
    return await load_balance(current, amount)

@router.get("/users/balance", response_model=UserOut)
async def api_user_balance(current: UserInDB = Depends(get_current_user)):
    return await check_user_balance(current)

@router.post("/users/transfer", response_model=TransactionOut)
async def api_transfer(payload: TransactionCreate, current: UserInDB = Depends(get_current_user)):
    return await transfer(current.email, payload)

@router.post("/merchants", response_model=MerchantOut)
async def api_create_merchant(payload: MerchantCreate, current: UserInDB = Depends(get_current_user)):
    return await create_merchant(payload)

@router.get("/merchants/{mid}/balance", response_model=MerchantOut)
async def api_merchant_balance(mid: str, current: UserInDB = Depends(get_current_user)):
    return await check_merchant_balance(mid)