Criar migrações com Alembic

```bash
alembic revision --autogenerate -m "Nome Migracao"
```

Aplicar migrações no Banco

```bash 
alembic upgrade head
```



Rodar Projeto


```bash
uv run uvicorn main:app --reload
```