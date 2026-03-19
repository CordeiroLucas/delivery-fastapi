from fastapi import APIRouter

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])

@order_router.get("/")
def get_orders():
    """
        Orders Route
    """
    return {"tobas":"ebas"}