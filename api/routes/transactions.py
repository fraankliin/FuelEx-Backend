from fastapi import APIRouter
from api.repositories.transaction_repository import get_all_transactions

router = APIRouter()

@router.get("/transactions")
def transactions():

    data = get_all_transactions()

    total_litros = sum(
        t["litros_suministrados"] for t in data
    )

    return {
        "transactions": data,
        "stats": {
            "total": len(data),
            "total_litros": total_litros
        }
    }
