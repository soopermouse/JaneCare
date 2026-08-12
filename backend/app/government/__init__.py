from .generic import GenericGovernmentAdapter
from .nl import NetherlandsGovernmentAdapter

def get_adapter(jurisdiction:str, standard:str):
    if jurisdiction.upper()=='NL': return NetherlandsGovernmentAdapter()
    return GenericGovernmentAdapter()
