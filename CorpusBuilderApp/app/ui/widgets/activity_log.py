"""
Activity Log Widget for Dashboard
"""

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QHeaderView, QFrame, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor, QIcon
import logging

class ActivityLogWidget(QFrame):
    """Widget displaying recent activity log"""
    
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
            QTableWidget {
                border: none;
                gridline-color: #f0f0f0;
            }
            QHeaderView::section {
                background-color: #f0f0f0;
                padding: 4px;
                font-weight: bold;
                border: none;
                border-bottom: 1px solid #d0d0d0;
            }
        """)
        
        # Initialize UI
        self.init_ui()
    
    def init_ui(self):
        """Initialize the user interface"""
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Activity table
        self.activity_table = QTableWidget()
        self.activity_table.setColumnCount(4)
        self.activity_table.setHorizontalHeaderLabels(["Time", "Action", "Status", "Details"])
        
        # Set column widths
        self.activity_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)
        self.activity_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.activity_table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)
        self.activity_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)
        
        # Set table properties
        self.activity_table.setAlternatingRowColors(True)
        self.activity_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.activity_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.activity_table.setShowGrid(True)
        
        layout.addWidget(self.activity_table)
    
    def update_activity_log(self, activities):
        """Update activity log display"""
        try:
            # Clear existing rows
            self.activity_table.setRowCount(0)
            
            # Add activities
            for activity in activities:
                row = self.activity_table.rowCount()
                self.activity_table.insertRow(row)
                
                # Time
                time_item = QTableWidgetItem(activity.get("time", ""))
                self.activity_table.setItem(row, 0, time_item)
                
                # Action
                action_item = QTableWidgetItem(activity.get("action", ""))
                self.activity_table.setItem(row, 1, action_item)
                
                # Status
                status = activity.get("status", "")
                status_item = QTableWidgetItem(status)
                
                # Set status color
                if status == "success":
                    status_item.setForeground(QColor("#2e7d32"))  # Green
                elif status == "running":
                    status_item.setForeground(QColor("#1976d2"))  # Blue
                elif status == "error" or status == "failed":
                    status_item.setForeground(QColor("#c62828"))  # Red
                else:
                    status_item.setForeground(QColor("#757575"))  # Gray
                
                self.activity_table.setItem(row, 2, status_item)
                
                # Details
                details_item = QTableWidgetItem(activity.get("details", ""))
                self.activity_table.setItem(row, 3, details_item)
            
        except Exception as e:
            self.logger.error(f"Error updating activity log: {e}")
```