from models import db, Usuario
from sqlalchemy.orm import sessionmaker, Session
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM


def pegar_sessao():
    """
    Get a db session and returns it
    """
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session  ## Yield sends a return with that result without exiting the function
    finally:
        session.close()


def verificar_token(token, session: Session = Depends(pegar_sessao)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_usuario = dic_info.get("sub", 0)

    except JWTError:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Acesso Negado, Token Expirado ou Inválido",
        )

    usuario = session.query(Usuario).filter(Usuario.id == id_usuario).first()
    if not usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="Acesso Inválido")

    return usuario
