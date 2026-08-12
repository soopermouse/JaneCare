from fastapi import APIRouter, Depends
from pydantic import BaseModel
from ..auth import authenticate, create_token, current_principal, Principal
from ..store import event

router=APIRouter(prefix='/api/auth',tags=['authentication'])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post('/login')
def login(body:LoginRequest):
    record=authenticate(body.email,body.password)
    event('authentication','User authenticated',{'principal_id':record['id'],'role':record['role']})
    return {'access_token':create_token(record),'token_type':'bearer','expires_in':28800,
            'principal':Principal.from_record(record).public()}

@router.get('/me')
def me(p:Principal=Depends(current_principal)):
    return p.public()
