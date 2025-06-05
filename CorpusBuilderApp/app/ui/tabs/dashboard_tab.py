"""
Dashboard Tab for CryptoFinance Corpus Builder
"""

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QProgressBar, QFrame, QSplitter, QPushButton,
                            QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt, QTimer, Signal as pyqtSignal, Slot as pyqtSlot, QSize, QThread
from PySide6.QtGui import QColor, QIcon
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

import logging
from pathlib import Path
import time
from datetime import datetime, timedelta
import math
import json
import threading

# Import UI components
from app.ui.widgets.corpus_statistics import CorpusStatistics
from app.ui.widgets.activity_log import ActivityLog
from app.ui.widgets.domain_distribution import DomainDistribution
from app.ui.widgets.active_operations import ActiveOperations
from app.ui.widgets.recent_activity import RecentActivity
# from ..widgets.storage_usage import StorageUsageWidget

class DashboardTab(QWidget):
    """Dashboard Tab with overview of corpus and activities"""
    
    update_needed = pyqtSignal()
    view_all_activity_requested = pyqtSignal()  # Signal to request full activity tab
    
    def __init__(self, project_config, parent=None):
        print(f"DEBUG: DashboardTab received config type: {type(project_config)}")
        print(f"DEBUG: DashboardTab received config value: {project_config}")
        super().__init__(parent)
        self.config = project_config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # UI setup
        self.init_ui()
        
        # Setup periodic update timer
        self.setup_update_timer()
        
        # Initial data load
        self.load_data()
    
    def init_ui(self):
        """Initialize the user interface with professional 4-column layout"""
        # Main layout with improved spacing
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(20, 15, 20, 20)
        main_layout.setSpacing(15)
        
        # Header with better positioning
        header_label = QLabel("Corpus Overview Dashboard")
        header_label.setObjectName("dashboard-header")
        header_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        main_layout.addWidget(header_label)
        
        # Create 4-column layout using QSplitter for responsiveness
        dashboard_splitter = QSplitter(Qt.Orientation.Horizontal)
        dashboard_splitter.setObjectName("dashboard-splitter")
        dashboard_splitter.setChildrenCollapsible(False)  # Prevent columns from collapsing
        
        # Column 1: Corpus Statistics - Improved sizing
        print("DEBUG: Creating CorpusStatistics...")
        self.corpus_stats_widget = CorpusStatistics(self.config)
        self.corpus_stats_widget.setObjectName("card")
        self.corpus_stats_widget.setMinimumSize(300, 450)  # Increased height for better space usage
        print("DEBUG: CorpusStatistics created.")
        dashboard_splitter.addWidget(self.corpus_stats_widget)
        
        # Column 2: Domain Distribution Chart - Improved sizing  
        print("DEBUG: Creating DomainDistribution...")
        self.domain_distribution_widget = DomainDistribution(self.config)
        self.domain_distribution_widget.setObjectName("card")
        self.domain_distribution_widget.setMinimumSize(350, 450)  # Larger for better pie chart display
        print("DEBUG: DomainDistribution created.")
        dashboard_splitter.addWidget(self.domain_distribution_widget)
        
        # Column 3: Active Operations - Improved sizing
        print("DEBUG: Creating ActiveOperations...")
        self.active_operations_widget = ActiveOperations(self.config)
        self.active_operations_widget.setObjectName("card")
        self.active_operations_widget.setMinimumSize(300, 450)  # Increased height
        print("DEBUG: ActiveOperations created.")
        dashboard_splitter.addWidget(self.active_operations_widget)
        
        # Column 4: Recent Activity - Improved sizing
        print("DEBUG: Creating RecentActivity...")
        self.recent_activity_widget = RecentActivity(self.config)
        self.recent_activity_widget.setObjectName("card")
        self.recent_activity_widget.setMinimumSize(300, 450)  # Increased height
        print("DEBUG: RecentActivity created.")
        dashboard_splitter.addWidget(self.recent_activity_widget)
        
        # Set proportions optimized for content (domain chart gets more space)
        dashboard_splitter.setSizes([300, 350, 300, 300])
        
        # Add the splitter to main layout with stretch to use full space
        main_layout.addWidget(dashboard_splitter, 1)  # Stretch factor 1 to fill available space
        
        # Legacy activity log (moved to separate tab or accessible via "View All")
        # We can remove this or make it accessible through the compact recent activity widget
        print("DEBUG: Creating legacy ActivityLog for full view...")
        self.activity_log_widget = ActivityLog(self.config)
        print("DEBUG: Legacy ActivityLog created (hidden by default).")
        
        # Connect signals
        self.update_needed.connect(self.on_update_needed)
        
        # Connect recent activity signals
        self.recent_activity_widget.activity_clicked.connect(self.handle_activity_click)
        self.recent_activity_widget.view_all_requested.connect(self.handle_view_all_request)
    
    def setup_update_timer(self):
        """Setup timer for periodic updates"""
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.update_data)
        self.update_timer.start(30000)  # Update every 30 seconds
    
    def load_data(self):
        """Load initial data for dashboard"""
        try:
            # Load corpus statistics
            corpus_stats = self.get_corpus_statistics()
            self.corpus_stats_widget.update_statistics(corpus_stats)
            
            # Load storage usage
            storage_usage = self.get_storage_usage()
            # self.storage_usage_widget.update_storage_usage(storage_usage)
            
            # Load domain distribution
            domain_distribution = self.get_domain_distribution()
            self.domain_distribution_widget.update_distribution_data(domain_distribution)
            
            # Load activity log
            activity_log = self.get_activity_log()
            self.activity_log_widget.update_activity_log(activity_log)
            
            self.logger.info("Dashboard data loaded successfully")
            
        except Exception as e:
            self.logger.error(f"Error loading dashboard data: {e}")
    
    def update_data(self):
        """Update dashboard data"""
        # Emit signal to update data in the UI thread
        self.update_needed.emit()
    
    @pyqtSlot()
    def on_update_needed(self):
        """Handle update signal"""
        try:
            # Update corpus statistics
            corpus_stats = self.get_corpus_statistics()
            self.corpus_stats_widget.update_statistics(corpus_stats)
            
            # Update storage usage
            storage_usage = self.get_storage_usage()
            # self.storage_usage_widget.update_storage_usage(storage_usage)
            
            # Update domain distribution
            domain_distribution = self.get_domain_distribution()
            self.domain_distribution_widget.update_distribution_data(domain_distribution)
            
            # Update activity log
            activity_log = self.get_activity_log()
            self.activity_log_widget.update_activity_log(activity_log)
            
            # Note: Active Operations and Recent Activity have their own auto-refresh timers
            # so they don't need manual updates here
            
        except Exception as e:
            self.logger.error(f"Error updating dashboard data: {e}")
    
    def handle_activity_click(self, activity):
        """Handle when an activity item is clicked"""
        # This could show a detailed view or switch to the full activity log
        self.logger.info(f"Activity clicked: {activity.get('action', 'Unknown')}")
        # For now, just log it - could be extended to show details dialog
    
    def handle_view_all_request(self):
        """Handle when View All is requested from Recent Activity"""
        self.logger.info("View All activity requested from dashboard")
        self.view_all_activity_requested.emit()
    
    def get_corpus_statistics(self):
        """Get corpus statistics"""
        # In a production app, this would query the actual corpus
        # For now, we'll return mock data for demonstration
        return {
            "total_documents": 2570,
            "total_size_gb": 45.8,
            "processed_documents": 2234,
            "pending_processing": 336,
            "average_quality": 0.82,
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    def get_storage_usage(self):
        """Get storage usage statistics"""
        # In a production app, this would query the actual disk usage
        # For now, we'll return mock data for demonstration
        return {
            "total_space_gb": 100.0,
            "used_space_gb": 45.8,
            "free_space_gb": 54.2,
            "usage_by_type": {
                "PDF": 32.5,
                "HTML": 8.2,
                "Code": 3.6,
                "Other": 1.5
            }
        }
    
    def get_domain_distribution(self):
        """Get domain distribution statistics"""
        # In a production app, this would query the actual domain distribution
        # For now, we'll return mock data for demonstration
        return {
            "Crypto Derivatives": {"allocation": 0.20, "current": 0.18, "documents": 456, "quality": 0.85},
            "DeFi": {"allocation": 0.12, "current": 0.15, "documents": 289, "quality": 0.82},
            "High Frequency Trading": {"allocation": 0.15, "current": 0.13, "documents": 378, "quality": 0.88},
            "Market Microstructure": {"allocation": 0.15, "current": 0.16, "documents": 423, "quality": 0.79},
            "Portfolio Construction": {"allocation": 0.10, "current": 0.09, "documents": 234, "quality": 0.76},
            "Regulation & Compliance": {"allocation": 0.05, "current": 0.04, "documents": 145, "quality": 0.91},
            "Risk Management": {"allocation": 0.15, "current": 0.17, "documents": 467, "quality": 0.83},
            "Valuation Models": {"allocation": 0.08, "current": 0.08, "documents": 178, "quality": 0.77},
        }
    
    def get_activity_log(self):
        """Get recent activity log"""
        # In a production app, this would query the actual activity log
        # For now, we'll return mock data for demonstration
        
        # Get current time for more realistic timestamps
        now = datetime.now()
        
        return [
            {"time": (now - timedelta(minutes=2)).strftime("%H:%M"), 
             "action": "GitHub collection started", 
             "status": "running"},
            {"time": (now - timedelta(minutes=15)).strftime("%H:%M"), 
             "action": "PDF processing completed", 
             "status": "success", 
             "details": "45 files processed"},
            {"time": (now - timedelta(minutes=30)).strftime("%H:%M"), 
             "action": "arXiv collection completed", 
             "status": "success", 
             "details": "23 papers collected"},
            {"time": (now - timedelta(minutes=47)).strftime("%H:%M"), 
             "action": "ISDA collection completed", 
             "status": "success", 
             "details": "12 documents collected"},
            {"time": (now - timedelta(minutes=63)).strftime("%H:%M"), 
             "action": "Domain rebalancing started", 
             "status": "success",
             "details": "8 domains rebalanced"}
        ]
