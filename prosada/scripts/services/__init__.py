"""
Services Layer

Derived computations, analysis, and health checks.
Services consume domain models and produce insights.
"""

# v2 services (implemented)
from .graph_composer import GraphComposer

# Legacy service (in-memory graph model)
from .timeline_service import TimelineService

# Planned legacy services (not yet implemented):
#   ValidationService      -> backend/services/validation.py
#   ThreadAnalysisService  -> backend/services/thread_analysis.py
#   ExportService          -> backend/services/export_service.py

__all__ = [
    "GraphComposer",
    "TimelineService",
]
