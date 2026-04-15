from fastapi import APIRouter, Depends, HTTPException, status
from schemas import PedidoSchema
from dependencies import Session, pegar_sessao, verificar_token
from models import Pedido, Usuario

order_router = APIRouter(
    prefix="/pedidos", tags=["pedidos"], dependencies=[Depends(verificar_token)]
)


@order_router.get("/")
async def raiz():
    return {"detail": "rota pedidos"}


@order_router.post("/pedido")
async def criar_pedido(
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    novo_pedido = Pedido(usuario=usuario.id)

    session.add(novo_pedido)
    session.commit()
    return {
        "mensagem": f"Pedido criado com sucesso! ID do pedido: {novo_pedido.id} | Status: {novo_pedido.status}"
    }


@order_router.post("/pedido/cancelar/{id_pedido}")
async def criar_pedido(
    id_pedido: int,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    pedido_info: Pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()

    if not usuario.admin or usuario.id != pedido_info.usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Acesso Negado!")

    if pedido_info.status == "CANCELADO":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Pedido já Cancelado!")

    pedido_info.status = "CANCELADO"
    session.commit()

    return {
        "mensagem": f"Pedido cancelado com sucesso!",
        "pedido": f"{pedido_info.id} - {pedido_info.status}",
    }


@order_router.get("/listar")
async def pedidos(
    quantidade: int = 10,
    session: Session = Depends(pegar_sessao),
    usuario: Usuario = Depends(verificar_token),
):
    """
    Orders Route
    """
    if not usuario or not usuario.admin:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Acesso Negado!")

    if quantidade <= 0:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            detail="Quantidade Inválida! Deve ser um valor positivo maior que zero.",
        )

    orders = session.query(Pedido).filter(Pedido.usuario == usuario.id)[:quantidade]

    return {"detail": "OK", "length": len(orders), "pedidos": orders}
