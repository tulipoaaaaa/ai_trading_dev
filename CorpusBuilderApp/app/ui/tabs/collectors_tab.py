from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QLabel, QProgressBar, QPushButton, QComboBox,
                             QSpinBox, QLineEdit, QGroupBox, QScrollArea)
from PyQt6.QtCore import Qt, pyqtSlot

from shared_tools.ui_wrappers.collectors.isda_wrapper import ISDAWrapper
from shared_tools.ui_wrappers.collectors.github_wrapper import GitHubWrapper
from shared_tools.ui_wrappers.collectors.anna_archive_wrapper import AnnaArchiveWrapper
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
        self.collector_tabs.addTab(self.create_isda_tab(), "ISDA")
        self.collector_tabs.addTab(self.create_github_tab(), "GitHub")
        self.collector_tabs.addTab(self.create_anna_tab(), "Anna's Archive")
        self.collector_tabs.addTab(self.create_arxiv_tab(), "arXiv")
        self.collector_tabs.addTab(self.create_fred_tab(), "FRED")
        self.collector_tabs.addTab(self.create_bitmex_tab(), "BitMEX")
        self.collector_tabs.addTab(self.create_quantopian_tab(), "Quantopian")
        self.collector_tabs.addTab(self.create_scidb_tab(), "SciDB")
        self.collector_tabs.addTab(self.create_web_tab(), "Web")
        
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

    def create_isda_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Configuration group
        config_group = QGroupBox("ISDA Collector Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Keywords
        keywords_layout = QHBoxLayout()
        keywords_layout.addWidget(QLabel("Keywords:"))
        self.isda_keywords = QLineEdit("derivatives, protocol, crypto, blockchain")
        keywords_layout.addWidget(self.isda_keywords)
        config_layout.addLayout(keywords_layout)
        
        # Max sources
        max_sources_layout = QHBoxLayout()
        max_sources_layout.addWidget(QLabel("Max Sources:"))
        self.isda_max_sources = QSpinBox()
        self.isda_max_sources.setRange(1, 1000)
        self.isda_max_sources.setValue(50)
        max_sources_layout.addWidget(self.isda_max_sources)
        config_layout.addLayout(max_sources_layout)
        
        layout.addWidget(config_group)
        
        # Controls group
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.isda_start_btn = QPushButton("Start Collection")
        self.isda_stop_btn = QPushButton("Stop")
        self.isda_stop_btn.setEnabled(False)
        
        controls_layout.addWidget(self.isda_start_btn)
        controls_layout.addWidget(self.isda_stop_btn)
        
        layout.addWidget(controls_group)
        
        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.isda_status = QLabel("Ready")
        progress_layout.addWidget(self.isda_status)
        
        self.isda_progress_bar = QProgressBar()
        self.isda_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.isda_progress_bar)
        
        layout.addWidget(progress_group)
        layout.addStretch()
        
        return tab

    # Create similar methods for other collectors
    def create_github_tab(self):
        # Similar to create_isda_tab but with GitHub-specific fields
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Configuration group
        config_group = QGroupBox("GitHub Collector Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Repository search terms
        terms_layout = QHBoxLayout()
        terms_layout.addWidget(QLabel("Search Terms:"))
        self.github_terms = QLineEdit("crypto trading, blockchain analysis")
        terms_layout.addWidget(self.github_terms)
        config_layout.addLayout(terms_layout)
        
        # Language filter
        lang_layout = QHBoxLayout()
        lang_layout.addWidget(QLabel("Language:"))
        self.github_language = QComboBox()
        for lang in ["All", "Python", "JavaScript", "Go", "Rust", "C++", "Java"]:
            self.github_language.addItem(lang)
        lang_layout.addWidget(self.github_language)
        config_layout.addLayout(lang_layout)
        
        # Stars filter
        stars_layout = QHBoxLayout()
        stars_layout.addWidget(QLabel("Min Stars:"))
        self.github_stars = QSpinBox()
        self.github_stars.setRange(0, 10000)
        self.github_stars.setValue(50)
        stars_layout.addWidget(self.github_stars)
        config_layout.addLayout(stars_layout)
        
        layout.addWidget(config_group)
        
        # Controls group
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.github_start_btn = QPushButton("Start Collection")
        self.github_stop_btn = QPushButton("Stop")
        self.github_stop_btn.setEnabled(False)
        
        controls_layout.addWidget(self.github_start_btn)
        controls_layout.addWidget(self.github_stop_btn)
        
        layout.addWidget(controls_group)
        
        # Progress group
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.github_status = QLabel("Ready")
        progress_layout.addWidget(self.github_status)
        
        self.github_progress_bar = QProgressBar()
        self.github_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.github_progress_bar)
        
        layout.addWidget(progress_group)
        layout.addStretch()
        
        return tab

    def create_anna_tab(self):
        # Similar implementation for Anna's Archive
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_arxiv_tab(self):
        # Similar implementation for arXiv
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_fred_tab(self):
        # Similar implementation for FRED
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_bitmex_tab(self):
        # Similar implementation for BitMEX
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_quantopian_tab(self):
        # Similar implementation for Quantopian
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_scidb_tab(self):
        # Similar implementation for SciDB
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def create_web_tab(self):
        # Similar implementation for Web scraper
        tab = QWidget()
        # Implementation similar to other collectors
        return tab

    def init_collectors(self):
        # Initialize all collector wrappers
        self.collector_wrappers['isda'] = ISDAWrapper(self.project_config)
        self.collector_wrappers['github'] = GitHubWrapper(self.project_config)
        self.collector_wrappers['anna'] = AnnaArchiveWrapper(self.project_config)
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
