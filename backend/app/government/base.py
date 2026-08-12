from abc import ABC, abstractmethod
from typing import Any

class GovernmentAdapter(ABC):
    id='generic'
    @abstractmethod
    def transform(self, canonical_report: dict[str, Any]) -> dict[str, Any]: ...
    def validate(self, payload: dict[str, Any]) -> list[str]:
        errors=[]
        if not payload.get('period'): errors.append('period is required')
        if not payload.get('case_count',0): errors.append('report contains no cases')
        return errors
    def submit(self, payload: dict[str, Any]) -> dict[str, Any]:
        # Network submission is intentionally not implemented in the generic adapter.
        return {"status":"prepared_for_external_transport","adapter":self.id,"payload":payload}
