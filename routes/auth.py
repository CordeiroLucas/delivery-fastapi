from fastapi import APIRouter, Depends, HTTPException, status
from models import Usuario
from dependencies import pegar_sessao, Session, verificar_token
from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from schemas import UsuarioSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone

auth_router = APIRouter(prefix="/auth", tags=["auth"])

def criar_token(id_usuario:int, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {
        "sub": id_usuario,
        "exp": data_expiracao
    }

    jwt_codificado = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)

    return jwt_codificado

def autenticar_usuario(email, senha, session: Session):
    usuario = session.query(Usuario).filter(Usuario.email == email).first()

    if not usuario:
        return False
    
    elif not bcrypt_context.verify(senha, usuario.senha):
        return False

    return usuario

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

    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)

    if not usuario:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuario Não Encontrado ou Credenciais Incorreto!")
    
    access_token = criar_token(usuario.id)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))

    return {
        "access-token" : access_token,
        "refresh-token": refresh_token,
        "token-type" : "Bearer"
    }

@auth_router.get("/refresh")
async def use_refresh_token(usuario: Usuario = Depends(verificar_token)):

    access_token = criar_token(usuario.id)

    return {
        "access-token" : access_token,
        "token-type" : "Bearer"
    }
