from fastapi.testclient import TestClient
from backend.app.main import app

c=TestClient(app)

def login(email,password):
    r=c.post('/api/auth/login',json={'email':email,'password':password}); assert r.status_code==200
    return {'Authorization':'Bearer '+r.json()['access_token']}

def test_unauthenticated_case_access_blocked():
    assert c.get('/api/cases').status_code==401

def test_client_can_only_use_client_portal():
    h=login('client@janecare.local','ChangeMe!Client1')
    assert c.get('/api/client/dashboard',headers=h).status_code==200
    assert c.get('/api/cases',headers=h).status_code==403
    assert c.get('/api/providers/dashboard',headers=h).status_code==403

def test_provider_is_scoped_to_organization():
    h=login('provider@janecare.local','ChangeMe!Provider1')
    r=c.get('/api/providers/dashboard',headers=h); assert r.status_code==200
    assert all(x['provider']=='Housing Support' for x in r.json()['referrals'])

def test_government_cannot_browse_cases_and_is_jurisdiction_scoped():
    h=login('government@janecare.local','ChangeMe!Government1')
    assert c.get('/api/cases',headers=h).status_code==403
    assert c.post('/api/government/reports/prepare',headers=h,json={'period':'2026-08','jurisdiction':'NL','standard':'generic'}).status_code==200
    assert c.post('/api/government/reports/prepare',headers=h,json={'period':'2026-08','jurisdiction':'BE','standard':'generic'}).status_code==403

def test_janeos_requires_separate_service_identity():
    assert c.get('/api/janeos/state').status_code==401
    assert c.get('/api/janeos/state',headers={'X-JaneOS-Key':'change-me-before-production'}).status_code==200
