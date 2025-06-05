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
# from ..widgets.storage_usage import StorageUsageWidget

class DashboardTab(QWidget):
    """Dashboard Tab with overview of corpus and activities"""
    
    update_needed = pyqtSignal()
    
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
        """Initialize the user interface"""
        # Main layout
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Header
        header_label = QLabel("Corpus Overview Dashboard")
        header_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        main_layout.addWidget(header_label)
        
        # Create top widgets layout
        top_layout = QHBoxLayout()
        
        print("DEBUG: Creating CorpusStatistics...")
        self.corpus_stats_widget = CorpusStatistics(self.config)
        print("DEBUG: CorpusStatistics created.")
        top_layout.addWidget(self.corpus_stats_widget, 2)
        
        # Storage usage widget (removed, file not found)
        # self.storage_usage_widget = StorageUsageWidget(self.config)
        # top_layout.addWidget(self.storage_usage_widget, 1)
        
        main_layout.addLayout(top_layout)
        
        # Create middle layout for domain distribution
        middle_layout = QHBoxLayout()
        
        print("DEBUG: Creating DomainDistribution...")
        self.domain_distribution_widget = DomainDistribution(self.config)
        print("DEBUG: DomainDistribution created.")
        middle_layout.addWidget(self.domain_distribution_widget)
        
        main_layout.addLayout(middle_layout)
        
        # Create bottom layout for activity log
        bottom_layout = QVBoxLayout()
        
        # Activity log header
        activity_header = QLabel("Recent Activity")
        activity_header.setStyleSheet("font-size: 14px; font-weight: bold;")
        bottom_layout.addWidget(activity_header)
        
        print("DEBUG: Creating ActivityLog...")
        self.activity_log_widget = ActivityLog(self.config)
        print("DEBUG: ActivityLog created.")
        bottom_layout.addWidget(self.activity_log_widget)
        
        main_layout.addLayout(bottom_layout)
        
        # Connect signals
        self.update_needed.connect(self.on_update_needed)
    
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
            
        except Exception as e:
            self.logger.error(f"Error updating dashboard data: {e}")
    
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
