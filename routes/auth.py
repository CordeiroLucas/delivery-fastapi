from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import pegar_sessao, Session
from main import bcrypt_context
from schemas import UsuarioSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def usuarios():
    """
        Root Auth Route
    """
    return {"rota":"auth", "autenticado":False}

@auth_router.post("/criar_conta")
async def registrar_usuario(usuario_schema: UsuarioSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == usuario_schema.email).first()

    if usuario:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Usuário já Cadastrado!")

    senha_critpografada = bcrypt_context.hash(usuario_schema.senha)

    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_critpografada, usuario_schema.ativo, usuario_schema.admin)
    session.add(novo_usuario)
    session.commit()

    return {"message":f"{usuario_schema.nome}, {usuario_schema.email}, {senha_critpografada} - Registrado com sucesso!"}

