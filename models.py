from sqlalchemy import create_engine, Column, Integer, String, Boolean, ForeignKey, Float
from sqlalchemy.orm import declarative_base, DeclarativeBase

db = create_engine("sqlite:///banco.db")

Base: DeclarativeBase = declarative_base()

class Usuario(Base):
    __tablename__ = "usuarios"

    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    nome: str = Column("nome", String)
    email: str = Column("email", String, unique=True, nullable=False)
    senha: str = Column("senha", String)
    ativo: bool = Column("ativo", Boolean)
    admin: bool = Column("admin", Boolean)

    def __init__(self, nome, email, senha, ativo=True, admin=False):
        self.nome = nome
        self.email = email
        self.senha = senha
        self.ativo = ativo
        self.admin = admin

    def __repr__(self):
        return f"<Usuario: {self.email}>"
    

class Pedido(Base):
    __tablename__ = "pedidos"

    STATUS_PEDIDOS = (
        ("PENDENTE", "PENDENTE"),
        ("CANCELADO", "CANCELADO"),
        ("FINALIZADO", "FINALIZADO")
    )

    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    status: str = Column("status", String)
    usuario: Usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco: float = Column("preco", Float)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario
        self.preco = preco
        self.status = status

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id: int = Column("id", Integer, primary_key=True, autoincrement=True)
    quantidade: str = Column("quantidade", Integer)
    sabor: str = Column("sabor", String)
    tamanho: str = Column("tamanho", String)
    preco_unitario: str = Column("preco_unitario", String)
    pedido: str = Column("pedido", ForeignKey("pedidos.id"))

    
    def __init__(self, quantidade, sabor, tamanho, preco_unitario, pedido):
        self.quantidade = quantidade
        self.sabor = sabor
        self.tamanho = tamanho
        self.preco_unitario = preco_unitario
        self.pedido = pedido