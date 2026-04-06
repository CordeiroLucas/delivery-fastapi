from pydantic import BaseModel, ConfigDict
from typing import Optional

class UsuarioSchema(BaseModel):
    nome: str
    email: str 
    senha: str 
    ativo: Optional[bool]
    admin: Optional[bool]

    model_config = ConfigDict(from_attributes=True)

class PedidoSchema(BaseModel):
    usuario: int 

    model_config = ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email: str
    senha: str

    model_config = ConfigDict(from_attributes=True)
