from fastapi import APIRouter
from services.db_services import get_all_accesos

router = APIRouter(prefix="/accesos")

@router.get("/")
def get_accesos():
    data = get_all_accesos()
    return {"status": "ok", "data": data}
