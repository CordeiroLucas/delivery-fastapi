from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime


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


class ItemPedidoSchema(BaseModel):
    quantidade: int
    sabor: str
    tamanho: str
    preco_unitario: float
    pedido: int

    model_config = ConfigDict(from_attributes=True)
