import base64, hashlib, hmac, json, os, secrets, time
from dataclasses import dataclass
from fastapi import Depends, Header, HTTPException, status

SECRET = os.getenv('JANECARE_AUTH_SECRET', 'change-me-before-production')
TOKEN_TTL = int(os.getenv('JANECARE_TOKEN_TTL_SECONDS', '28800'))

# Demo identities. Replace with database/IdP-backed principals in production.
USERS = {
    'professional@janecare.local': {
        'id':'USR-PRO-1','email':'professional@janecare.local','name':'M. de Vries','role':'professional',
        'password':'ChangeMe!Professional1','case_ids':['JC-1024']
    },
    'provider@janecare.local': {
        'id':'USR-PRV-1','email':'provider@janecare.local','name':'Housing Support','role':'provider',
        'password':'ChangeMe!Provider1','provider_org':'Housing Support'
    },
    'client@janecare.local': {
        'id':'USR-CLI-1','email':'client@janecare.local','name':'Sarah M.','role':'client',
        'password':'ChangeMe!Client1','client_case_id':'JC-1024'
    },
    'government@janecare.local': {
        'id':'USR-GOV-1','email':'government@janecare.local','name':'Government Reporting User','role':'government',
        'password':'ChangeMe!Government1','jurisdictions':['NL']
    },
    'admin@janecare.local': {
        'id':'USR-ADM-1','email':'admin@janecare.local','name':'JaneCare Administrator','role':'admin',
        'password':'ChangeMe!Admin1'
    }
}

@dataclass
class Principal:
    id: str
    email: str
    name: str
    role: str
    case_ids: list[str] | None = None
    provider_org: str | None = None
    client_case_id: str | None = None
    jurisdictions: list[str] | None = None

    @classmethod
    def from_record(cls, r):
        return cls(**{k:r.get(k) for k in cls.__annotations__})

    def public(self):
        return {k:v for k,v in self.__dict__.items() if v is not None}


def _b64(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b'=').decode()

def _unb64(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + '=' * (-len(data) % 4))

def create_token(record: dict) -> str:
    now=int(time.time())
    payload={
        'sub':record['id'],'email':record['email'],'role':record['role'],
        'iat':now,'exp':now+TOKEN_TTL,'nonce':secrets.token_hex(8)
    }
    body=_b64(json.dumps(payload,separators=(',',':')).encode())
    sig=_b64(hmac.new(SECRET.encode(),body.encode(),hashlib.sha256).digest())
    return body+'.'+sig

def decode_token(token: str) -> dict:
    try:
        body,sig=token.split('.',1)
        expected=_b64(hmac.new(SECRET.encode(),body.encode(),hashlib.sha256).digest())
        if not hmac.compare_digest(sig,expected): raise ValueError('bad signature')
        payload=json.loads(_unb64(body))
        if int(payload['exp']) < int(time.time()): raise ValueError('expired')
        return payload
    except Exception:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Invalid or expired authentication token')

def authenticate(email: str, password: str):
    record=USERS.get(email.lower())
    if not record or not hmac.compare_digest(record['password'], password):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Invalid email or password')
    return record

def current_principal(authorization: str | None = Header(default=None)) -> Principal:
    if not authorization or not authorization.lower().startswith('bearer '):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Authentication required')
    payload=decode_token(authorization.split(' ',1)[1])
    record=next((u for u in USERS.values() if u['id']==payload['sub']),None)
    if not record: raise HTTPException(status.HTTP_401_UNAUTHORIZED,'Unknown account')
    return Principal.from_record(record)

def require_roles(*roles):
    def dependency(p: Principal=Depends(current_principal)):
        if p.role not in roles:
            raise HTTPException(status.HTTP_403_FORBIDDEN,'Your account is not authorized for this function')
        return p
    return dependency
