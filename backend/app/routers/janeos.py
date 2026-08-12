import os, hmac
from fastapi import APIRouter, Header, HTTPException, Depends
from ..janeos import JaneCareAdapter
from ..schemas import CommandRequest
from ..store import EVENTS
router=APIRouter(prefix='/api/janeos',tags=['janeos-management'])
adapter=JaneCareAdapter()

def janeos_auth(x_janeos_key: str | None = Header(default=None)):
    expected=os.getenv('JANEOS_SERVICE_KEY','change-me-before-production')
    if not x_janeos_key or not hmac.compare_digest(x_janeos_key,expected): raise HTTPException(401,'JaneOS service authentication required')
    return True

@router.get('/manifest')
def manifest(_:bool=Depends(janeos_auth)): return adapter.manifest()
@router.get('/health')
def health(_:bool=Depends(janeos_auth)): return adapter.health()
@router.get('/state')
def state(_:bool=Depends(janeos_auth)): return adapter.state()
@router.get('/metrics')
def metrics(_:bool=Depends(janeos_auth)): return adapter.metrics()
@router.get('/events')
def events(_:bool=Depends(janeos_auth)): return EVENTS[:50]
@router.post('/commands')
def command(body:CommandRequest,_:bool=Depends(janeos_auth)): return adapter.command(body.command,body.args)
