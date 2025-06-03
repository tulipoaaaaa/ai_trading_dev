"""
Dashboard Tab for CryptoFinance Corpus Builder
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, 
                            QLabel, QProgressBar, QFrame, QSplitter, QPushButton,
                            QScrollArea, QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, pyqtSlot, QSize, QThread
from PyQt6.QtGui import QColor, QIcon
from PyQt6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis

import logging
from pathlib import Path
import time
from datetime import datetime, timedelta
import math
import json
import threading

# Import UI components
from ..widgets.corpus_statistics import CorpusStatisticsWidget
from ..widgets.activity_log import ActivityLogWidget
from ..widgets.domain_distribution import DomainDistributionWidget
from ..widgets.storage_usage import StorageUsageWidget

class DashboardTab(QWidget):
    """Dashboard Tab with overview of corpus and activities"""
    
    update_needed = pyqtSignal()
    
    def __init__(self, config):
        super().__init__()
        self.config = config
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
        
        # Corpus statistics widget
        self.corpus_stats_widget = CorpusStatisticsWidget(self.config)
        top_layout.addWidget(self.corpus_stats_widget, 2)
        
        # Storage usage widget
        self.storage_usage_widget = StorageUsageWidget(self.config)
        top_layout.addWidget(self.storage_usage_widget, 1)
        
        main_layout.addLayout(top_layout)
        
        # Create middle layout for domain distribution
        middle_layout = QHBoxLayout()
        
        # Domain distribution widget
        self.domain_distribution_widget = DomainDistributionWidget(self.config)
        middle_layout.addWidget(self.domain_distribution_widget)
        
        main_layout.addLayout(middle_layout)
        
        # Create bottom layout for activity log
        bottom_layout = QVBoxLayout()
        
        # Activity log header
        activity_header = QLabel("Recent Activity")
        activity_header.setStyleSheet("font-size: 14px; font-weight: bold;")
        bottom_layout.addWidget(activity_header)
        
        # Activity log widget
        self.activity_log_widget = ActivityLogWidget(self.config)
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
            self.storage_usage_widget.update_storage_usage(storage_usage)
            
            # Load domain distribution
            domain_distribution = self.get_domain_distribution()
            self.domain_distribution_widget.update_distribution(domain_distribution)
            
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
            self.storage_usage_widget.update_storage_usage(storage_usage)
            
            # Update domain distribution
            domain_distribution = self.get_domain_distribution()
            self.domain_distribution_widget.update_distribution(domain_distribution)
            
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
        return [
            {"name": "Crypto Derivatives", "allocation": 0.20, "current": 0.18, "documents": 456, "quality": 0.85},
            {"name": "DeFi", "allocation": 0.12, "current": 0.15, "documents": 289, "quality": 0.82},
            {"name": "High Frequency Trading", "allocation": 0.15, "current": 0.13, "documents": 378, "quality": 0.88},
            {"name": "Market Microstructure", "allocation": 0.15, "current": 0.16, "documents": 423, "quality": 0.79},
            {"name": "Portfolio Construction", "allocation": 0.10, "current": 0.09, "documents": 234, "quality": 0.76},
            {"name": "Regulation & Compliance", "allocation": 0.05, "current": 0.04, "documents": 145, "quality": 0.91},
            {"name": "Risk Management", "allocation": 0.15, "current": 0.17, "documents": 467, "quality": 0.83},
            {"name": "Valuation Models", "allocation": 0.08, "current": 0.08, "documents": 178, "quality": 0.77}
        ]
    
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
```