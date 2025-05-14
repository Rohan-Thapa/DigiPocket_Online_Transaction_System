import logging
from datetime import datetime
from fastapi import HTTPException
from repositories.transaction_repo import TransactionRepository
from models.transaction import TransactionCreate, TransactionOut
from services.user_service import can_spend, update_daily_spent
from repositories.user_repo import UserRepository
from repositories.merchant_repo import MerchantRepository
from core.config import settings
from models.user import UserInDB

# configure logger using config.log_file
logger = logging.getLogger("transaction_logger")
logger.setLevel(logging.INFO)
handler = logging.FileHandler(settings.log_file)
formatter = logging.Formatter("%(asctime)s - %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)

# repositories
transaction_repo = TransactionRepository()
user_repo = UserRepository()
merchant_repo = MerchantRepository()

async def transfer(sender_email: str, data: TransactionCreate) -> TransactionOut:
    # Fetch and validate sender
    sender_dict = await user_repo.get_by_email(sender_email)
    if not sender_dict:
        raise HTTPException(status_code=404, detail="Sender not found")
    # Convert ObjectId to string for Pydantic
    sender_dict['_id'] = str(sender_dict['_id'])
    sender = UserInDB(**sender_dict)

    # Check daily limit
    if not await can_spend(sender, data.amount):
        raise HTTPException(status_code=400, detail="Daily limit exceeded")

    # Debit sender
    sender.balance -= data.amount
    await user_repo.update(sender.id, {'balance': sender.balance})
    await update_daily_spent(sender, data.amount)

    # Credit recipient
    if data.recipient_type == 'user':
        rdict = await user_repo.get(data.recipient_id)
        if not rdict:
            raise HTTPException(status_code=404, detail="Recipient user not found")
        rdict['_id'] = str(rdict['_id'])
        ruser = UserInDB(**rdict)
        ruser.balance += data.amount
        await user_repo.update(ruser.id, {'balance': ruser.balance})
    else:
        m = await merchant_repo.get(data.recipient_id)
        if not m:
            raise HTTPException(status_code=404, detail="Merchant not found")
        m['balance'] += data.amount
        await merchant_repo.update(data.recipient_id, {'balance': m['balance']})

    # Create transaction record
    tx_data = data.dict()
    tx_data.update({
        'sender_id': sender.id,
        'status': 'completed',
        'timestamp': datetime.utcnow()
    })
    record = await transaction_repo.create(tx_data)
    if not record or record.get('_id') is None:
        raise HTTPException(status_code=500, detail="Failed to create transaction")

    # Prepare output and log
    tx_id = str(record['_id'])
    logger.info(f"TX {tx_id} | {sender.id}->{data.recipient_type}:{data.recipient_id} | {data.amount} | {data.description}")

    out = {
        '_id': tx_id,
        'sender_id': record['sender_id'],
        'recipient_type': record['recipient_type'],
        'recipient_id': record['recipient_id'],
        'amount': record['amount'],
        'description': record.get('description'),
        'status': record['status'],
        'timestamp': record['timestamp']
    }
    return TransactionOut(**out)