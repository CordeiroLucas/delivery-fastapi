from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PedidoSchema
from dependencies import Session, pegar_sessao, verificar_token
from models import Pedido, Usuario

order_router = APIRouter(prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)])


@order_router.get("/")
async def pedidos(
    session: Session = Depends(pegar_sessao), 
    usuario: Usuario = Depends(verificar_token)
):
    """
    Orders Route
    """
    if not usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Access Denied")

    orders = session.query(Pedido).filter(Pedido.usuario == usuario.id).all()

    return {"detail": "OK", "length": len(orders), "data": orders}


@order_router.post("/pedido")
async def criar_pedido(
    # pedido_schema: PedidoSchema, 
    session: Session = Depends(pegar_sessao),
    usuario: Usuario  = Depends(verificar_token)
):

    if not usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Access Denied")

    novo_pedido = Pedido(usuario=usuario.id)

    session.add(novo_pedido)
    session.commit()
    return {"mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id} | Status: {novo_pedido.status}"}
