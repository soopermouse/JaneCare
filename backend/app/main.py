from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import auth, clients, dashboard, providers, government, janeos
from .store import event

@asynccontextmanager
async def lifespan(app: FastAPI):
    event('system','JaneCare started with scoped authentication and JaneOS service identity')
    yield

app=FastAPI(title='JaneCare',version='0.2.0',description='AI-assisted social-care coordination managed by JaneOS',lifespan=lifespan)
app.include_router(auth.router); app.include_router(clients.router); app.include_router(dashboard.router)
app.include_router(providers.router); app.include_router(government.router); app.include_router(janeos.router)

@app.get('/health')
def health(): return {'status':'healthy','application':'JaneCare','authentication':'enabled'}

frontend=Path(__file__).resolve().parents[2]/'frontend'
if frontend.exists(): app.mount('/',StaticFiles(directory=frontend,html=True),name='frontend')
