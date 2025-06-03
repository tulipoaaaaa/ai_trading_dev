from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
                             QLabel, QPushButton, QTextEdit, QComboBox,
                             QLineEdit, QCheckBox, QFileDialog, QSplitter,
                             QTableWidget, QTableWidgetItem, QHeaderView)
from PyQt6.QtCore import Qt, QTimer, pyqtSlot
from PyQt6.QtGui import QColor, QTextCharFormat, QBrush

import os
import re
from datetime import datetime


class LogsTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.log_files = {}
        self.current_log = None
        self.update_timer = None
        self.setup_ui()
        self.scan_log_directory()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Log navigation and filtering controls
        controls_layout = QHBoxLayout()
        
        # Log selector
        controls_layout.addWidget(QLabel("Log:"))
        self.log_selector = QComboBox()
        self.log_selector.setMinimumWidth(250)
        self.log_selector.currentIndexChanged.connect(self.on_log_selected)
        controls_layout.addWidget(self.log_selector)
        
        # Filter
        controls_layout.addWidget(QLabel("Filter:"))
        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter logs (regex supported)")
        self.filter_input.textChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.filter_input)
        
        # Level filter
        controls_layout.addWidget(QLabel("Level:"))
        self.level_filter = QComboBox()
        self.level_filter.addItems(["All", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"])
        self.level_filter.currentIndexChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.level_filter)
        
        # Date range (simplified for now)
        self.today_only = QCheckBox("Today Only")
        self.today_only.stateChanged.connect(self.apply_filters)
        controls_layout.addWidget(self.today_only)
        
        main_layout.addLayout(controls_layout)
        
        # Create a splitter for log table and details
        splitter = QSplitter(Qt.Orientation.Vertical)
        
        # Log entries table
        self.log_table = QTableWidget()
        self.log_table.setColumnCount(5)
        self.log_table.setHorizontalHeaderLabels(["Time", "Level", "Component", "Message", "Details"])
        
        # Configure table properties
        self.log_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.ResizeToContents)
        self.log_table.horizontalHeader().setSectionResizeMode(3, QHeaderView.ResizeMode.Stretch)
        self.log_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.log_table.clicked.connect(self.on_log_entry_selected)
        
        splitter.addWidget(self.log_table)
        
        # Log detail view
        self.log_detail = QTextEdit()
        self.log_detail.setReadOnly(True)
        splitter.addWidget(self.log_detail)
        
        # Set initial splitter sizes (70% table, 30% details)
        splitter.setSizes([700, 300])
        
        main_layout.addWidget(splitter, 1)
        
        # Controls at the bottom
        bottom_layout = QHBoxLayout()
        
        self.auto_refresh = QCheckBox("Auto-refresh")
        self.auto_refresh.setChecked(True)
        self.auto_refresh.stateChanged.connect(self.toggle_auto_refresh)
        bottom_layout.addWidget(self.auto_refresh)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_logs)
        bottom_layout.addWidget(self.refresh_btn)
        
        self.clear_filter_btn = QPushButton("Clear Filter")
        self.clear_filter_btn.clicked.connect(self.clear_filters)
        bottom_layout.addWidget(self.clear_filter_btn)
        
        self.export_btn = QPushButton("Export Logs")
        self.export_btn.clicked.connect(self.export_logs)
        bottom_layout.addWidget(self.export_btn)
        
        self.clear_logs_btn = QPushButton("Clear Log View")
        self.clear_logs_btn.clicked.connect(self.clear_log_view)
        bottom_layout.addWidget(self.clear_logs_btn)
        
        main_layout.addLayout(bottom_layout)
        
        # Set up auto-refresh timer
        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.refresh_logs)
        self.update_timer.start(5000)  # Refresh every 5 seconds
    
    def scan_log_directory(self):
        """Scan for log files in the configured log directory"""
        # In a real implementation, this would use project_config to get the log directory
        # For now, use a placeholder path
        try:
            log_dir = self.project_config.get_logs_dir()
        except:
            log_dir = os.path.expanduser("~/.cryptofinance/logs")
        
        # Placeholder - in a real implementation this would scan the actual directory
        # For demonstration, populate with sample log files
        self.log_files = {
            "collectors.log": {"path": f"{log_dir}/collectors.log", "type": "collector"},
            "processors.log": {"path": f"{log_dir}/processors.log", "type": "processor"},
            "app.log": {"path": f"{log_dir}/app.log", "type": "app"},
            "errors.log": {"path": f"{log_dir}/errors.log", "type": "error"}
        }
        
        # Update the log selector
        self.log_selector.clear()
        for log_name in self.log_files:
            self.log_selector.addItem(log_name)
        
        # Load the first log if available
        if self.log_selector.count() > 0:
            self.on_log_selected(0)
    
    def on_log_selected(self, index):
        """Handle log file selection"""
        if index >= 0:
            log_name = self.log_selector.currentText()
            self.current_log = self.log_files.get(log_name)
            self.refresh_logs()
    
    def refresh_logs(self):
        """Refresh the current log view"""
        if not self.current_log:
            return
            
        # In a real implementation, this would read from the actual log file
        # For demonstration, generate sample log entries
        log_entries = self.generate_sample_logs(self.current_log["type"])
        
        # Apply filters
        filtered_entries = self.filter_log_entries(log_entries)
        
        # Update the table
        self.populate_log_table(filtered_entries)
    
    def generate_sample_logs(self, log_type):
        """Generate sample log entries for demonstration"""
        entries = []
        
        # Current time as base
        now = datetime.now()
        
        # Different log patterns based on log type
        if log_type == "collector":
            components = ["ISDACollector", "GitHubCollector", "AnnaArchiveCollector", "ArxivCollector"]
            messages = [
                "Started collection process",
                "Connecting to API",
                "Retrieved document list",
                "Downloaded document",
                "Collection completed",
                "Error connecting to API",
                "Rate limit exceeded",
                "Authentication failed"
            ]
            
            # Generate 20 sample entries
            for i in range(20):
                # Randomize time within the last day
                time_offset = i * 30  # 30 minutes between entries
                entry_time = now.replace(
                    hour=(now.hour - (time_offset // 60)) % 24,
                    minute=(now.minute - (time_offset % 60)) % 60
                )
                
                # Randomly select component and message
                component = components[i % len(components)]
                message_index = i % len(messages)
                message = messages[message_index]
                
                # Determine level based on message
                if "Error" in message or "failed" in message:
                    level = "ERROR"
                elif "exceeded" in message:
                    level = "WARNING"
                elif "Started" in message:
                    level = "INFO"
                else:
                    level = "DEBUG"
                
                # Create details
                if level == "ERROR":
                    details = f"Exception occurred: ConnectionError\nTraceback: File \"collector.py\", line 120\nCannot connect to server"
                else:
                    details = f"Additional information for {message.lower()}"
                
                entries.append({
                    "time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": level,
                    "component": component,
                    "message": message,
                    "details": details
                })
        
        elif log_type == "processor":
            components = ["PDFProcessor", "TextProcessor", "BalancerProcessor", "QualityControl"]
            messages = [
                "Processing file",
                "Extraction complete",
                "Failed to extract text",
                "OCR fallback used",
                "Detected language",
                "Quality score calculated",
                "File categorized",
                "Error processing file"
            ]
            
            # Generate 20 sample entries
            for i in range(20):
                # Randomize time within the last day
                time_offset = i * 15  # 15 minutes between entries
                entry_time = now.replace(
                    hour=(now.hour - (time_offset // 60)) % 24,
                    minute=(now.minute - (time_offset % 60)) % 60
                )
                
                # Randomly select component and message
                component = components[i % len(components)]
                message_index = i % len(messages)
                message = messages[message_index]
                
                # Add a file name to the message
                file_name = f"document_{i+1}.{'pdf' if component == 'PDFProcessor' else 'txt'}"
                full_message = f"{message}: {file_name}"
                
                # Determine level based on message
                if "Error" in message or "Failed" in message:
                    level = "ERROR"
                elif "fallback" in message:
                    level = "WARNING"
                elif "Processing" in message:
                    level = "INFO"
                else:
                    level = "DEBUG"
                
                # Create details
                if level == "ERROR":
                    details = f"Exception occurred: ProcessingError\nTraceback: File \"{component.lower()}.py\", line 87\nCannot process file {file_name}"
                elif "language" in message.lower():
                    details = f"Detected language: English\nConfidence: 95%\nAlternatives: None"
                elif "score" in message.lower():
                    details = f"Quality score: 87/100\nFactors:\n- Text quality: 90/100\n- Structure: 85/100\n- Content relevance: 88/100"
                else:
                    details = f"File: {file_name}\nSize: 1.2MB\nPages: 8"
                
                entries.append({
                    "time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": level,
                    "component": component,
                    "message": full_message,
                    "details": details
                })
        
        elif log_type == "app":
            components = ["MainWindow", "CollectorsTab", "ProcessorsTab", "CorpusManager"]
            messages = [
                "Application started",
                "Configuration loaded",
                "Tab initialized",
                "User action: start collection",
                "User action: stop processing",
                "Dialog opened",
                "Settings saved",
                "Application shutdown initiated"
            ]
            
            # Generate 15 sample entries
            for i in range(15):
                # Randomize time within the last day
                time_offset = i * 45  # 45 minutes between entries
                entry_time = now.replace(
                    hour=(now.hour - (time_offset // 60)) % 24,
                    minute=(now.minute - (time_offset % 60)) % 60
                )
                
                # Randomly select component and message
                component = components[i % len(components)]
                message_index = i % len(messages)
                message = messages[message_index]
                
                # Determine level
                level = "INFO"  # Most app logs are INFO level
                
                # Create details
                if "started" in message.lower():
                    details = f"App version: 3.0.1\nPython version: 3.8.10\nPyQt version: 6.6.0"
                elif "configuration" in message.lower():
                    details = f"Config file: config/test.yaml\nEnvironment: test"
                elif "user action" in message.lower():
                    details = f"User: admin\nAction time: {entry_time.strftime('%H:%M:%S')}"
                else:
                    details = ""
                
                entries.append({
                    "time": entry_time.strftime("%Y-%m-%d %H:%M:%S"),
                    "level": level,
                    "component": component,
                    "message": message,
                    "details": details
                })
        
        elif log_type == "error":
            components =
