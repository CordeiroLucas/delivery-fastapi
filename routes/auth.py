from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import get_session, Session
from main import bcrypt_context

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
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário já Cadastrado!")

    senha_critpografada = bcrypt_context.hash(senha)

    novo_usuario = Usuario(nome, email, senha_critpografada)
    session.add(novo_usuario)
    session.commit()

    return {"message":f"{nome}, {email}, {senha_critpografada} - Registrado com sucesso!"}

