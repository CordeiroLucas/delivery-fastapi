from fastapi import APIRouter, Depends
from schemas import PedidoSchema
from dependencies import Session, pegar_sessao
from models import Pedido

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"])


@order_router.get("/")
async def pedidos():
    """
    Orders Route
    """
    return {"rota": "pedidos"}


@order_router.post("/pedido")
async def criar_pedido(
    pedido_schema: PedidoSchema, session: Session = Depends(pegar_sessao)
):
    novo_pedido = Pedido(usuario=pedido_schema.usuario)

    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id}"}
