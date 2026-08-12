from .base import GovernmentAdapter
class GenericGovernmentAdapter(GovernmentAdapter):
    id='generic'
    def transform(self, canonical_report): return canonical_report
