from backend.app.janeos.adapter import JaneCareAdapter

def test_manifest_and_health():
    a=JaneCareAdapter()
    assert a.manifest()['id']=='janecare'
    assert a.health()['status']=='healthy'

def test_unknown_command_blocked():
    a=JaneCareAdapter()
    assert a.command('deny_eligibility',{})['status']=='blocked'
