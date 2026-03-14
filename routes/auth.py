from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
def get_orders():
    """
        Root Auth Route
    """
    return {"tobus":"eles", "autenticado":False}