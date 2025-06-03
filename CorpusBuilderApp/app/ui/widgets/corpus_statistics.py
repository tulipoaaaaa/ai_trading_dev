"""
Corpus Statistics Widget for Dashboard
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                            QProgressBar, QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
import logging

class CorpusStatisticsWidget(QFrame):
    """Widget displaying corpus statistics"""
    
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # Set frame styling
        self.setFrameShape(QFrame.Shape.StyledPanel)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setStyleSheet("""
            QFrame {
                background-color: #ffffff;
                border-radius: 6px;
                border: 1px solid #e0e0e0;
            }
            QLabel.header {
                font-size: 14px;
                font-weight: bold;
                color: #404040;
            }
            QLabel.stat {
                font-size: 22px;
                font-weight: bold;
                color: #303030;
            }
            QLabel.desc {
                font-size: 12px;
                color: #606060;
            }
        """)
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Header
        header = QLabel("Corpus Statistics")
        header.setProperty("class", "header")
        layout.addWidget(header)
        
        # Statistics grid
        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        layout.addLayout(grid_layout)
        
        # Total documents
        grid_layout.addWidget(QLabel("Total Documents"), 0, 0)
        self.total_documents_label = QLabel("0")
        self.total_documents_label.setProperty("class", "stat")
        grid_layout.addWidget(self.total_documents_label, 1, 0)
        
        # Total size
        grid_layout.addWidget(QLabel("Total Size"), 0, 1)
        self.total_size_label = QLabel("0 GB")
        self.total_size_label.setProperty("class", "stat")
        grid_layout.addWidget(self.total_size_label, 1, 1)
        
        # Processed documents
        grid_layout.addWidget(QLabel("Processed"), 2, 0)
        self.processed_documents_label = QLabel("0")
        self.processed_documents_label.setProperty("class", "stat")
        grid_layout.addWidget(self.processed_documents_label, 3, 0)
        
        # Pending processing
        grid_layout.addWidget(QLabel("Pending"), 2, 1)
        self.pending_processing_label = QLabel("0")
        self.pending_processing_label.setProperty("class", "stat")
        grid_layout.addWidget(self.pending_processing_label, 3, 1)
        
        # Processing progress
        grid_layout.addWidget(QLabel("Processing Progress"), 4, 0, 1, 2)
        self.processing_progress_bar = QProgressBar()
        self.processing_progress_bar.setRange(0, 100)
        self.processing_progress_bar.setValue(0)
        grid_layout.addWidget(self.processing_progress_bar, 5, 0, 1, 2)
        
        # Average quality
        grid_layout.addWidget(QLabel("Average Quality"), 6, 0)
        self.average_quality_label = QLabel("0")
        self.average_quality_label.setProperty("class", "stat")
        grid_layout.addWidget(self.average_quality_label, 7, 0)
        
        # Last updated
        grid_layout.addWidget(QLabel("Last Updated"), 6, 1)
        self.last_updated_label = QLabel("Never")
        self.last_updated_label.setProperty("class", "desc")
        grid_layout.addWidget(self.last_updated_label, 7, 1)
        
        # Set size policy
        self.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
    
    def update_statistics(self, statistics):
        """Update statistics display"""
        try:
            # Update labels
            self.total_documents_label.setText(str(statistics.get("total_documents", 0)))
            self.total_size_label.setText(f"{statistics.get('total_size_gb', 0):.1f} GB")
            self.processed_documents_label.setText(str(statistics.get("processed_documents", 0)))
            self.pending_processing_label.setText(str(statistics.get("pending_processing", 0)))
            
            # Calculate and update progress bar
            total_docs = statistics.get("total_documents", 0)
            if total_docs > 0:
                processed = statistics.get("processed_documents", 0)
                progress_percent = min(100, int((processed / total_docs) * 100))
                self.processing_progress_bar.setValue(progress_percent)
            else:
                self.processing_progress_bar.setValue(0)
            
            # Update quality
            quality = statistics.get("average_quality", 0)
            self.average_quality_label.setText(f"{quality:.2f}")
            
            # Set color based on quality
            if quality >= 0.8:
                color = "#2e7d32"  # Green
            elif quality >= 0.6:
                color = "#f9a825"  # Amber
            else:
                color = "#c62828"  # Red
            self.average_quality_label.setStyleSheet(f"font-size: 22px; font-weight: bold; color: {color};")
            
            # Update last updated
            self.last_updated_label.setText(statistics.get("last_updated", "Never"))
            
        except Exception as e:
            self.logger.error(f"Error updating statistics: {e}")
```