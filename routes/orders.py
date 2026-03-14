from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"])

@order_router.get("/")
def get_orders():
    """
        Orders Route
    """
    return {"tobas":"ebas"}