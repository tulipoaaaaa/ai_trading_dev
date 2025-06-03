from PyQt6.QtCore import pyqtSignal
from ..base_wrapper import BaseWrapper, CollectorWrapperMixin
from shared_tools.collectors.enhanced_scidb_collector import EnhancedSciDBCollector

class SciDBWrapper(BaseWrapper, CollectorWrapperMixin):
    """UI wrapper for Enhanced SciDB Collector"""
    
    papers_found = pyqtSignal(int)  # Number of papers found
    
    def __init__(self, config):
        super().__init__(config)
        self.collector = None
        
    def _create_target_object(self):
        """Create Enhanced SciDB collector instance"""
        if not self.collector:
            self.collector = EnhancedSciDBCollector(self.config)
        return self.collector
        
    def _get_operation_type(self):
        return "collect"