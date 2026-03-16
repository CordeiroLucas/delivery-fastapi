<!-- 
Iniciar Pasta de Configuração Alembic

```bash
alembic init alembic
``` 
-->

Criar migrações com Alembic

```bash
alembic revision --autogenerate -m "Nome Migracao"
```

Aplicar migração no Banco

```bash 
alembic upgrade head
```

Rodar Projeto

```bash
uv run uvicorn main:app --reload
```