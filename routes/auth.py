from fastapi import APIRouter, Depends
from models import Usuario
from dependencies import get_session, Session

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
def get_orders():
    """
        Root Auth Route
    """
    return {"tobus":"eles", "autenticado":False}

@auth_router.post("/criar_conta")
async def registrar_usuario(nome: str, email: str, senha: str, session: Session = Depends(get_session)):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if usuario:
        return {"message":"user already registered"}

    novo_usuario = Usuario(nome, email, senha)
    session.add(novo_usuario)
    session.commit()

    return {"message":f"{nome}, {email} - Registrado com sucesso!"}

