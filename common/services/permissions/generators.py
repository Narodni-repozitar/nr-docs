"""Custom permission generators for handling NUSL harvested records."""

from invenio_search.engine import dsl
from oarepo_oaipmh_harvester.services.generators import IfHarvested

# The prefix for records that should be treated as "not harvested"
NUSL_PREFIX = "oai:invenio.nusl.cz:"


class NuslIfHarvested(IfHarvested):
    """
    Custom harvested check that treats records from NUSL as "not harvested".
    
    A record is considered "harvested" only if:
    1. It has oai.harvest.identifier, AND
    2. The identifier does NOT start with "oai:invenio.nusl.cz:"
    """
    
    def _condition(self, record, **context):
        """Check if the record is harvested (but not from NUSL)."""
        oai_section = record.get("oai", None)
        if not oai_section:
            return False
        harvest = oai_section.get("harvest", None)
        if not harvest:
            return False
        identifier = harvest.get("identifier")
        
        return bool(identifier) and not identifier.startswith(NUSL_PREFIX)
    
    def query_filter(self, **context):
        """Apply then or else filter for search queries."""
        q_has_identifier = dsl.Q("exists", field="oai.harvest.identifier")
        q_is_nusl = dsl.Q("prefix", **{"oai.harvest.identifier": NUSL_PREFIX})
        
        q_harvested = q_has_identifier & ~q_is_nusl
        
        if self.then_:
            then_query = self._make_query(self.then_, **context)
        else:
            then_query = dsl.Q("match_none")
        
        if self.else_:
            else_query = self._make_query(self.else_, **context)
        else:
            else_query = dsl.Q("match_none")
        
        return (q_harvested & then_query) | (~q_harvested & else_query)


class NuslIfNotHarvested(NuslIfHarvested):
    """Inverse of CustomIfHarvested - returns True when record is NOT harvested."""
    
    def _condition(self, record, **context):
        return not super()._condition(record, **context)