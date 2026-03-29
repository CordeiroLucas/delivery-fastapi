from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import pegar_sessao, Session
from main import bcrypt_context
from schemas import UsuarioSchema, LoginSchema

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(email):
    token = f"dAosjdaoiO9apkAOUNbuAjrNOisdo{email}"
    return token

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
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário já Cadastrado!")

    senha_critpografada = bcrypt_context.hash(usuario_schema.senha)

    novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_critpografada, usuario_schema.ativo, usuario_schema.admin)
    session.add(novo_usuario)
    session.commit()

    return {"message":f"{usuario_schema.nome}, {usuario_schema.email}, {senha_critpografada} - Registrado com sucesso!"}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = session.query(Usuario).filter(Usuario.email == login_schema.email).first()

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario não encontrado")
    
    access_token = criar_token(usuario.id)

    return {
        "Access-Token" : access_token,
        "Token-Type" : "Bearer"
    }

    # headers = {
    #     "Access-Token" : f"Bearer {}"
    # }