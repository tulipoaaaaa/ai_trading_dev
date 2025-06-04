from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QLabel, QProgressBar, QPushButton, QComboBox,
                             QSpinBox, QLineEdit, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSlot

from shared_tools.ui_wrappers.collectors.isda_wrapper import ISDAWrapper
from shared_tools.ui_wrappers.collectors.github_wrapper import GitHubWrapper
from shared_tools.ui_wrappers.collectors.annas_archive_wrapper import AnnasArchiveWrapper
from shared_tools.ui_wrappers.collectors.arxiv_wrapper import ArxivWrapper
from shared_tools.ui_wrappers.collectors.fred_wrapper import FREDWrapper
from shared_tools.ui_wrappers.collectors.bitmex_wrapper import BitMEXWrapper
from shared_tools.ui_wrappers.collectors.quantopian_wrapper import QuantopianWrapper
from shared_tools.ui_wrappers.collectors.scidb_wrapper import SciDBWrapper
from shared_tools.ui_wrappers.collectors.web_wrapper import WebWrapper


class CollectorsTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.collector_wrappers = {}
        self.setup_ui()
        self.init_collectors()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Collector tabs widget
        self.collector_tabs = QTabWidget()
        
        # Create tabs for each collector
        self.collector_tabs.addTab(ISDAWrapper(), "ISDA")
        self.collector_tabs.addTab(GitHubWrapper(), "GitHub")
        self.collector_tabs.addTab(AnnasArchiveWrapper(), "Anna's Archive")
        self.collector_tabs.addTab(ArxivWrapper(), "arXiv")
        self.collector_tabs.addTab(FREDWrapper(), "FRED")
        self.collector_tabs.addTab(BitMEXWrapper(), "BitMEX")
        self.collector_tabs.addTab(QuantopianWrapper(), "Quantopian")
        self.collector_tabs.addTab(SciDBWrapper(), "SciDB")
        self.collector_tabs.addTab(WebWrapper(), "Web")
        
        main_layout.addWidget(self.collector_tabs)
        
        # Add a status/summary area at the bottom
        status_group = QGroupBox("Collection Status")
        status_layout = QVBoxLayout(status_group)
        
        self.collection_status_label = QLabel("Ready to collect data")
        status_layout.addWidget(self.collection_status_label)
        
        # Overall progress bar
        self.overall_progress = QProgressBar()
        self.overall_progress.setRange(0, 100)
        self.overall_progress.setValue(0)
        status_layout.addWidget(self.overall_progress)
        
        # Button for stopping all collectors
        stop_all_btn = QPushButton("Stop All Collectors")
        stop_all_btn.clicked.connect(self.stop_all_collectors)
        status_layout.addWidget(stop_all_btn)
        
        main_layout.addWidget(status_group)

    def init_collectors(self):
        # Initialize all collector wrappers
        self.collector_wrappers['isda'] = ISDAWrapper(self.project_config)
        self.collector_wrappers['github'] = GitHubWrapper(self.project_config)
        self.collector_wrappers['anna'] = AnnasArchiveWrapper(self.project_config)
        self.collector_wrappers['arxiv'] = ArxivWrapper(self.project_config)
        self.collector_wrappers['fred'] = FREDWrapper(self.project_config)
        self.collector_wrappers['bitmex'] = BitMEXWrapper(self.project_config)
        self.collector_wrappers['quantopian'] = QuantopianWrapper(self.project_config)
        self.collector_wrappers['scidb'] = SciDBWrapper(self.project_config)
        self.collector_wrappers['web'] = WebWrapper(self.project_config)

    def connect_signals(self):
        # Connect signals for ISDA collector
        self.isda_start_btn.clicked.connect(self.start_isda_collection)
        self.isda_stop_btn.clicked.connect(self.stop_isda_collection)
        
        isda_wrapper = self.collector_wrappers['isda']
        isda_wrapper.progress_updated.connect(self.isda_progress_bar.setValue)
        isda_wrapper.status_updated.connect(self.isda_status.setText)
        isda_wrapper.collection_completed.connect(self.on_isda_collection_completed)
        
        # Connect signals for GitHub collector
        self.github_start_btn.clicked.connect(self.start_github_collection)
        self.github_stop_btn.clicked.connect(self.stop_github_collection)
        
        github_wrapper = self.collector_wrappers['github']
        github_wrapper.progress_updated.connect(self.github_progress_bar.setValue)
        github_wrapper.status_updated.connect(self.github_status.setText)
        github_wrapper.collection_completed.connect(self.on_github_collection_completed)
        
        # Connect signals for other collectors similarly
        # ...

    def start_isda_collection(self):
        isda_wrapper = self.collector_wrappers['isda']
        
        # Set configuration from UI
        keywords = [k.strip() for k in self.isda_keywords.text().split(',')]
        max_sources = self.isda_max_sources.value()
        
        isda_wrapper.set_search_keywords(keywords)
        isda_wrapper.set_max_sources(max_sources)
        
        # Update UI state
        self.isda_start_btn.setEnabled(False)
        self.isda_stop_btn.setEnabled(True)
        
        # Start collection
        isda_wrapper.start()

    def stop_isda_collection(self):
        self.collector_wrappers['isda'].stop()
        self.isda_start_btn.setEnabled(True)
        self.isda_stop_btn.setEnabled(False)

    def start_github_collection(self):
        github_wrapper = self.collector_wrappers['github']
        
        # Set configuration from UI
        terms = [t.strip() for t in self.github_terms.text().split(',')]
        language = self.github_language.currentText()
        if language == "All":
            language = None
        min_stars = self.github_stars.value()
        
        github_wrapper.set_search_terms(terms)
        github_wrapper.set_language_filter(language)
        github_wrapper.set_min_stars(min_stars)
        
        # Update UI state
        self.github_start_btn.setEnabled(False)
        self.github_stop_btn.setEnabled(True)
        
        # Start collection
        github_wrapper.start()

    def stop_github_collection(self):
        self.collector_wrappers['github'].stop()
        self.github_start_btn.setEnabled(True)
        self.github_stop_btn.setEnabled(False)
    
    # Add similar methods for other collectors
    
    @pyqtSlot(dict)
    def on_isda_collection_completed(self, results):
        self.isda_start_btn.setEnabled(True)
        self.isda_stop_btn.setEnabled(False)
        
        # Update status and possibly show a notification
        message = f"ISDA collection completed: {len(results.get('documents', []))} documents collected"
        self.collection_status_label.setText(message)
        
        # You could emit a signal here to notify other parts of the application

    @pyqtSlot(dict)
    def on_github_collection_completed(self, results):
        self.github_start_btn.setEnabled(True)
        self.github_stop_btn.setEnabled(False)
        
        # Update status
        message = f"GitHub collection completed: {len(results.get('repositories', []))} repositories collected"
        self.collection_status_label.setText(message)

    def stop_all_collectors(self):
        for collector_name, wrapper in self.collector_wrappers.items():
            wrapper.stop()
        
        # Reset UI elements
        self.isda_start_btn.setEnabled(True)
        self.isda_stop_btn.setEnabled(False)
        self.github_start_btn.setEnabled(True)
        self.github_stop_btn.setEnabled(False)
        # Reset other collector buttons similarly
        
        self.collection_status_label.setText("All collectors stopped")
