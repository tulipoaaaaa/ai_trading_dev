from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QPushButton, QProgressBar, QSpinBox,
                             QTableWidget, QTableWidgetItem, QHeaderView,
                             QComboBox, QCheckBox, QMessageBox)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QColor, QBrush, QPalette

from shared_tools.ui_wrappers.processors.corpus_balancer_wrapper import CorpusBalancerWrapper


class BalancerTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.balancer = CorpusBalancerWrapper(project_config)
        self.setup_ui()
        self.connect_signals()
        self.refresh_corpus_stats()
    
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Current Distribution
        current_group = QGroupBox("Current Corpus Distribution")
        current_layout = QVBoxLayout(current_group)
        
        # Domain table
        self.domain_table = QTableWidget(8, 5)  # 8 domains, 5 columns
        self.domain_table.setHorizontalHeaderLabels([
            "Domain", "Target %", "Current %", "Document Count", "Progress"
        ])
        
        # Set up table properties
        self.domain_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.domain_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        self.domain_table.verticalHeader().setVisible(False)
        
        current_layout.addWidget(self.domain_table)
        
        # Initialize with domains
        domains = [
            "Crypto Derivatives", 
            "High Frequency Trading",
            "Risk Management",
            "Market Microstructure",
            "DeFi",
            "Portfolio Construction",
            "Valuation Models",
            "Regulation & Compliance"
        ]
        
        # Default targets (as percentages)
        targets = [20, 15, 15, 15, 12, 10, 8, 5]
        
        for i, (domain, target) in enumerate(zip(domains, targets)):
            # Domain name
            domain_item = QTableWidgetItem(domain)
            domain_item.setFlags(domain_item.flags() & ~Qt.ItemFlag.ItemIsEditable)
            self.domain_table.setItem(i, 0, domain_item)
            
            # Target percentage
            target_item = QTableWidgetItem(f"{target}%")
            self.domain_table.setItem(i, 1, target_item)
            
            # Current percentage (will be updated with real data)
            current_item = QTableWidgetItem("0%")
            self.domain_table.setItem(i, 2, current_item)
            
            # Document count (will be updated with real data)
            count_item = QTableWidgetItem("0")
            self.domain_table.setItem(i, 3, count_item)
            
            # Progress bar
            progress_bar = QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setValue(0)
            self.domain_table.setCellWidget(i, 4, progress_bar)
        
        main_layout.addWidget(current_group)
        
        # Balancing Options
        options_group = QGroupBox("Balancing Options")
        options_layout = QVBoxLayout(options_group)
        
        # Quality threshold
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Minimum Quality Score:"))
        self.quality_threshold = QSpinBox()
        self.quality_threshold.setRange(0, 100)
        self.quality_threshold.setValue(70)
        quality_layout.addWidget(self.quality_threshold)
        options_layout.addLayout(quality_layout)
        
        # Balance method
        method_layout = QHBoxLayout()
        method_layout.addWidget(QLabel("Balancing Method:"))
        self.balance_method = QComboBox()
        self.balance_method.addItems([
            "Target Percentage", 
            "Equal Distribution",
            "Document Count Targets"
        ])
        method_layout.addWidget(self.balance_method)
        options_layout.addLayout(method_layout)
        
        # Additional options
        self.auto_classify = QCheckBox("Automatically classify unclassified documents")
        self.auto_classify.setChecked(True)
        options_layout.addWidget(self.auto_classify)
        
        self.preserve_existing = QCheckBox("Preserve existing domain assignments")
        self.preserve_existing.setChecked(True)
        options_layout.addWidget(self.preserve_existing)
        
        main_layout.addWidget(options_group)
        
        # Balance Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.refresh_btn = QPushButton("Refresh Corpus Stats")
        self.refresh_btn.clicked.connect(self.refresh_corpus_stats)
        controls_layout.addWidget(self.refresh_btn)
        
        self.analyze_btn = QPushButton("Analyze Imbalance")
        self.analyze_btn.clicked.connect(self.analyze_corpus_balance)
        controls_layout.addWidget(self.analyze_btn)
        
        self.balance_btn = QPushButton("Balance Corpus")
        self.balance_btn.clicked.connect(self.balance_corpus)
        controls_layout.addWidget(self.balance_btn)
        
        self.stop_btn = QPushButton("Stop")
        self.stop_btn.setEnabled(False)
        self.stop_btn.clicked.connect(self.stop_balancing)
        controls_layout.addWidget(self.stop_btn)
        
        main_layout.addWidget(controls_group)
        
        # Status area
        status_group = QGroupBox("Balancing Status")
        status_layout = QVBoxLayout(status_group)
        
        self.status_label = QLabel("Ready")
        status_layout.addWidget(self.status_label)
        
        self.overall_progress = QProgressBar()
        status_layout.addWidget(self.overall_progress)
        
        main_layout.addWidget(status_group)
    
    def connect_signals(self):
        # Connect balancer wrapper signals
        self.balancer.progress_updated.connect(self.overall_progress.setValue)
        self.balancer.status_updated.connect(self.status_label.setText)
        self.balancer.balance_completed.connect(self.on_balance_completed)
    
    def refresh_corpus_stats(self):
        """Refresh the corpus statistics display"""
        self.status_label.setText("Fetching corpus statistics...")
        
        # In a real implementation, this would fetch actual statistics
        # For now, simulate with sample data
        
        total_docs = 1250  # Simulated total
        
        # Simulate document counts for each domain
        domain_counts = {
            "Crypto Derivatives": 320,  # Higher than target (20%)
            "High Frequency Trading": 180,  # Roughly on target (15%)
            "Risk Management": 175,  # Roughly on target (15%)
            "Market Microstructure": 160,  # Slightly below target (15%)
            "DeFi": 200,  # Higher than target (12%)
            "Portfolio Construction": 100,  # On target (10%)
            "Valuation Models": 75,  # Slightly below target (8%)
            "Regulation & Compliance": 40,  # Below target (5%)
        }
        
        # Update the table with statistics
        for i in range(self.domain_table.rowCount()):
            domain = self.domain_table.item(i, 0).text()
            target_text = self.domain_table.item(i, 1).text()
            target = float(target_text.strip('%'))
            
            count = domain_counts.get(domain, 0)
            percentage = (count / total_docs) * 100 if total_docs > 0 else 0
            
            # Update current percentage
            self.domain_table.setItem(i, 2, QTableWidgetItem(f"{percentage:.1f}%"))
            
            # Update document count
            self.domain_table.setItem(i, 3, QTableWidgetItem(str(count)))
            
            # Update progress bar
            progress = self.domain_table.cellWidget(i, 4)
            progress.setValue(int(percentage))
            
            # Color code based on target vs actual
            if abs(percentage - target) <= 2:
                # On target (±2%)
                progress.setStyleSheet("QProgressBar::chunk { background-color: green; }")
            elif percentage < target:
                # Below target
                progress.setStyleSheet("QProgressBar::chunk { background-color: orange; }")
            else:
                # Above target
                progress.setStyleSheet("QProgressBar::chunk { background-color: blue; }")
        
        self.status_label.setText(f"Corpus contains {total_docs} documents across 8 domains")
    
    def analyze_corpus_balance(self):
        """Analyze the corpus balance and provide recommendations"""
        self.status_label.setText("Analyzing corpus balance...")
        
        # In a real implementation, this would perform a real analysis
        # For now, generate some sample recommendations
        
        imbalance_report = """
        <h3>Corpus Balance Analysis</h3>
        <p>The analysis identified the following imbalances:</p>
        <ul>
            <li><b>Overrepresented Domains:</b> DeFi (+4.0%), Crypto Derivatives (+5.6%)</li>
            <li><b>Underrepresented Domains:</b> Regulation & Compliance (-1.8%), Valuation Models (-1.0%)</li>
        </ul>
        <p>Recommended actions:</p>
        <ul>
            <li>Collect 23 more documents in Regulation & Compliance</li>
            <li>Collect 12 more documents in Valuation Models</li>
            <li>Consider moving 50 documents from DeFi to underrepresented domains</li>
            <li>Consider moving 70 documents from Crypto Derivatives to underrepresented domains</li>
        </ul>
        """
        
        # Show the analysis in a message box
        QMessageBox.information(
            self, "Corpus Balance Analysis", imbalance_report
        )
        
        self.status_label.setText("Balance analysis completed")
    
    def balance_corpus(self):
        """Start the corpus balancing process"""
        # Update UI state
        self.balance_btn.setEnabled(False)
        self.stop_btn.setEnabled(True)
        self.status_label.setText("Balancing corpus...")
        self.overall_progress.setValue(0)
        
        # Configure balancer
        quality_threshold = self.quality_threshold.value()
        method = self.balance_method.currentText()
        auto_classify = self.auto_classify.isChecked()
        preserve_existing = self.preserve_existing.isChecked()
        
        # Collect target percentages from the table
        targets = {}
        for i in range(self.domain_table.rowCount()):
            domain = self.domain_table.item(i, 0).text()
            target_text = self.domain_table.item(i, 1).text()
            target = float(target_text.strip('%'))
            targets[domain] = target
        
        # Start balancing
        self.balancer.set_quality_threshold(quality_threshold)
        self.balancer.set_balance_method(method)
        self.balancer.set_auto_classify(auto_classify)
        self.balancer.set_preserve_existing(preserve_existing)
        self.balancer.set_domain_targets(targets)
        
        # Start the balancing process
        self.balancer.start()
    
    def stop_balancing(self):
        """Stop the corpus balancing process"""
        self.balancer.stop()
        self.balance_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        self.status_label.setText("Balancing stopped")
    
    @pyqtSlot(dict)
    def on_balance_completed(self, results):
        """Handle completion of the balancing process"""
        self.balance_btn.setEnabled(True)
        self.stop_btn.setEnabled(False)
        
        # Update status
        moved_count = results.get('moved_count', 0)
        classified_count = results.get('classified_count', 0)
        
        self.status_label.setText(
            f"Balancing completed: {moved_count} documents moved, "
            f"{classified_count} documents classified"
        )
        
        # Refresh statistics to show the new balance
        self.refresh_corpus_stats()
        
        # Show completion message
        QMessageBox.information(
            self, "Balancing Complete",
            f"Corpus balancing completed successfully.\n\n"
            f"• {moved_count} documents were moved to new domains\n"
            f"• {classified_count} documents were classified\n\n"
            f"The corpus distribution has been updated to better match target percentages."
        )
