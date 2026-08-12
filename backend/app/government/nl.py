from .base import GovernmentAdapter

class NetherlandsGovernmentAdapter(GovernmentAdapter):
    id='nl-placeholder'
    def transform(self, canonical_report):
        # Deliberately canonical/placeholder. A production iWmo/iJw/iPgb transport
        # must be implemented against the applicable, current official standard.
        return {**canonical_report,"jurisdiction":"NL","mapping_status":"adapter_placeholder_requires_certification"}
