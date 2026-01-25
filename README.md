# AI Campaign Back-end

Instruções rápidas para rodar o projeto localmente (Windows).

1) Crie e ative um ambiente virtual (recomendado):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1  # ou Activate.bat no cmd
```

2) Instale dependências:

```powershell
pip install -r requirements.txt
```

3) Rodar a API FastAPI (endpoints em `main.py`):

```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Obs: Por padrão o projeto usa SQLite local (`./test.db`) se a variável de ambiente `DATABASE_URL` não estiver definida. Para usar PostgreSQL, exporte uma URL no formato:

```
postgresql://USER:PASSWORD@HOST:PORT/DBNAME
```

4) Rodar o webhook (arquivo `server.py`):

```powershell
python server.py
```

5) Endpoints úteis:
- `GET /campanhas/` — lista campanhas
- `POST /campanhas/` — cria campanha
- `GET /campanhas/{id}` — obtém campanha
- `DELETE /campanhas/{id}` — deleta campanha
