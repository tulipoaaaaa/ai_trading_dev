from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTabWidget, 
                             QLabel, QProgressBar, QPushButton, QCheckBox, 
                             QSpinBox, QListWidget, QGroupBox, QFileDialog)
from PyQt6.QtCore import Qt, pyqtSlot
import os

from shared_tools.ui_wrappers.processors.pdf_extractor_wrapper import PDFExtractorWrapper
from shared_tools.ui_wrappers.processors.text_extractor_wrapper import TextExtractorWrapper
from shared_tools.ui_wrappers.processors.corpus_balancer_wrapper import CorpusBalancerWrapper
from shared_tools.ui_wrappers.processors.quality_control_wrapper import QualityControlWrapper
from shared_tools.ui_wrappers.processors.deduplicator_wrapper import DeduplicatorWrapper
from shared_tools.ui_wrappers.processors.domain_classifier_wrapper import DomainClassifierWrapper
from shared_tools.ui_wrappers.processors.formula_extractor_wrapper import FormulaExtractorWrapper
from shared_tools.ui_wrappers.processors.chart_image_extractor_wrapper import ChartImageExtractorWrapper
from shared_tools.ui_wrappers.processors.language_confidence_detector_wrapper import LanguageConfidenceDetectorWrapper
from shared_tools.ui_wrappers.processors.machine_translation_detector_wrapper import MachineTranslationDetectorWrapper
from shared_tools.ui_wrappers.processors.financial_symbol_processor_wrapper import FinancialSymbolProcessorWrapper


class ProcessorsTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.processor_wrappers = {}
        self.file_queue = []
        self.setup_ui()
        self.init_processors()
        self.connect_signals()

    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Create tabs for different processor types
        self.processor_tabs = QTabWidget()
        self.processor_tabs.addTab(self.create_pdf_tab(), "PDF Processing")
        self.processor_tabs.addTab(self.create_text_tab(), "Text Processing")
        self.processor_tabs.addTab(self.create_advanced_tab(), "Advanced Processing")
        self.processor_tabs.addTab(self.create_batch_tab(), "Batch Operations")
        
        main_layout.addWidget(self.processor_tabs)
        
        # Add a status/summary area at the bottom
        status_group = QGroupBox("Processing Status")
        status_layout = QVBoxLayout(status_group)
        
        self.processing_status_label = QLabel("Ready to process files")
        status_layout.addWidget(self.processing_status_label)
        
        # Overall progress bar
        self.overall_progress = QProgressBar()
        self.overall_progress.setRange(0, 100)
        self.overall_progress.setValue(0)
        status_layout.addWidget(self.overall_progress)
        
        # Button for stopping all processors
        stop_all_btn = QPushButton("Stop All Processors")
        stop_all_btn.clicked.connect(self.stop_all_processors)
        status_layout.addWidget(stop_all_btn)
        
        main_layout.addWidget(status_group)

    def create_pdf_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Configuration group
        config_group = QGroupBox("PDF Processor Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # OCR options
        self.ocr_enabled = QCheckBox("Enable OCR for scanned documents")
        self.ocr_enabled.setChecked(True)
        config_layout.addWidget(self.ocr_enabled)
        
        # Table extraction
        self.table_extraction = QCheckBox("Extract tables")
        self.table_extraction.setChecked(True)
        config_layout.addWidget(self.table_extraction)
        
        # Formula extraction
        self.formula_extraction = QCheckBox("Extract mathematical formulas")
        self.formula_extraction.setChecked(True)
        config_layout.addWidget(self.formula_extraction)
        
        # Thread count
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("Worker Threads:"))
        self.pdf_threads = QSpinBox()
        self.pdf_threads.setRange(1, 16)
        self.pdf_threads.setValue(4)
        thread_layout.addWidget(self.pdf_threads)
        config_layout.addLayout(thread_layout)
        
        layout.addWidget(config_group)
        
        # File selection
        files_group = QGroupBox("PDF Files")
        files_layout = QVBoxLayout(files_group)
        
        file_buttons_layout = QHBoxLayout()
        self.add_pdf_btn = QPushButton("Add PDF Files")
        self.add_pdf_btn.clicked.connect(self.add_pdf_files)
        self.clear_pdf_btn = QPushButton("Clear List")
        self.clear_pdf_btn.clicked.connect(self.clear_pdf_files)
        file_buttons_layout.addWidget(self.add_pdf_btn)
        file_buttons_layout.addWidget(self.clear_pdf_btn)
        
        files_layout.addLayout(file_buttons_layout)
        
        self.pdf_file_list = QListWidget()
        files_layout.addWidget(self.pdf_file_list)
        
        layout.addWidget(files_group)
        
        # Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.pdf_start_btn = QPushButton("Start Processing")
        self.pdf_stop_btn = QPushButton("Stop")
        self.pdf_stop_btn.setEnabled(False)
        
        controls_layout.addWidget(self.pdf_start_btn)
        controls_layout.addWidget(self.pdf_stop_btn)
        
        layout.addWidget(controls_group)
        
        # Progress
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.pdf_status = QLabel("Ready")
        progress_layout.addWidget(self.pdf_status)
        
        self.pdf_progress_bar = QProgressBar()
        self.pdf_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.pdf_progress_bar)
        
        layout.addWidget(progress_group)
        
        return tab

    def create_text_tab(self):
        # Similar to PDF tab but for text files
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Configuration group
        config_group = QGroupBox("Text Processor Configuration")
        config_layout = QVBoxLayout(config_group)
        
        # Language detection
        self.language_detection = QCheckBox("Enable language detection")
        self.language_detection.setChecked(True)
        config_layout.addWidget(self.language_detection)
        
        # Quality threshold
        quality_layout = QHBoxLayout()
        quality_layout.addWidget(QLabel("Quality Threshold:"))
        self.quality_threshold = QSpinBox()
        self.quality_threshold.setRange(0, 100)
        self.quality_threshold.setValue(80)
        quality_layout.addWidget(self.quality_threshold)
        config_layout.addLayout(quality_layout)
        
        # Thread count
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("Worker Threads:"))
        self.text_threads = QSpinBox()
        self.text_threads.setRange(1, 16)
        self.text_threads.setValue(4)
        thread_layout.addWidget(self.text_threads)
        config_layout.addLayout(thread_layout)
        
        layout.addWidget(config_group)
        
        # File selection
        files_group = QGroupBox("Text Files")
        files_layout = QVBoxLayout(files_group)
        
        file_buttons_layout = QHBoxLayout()
        self.add_text_btn = QPushButton("Add Text Files")
        self.add_text_btn.clicked.connect(self.add_text_files)
        self.clear_text_btn = QPushButton("Clear List")
        self.clear_text_btn.clicked.connect(self.clear_text_files)
        file_buttons_layout.addWidget(self.add_text_btn)
        file_buttons_layout.addWidget(self.clear_text_btn)
        
        files_layout.addLayout(file_buttons_layout)
        
        self.text_file_list = QListWidget()
        files_layout.addWidget(self.text_file_list)
        
        layout.addWidget(files_group)
        
        # Controls and progress similar to PDF tab
        controls_group = QGroupBox("Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.text_start_btn = QPushButton("Start Processing")
        self.text_stop_btn = QPushButton("Stop")
        self.text_stop_btn.setEnabled(False)
        
        controls_layout.addWidget(self.text_start_btn)
        controls_layout.addWidget(self.text_stop_btn)
        
        layout.addWidget(controls_group)
        
        progress_group = QGroupBox("Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.text_status = QLabel("Ready")
        progress_layout.addWidget(self.text_status)
        
        self.text_progress_bar = QProgressBar()
        self.text_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.text_progress_bar)
        
        layout.addWidget(progress_group)
        
        return tab

    def create_advanced_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Advanced processing options
        advanced_group = QGroupBox("Advanced Processing Options")
        advanced_layout = QVBoxLayout(advanced_group)
        
        # Deduplication
        self.enable_deduplication = QCheckBox("Enable deduplication")
        self.enable_deduplication.setChecked(True)
        advanced_layout.addWidget(self.enable_deduplication)
        
        # Domain classification
        self.enable_domain_classification = QCheckBox("Enable domain classification")
        self.enable_domain_classification.setChecked(True)
        advanced_layout.addWidget(self.enable_domain_classification)
        
        # Financial symbol processing
        self.enable_financial_symbols = QCheckBox("Extract financial symbols")
        self.enable_financial_symbols.setChecked(True)
        advanced_layout.addWidget(self.enable_financial_symbols)
        
        # Language confidence
        self.enable_language_confidence = QCheckBox("Detect language confidence")
        self.enable_language_confidence.setChecked(True)
        advanced_layout.addWidget(self.enable_language_confidence)
        
        # Machine translation detection
        self.enable_mt_detection = QCheckBox("Detect machine translation")
        self.enable_mt_detection.setChecked(True)
        advanced_layout.addWidget(self.enable_mt_detection)
        
        layout.addWidget(advanced_group)
        
        # Batch operations group
        batch_group = QGroupBox("Apply to Corpus")
        batch_layout = QVBoxLayout(batch_group)
        
        self.apply_to_all_btn = QPushButton("Apply to Entire Corpus")
        self.apply_to_all_btn.clicked.connect(self.apply_advanced_processing)
        batch_layout.addWidget(self.apply_to_all_btn)
        
        self.apply_to_selected_btn = QPushButton("Apply to Selected Domain")
        batch_layout.addWidget(self.apply_to_selected_btn)
        
        layout.addWidget(batch_group)
        
        # Progress for batch operations
        progress_group = QGroupBox("Batch Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.advanced_status = QLabel("Ready")
        progress_layout.addWidget(self.advanced_status)
        
        self.advanced_progress_bar = QProgressBar()
        self.advanced_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.advanced_progress_bar)
        
        layout.addWidget(progress_group)
        
        return tab

    def create_batch_tab(self):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        
        # Batch processing options
        batch_config_group = QGroupBox("Batch Configuration")
        batch_config_layout = QVBoxLayout(batch_config_group)
        
        # Directory selection
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(QLabel("Input Directory:"))
        self.input_dir_path = QLabel("Not selected")
        dir_layout.addWidget(self.input_dir_path)
        self.select_input_dir_btn = QPushButton("Select...")
        self.select_input_dir_btn.clicked.connect(self.select_input_directory)
        dir_layout.addWidget(self.select_input_dir_btn)
        batch_config_layout.addLayout(dir_layout)
        
        # Recursive option
        self.recursive_processing = QCheckBox("Process subdirectories recursively")
        self.recursive_processing.setChecked(True)
        batch_config_layout.addWidget(self.recursive_processing)
        
        # File type selection
        file_type_layout = QHBoxLayout()
        file_type_layout.addWidget(QLabel("File Types:"))
        self.process_pdf = QCheckBox("PDF")
        self.process_pdf.setChecked(True)
        self.process_text = QCheckBox("Text")
        self.process_text.setChecked(True)
        self.process_docx = QCheckBox("DOCX")
        self.process_docx.setChecked(True)
        self.process_html = QCheckBox("HTML")
        self.process_html.setChecked(True)
        file_type_layout.addWidget(self.process_pdf)
        file_type_layout.addWidget(self.process_text)
        file_type_layout.addWidget(self.process_docx)
        file_type_layout.addWidget(self.process_html)
        batch_config_layout.addLayout(file_type_layout)
        
        # Thread count
        thread_layout = QHBoxLayout()
        thread_layout.addWidget(QLabel("Batch Threads:"))
        self.batch_threads = QSpinBox()
        self.batch_threads.setRange(1, 16)
        self.batch_threads.setValue(4)
        thread_layout.addWidget(self.batch_threads)
        batch_config_layout.addLayout(thread_layout)
        
        layout.addWidget(batch_config_group)
        
        # Controls
        controls_group = QGroupBox("Batch Controls")
        controls_layout = QHBoxLayout(controls_group)
        
        self.batch_start_btn = QPushButton("Start Batch Processing")
        self.batch_start_btn.clicked.connect(self.start_batch_processing)
        self.batch_stop_btn = QPushButton("Stop")
        self.batch_stop_btn.clicked.connect(self.stop_batch_processing)
        self.batch_stop_btn.setEnabled(False)
        
        controls_layout.addWidget(self.batch_start_btn)
        controls_layout.addWidget(self.batch_stop_btn)
        
        layout.addWidget(controls_group)
        
        # Progress
        progress_group = QGroupBox("Batch Progress")
        progress_layout = QVBoxLayout(progress_group)
        
        self.batch_status = QLabel("Ready")
        progress_layout.addWidget(self.batch_status)
        
        self.batch_progress_bar = QProgressBar()
        self.batch_progress_bar.setRange(0, 100)
        progress_layout.addWidget(self.batch_progress_bar)
        
        # Stats
        self.batch_stats = QLabel("No files processed yet")
        progress_layout.addWidget(self.batch_stats)
        
        layout.addWidget(progress_group)
        
        return tab

    def init_processors(self):
        # Initialize all processor wrappers
        self.processor_wrappers['pdf'] = PDFExtractorWrapper(self.project_config)
        self.processor_wrappers['text'] = TextExtractorWrapper(self.project_config)
        self.processor_wrappers['balancer'] = CorpusBalancerWrapper(self.project_config)
        self.processor_wrappers['quality'] = QualityControlWrapper(self.project_config)
        self.processor_wrappers['deduplicator'] = DeduplicatorWrapper(self.project_config)
        self.processor_wrappers['domain'] = DomainClassifierWrapper(self.project_config)
        self.processor_wrappers['formula'] = FormulaExtractorWrapper(self.project_config)
        self.processor_wrappers['chart'] = ChartImageExtractorWrapper(self.project_config)
        self.processor_wrappers['language'] = LanguageConfidenceDetectorWrapper(self.project_config)
        self.processor_wrappers['mt_detector'] = MachineTranslationDetectorWrapper(self.project_config)
        self.processor_wrappers['financial'] = FinancialSymbolProcessorWrapper(self.project_config)

    def connect_signals(self):
        # Connect PDF processor signals
        pdf_wrapper = self.processor_wrappers['pdf']
        pdf_wrapper.progress_updated.connect(self.pdf_progress_bar.setValue)
        pdf_wrapper.status_updated.connect(self.pdf_status.setText)
        pdf_wrapper.batch_completed.connect(self.on_pdf_batch_completed)
        
        self.pdf_start_btn.clicked.connect(self.start_pdf_processing)
        self.pdf_stop_btn.clicked.connect(self.stop_pdf_processing)
        
        # Connect Text processor signals
        text_wrapper = self.processor_wrappers['text']
        text_wrapper.progress_updated.connect(self.text_progress_bar.setValue)
        text_wrapper.status_updated.connect(self.text_status.setText)
        text_wrapper.batch_completed.connect(self.on_text_batch_completed)
        
        self.text_start_btn.clicked.connect(self.start_text_processing)
        self.text_stop_btn.clicked.connect(self.stop_text_processing)
        
        # Connect other processor signals similarly
        # ...

    def add_pdf_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select PDF Files", "", "PDF Files (*.pdf)"
        )
        if files:
            for file in files:
                self.pdf_file_list.addItem(file)

    def clear_pdf_files(self):
        self.pdf_file_list.clear()

    def add_text_files(self):
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select Text Files", "", 
            "Text Files (*.txt *.html *.htm *.docx *.doc *.md *.csv *.json *.xml)"
        )
        if files:
            for file in files:
                self.text_file_list.addItem(file)

    def clear_text_files(self):
        self.text_file_list.clear()

    def select_input_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Input Directory", ""
        )
        if directory:
            self.input_dir_path.setText(directory)

    def start_pdf_processing(self):
        pdf_wrapper = self.processor_wrappers['pdf']
        
        # Get files from list
        files_to_process = []
        for i in range(self.pdf_file_list.count()):
            files_to_process.append(self.pdf_file_list.item(i).text())
        
        if not files_to_process:
            self.pdf_status.setText("Error: No files to process")
            return
        
        # Configure processor
        pdf_wrapper.set_ocr_enabled(self.ocr_enabled.isChecked())
        pdf_wrapper.set_table_extraction(self.table_extraction.isChecked())
        pdf_wrapper.set_formula_extraction(self.formula_extraction.isChecked())
        pdf_wrapper.set_worker_threads(self.pdf_threads.value())
        
        # Update UI
        self.pdf_start_btn.setEnabled(False)
        self.pdf_stop_btn.setEnabled(True)
        
        # Start processing
        pdf_wrapper.start_batch_processing(files_to_process)

    def stop_pdf_processing(self):
        self.processor_wrappers['pdf'].stop()
        self.pdf_start_btn.setEnabled(True)
        self.pdf_stop_btn.setEnabled(False)

    def start_text_processing(self):
        text_wrapper = self.processor_wrappers['text']
        
        # Get files from list
        files_to_process = []
        for i in range(self.text_file_list.count()):
            files_to_process.append(self.text_file_list.item(i).text())
        
        if not files_to_process:
            self.text_status.setText("Error: No files to process")
            return
        
        # Configure processor
        text_wrapper.set_language_detection(self.language_detection.isChecked())
        text_wrapper.set_quality_threshold(self.quality_threshold.value())
        text_wrapper.set_worker_threads(self.text_threads.value())
        
        # Update UI
        self.text_start_btn.setEnabled(False)
        self.text_stop_btn.setEnabled(True)
        
        # Start processing
        text_wrapper.start_batch_processing(files_to_process)

    def stop_text_processing(self):
        self.processor_wrappers['text'].stop()
        self.text_start_btn.setEnabled(True)
        self.text_stop_btn.setEnabled(False)
    
    def apply_advanced_processing(self):
        # Enable/disable processors based on UI selections
        self.processor_wrappers['deduplicator'].set_enabled(
            self.enable_deduplication.isChecked()
        )
        self.processor_wrappers['domain'].set_enabled(
            self.enable_domain_classification.isChecked()
        )
        self.processor_wrappers['financial'].set_enabled(
            self.enable_financial_symbols.isChecked()
        )
        self.processor_wrappers['language'].set_enabled(
            self.enable_language_confidence.isChecked()
        )
        self.processor_wrappers['mt_detector'].set_enabled(
            self.enable_mt_detection.isChecked()
        )
        
        # Start a complex batch operation that applies multiple processors
        self.advanced_status.setText("Starting advanced processing...")
        self.advanced_progress_bar.setValue(0)
        
        # TODO: Implement complex batch processing with multiple processors
        # For now, just simulate a basic operation
        self.advanced_status.setText("Advanced processing in progress...")
        
        # This would be done with proper processing in the real implementation
        self.advanced_progress_bar.setValue(100)
        self.advanced_status.setText("Advanced processing completed")

    def start_batch_processing(self):
        input_dir = self.input_dir_path.text()
        if input_dir == "Not selected" or not os.path.isdir(input_dir):
            self.batch_status.setText("Error: Invalid input directory")
            return
        
        # Configure batch processing
        recursive = self.recursive_processing.isChecked()
        thread_count = self.batch_threads.value()
        
        # Determine file types to process
        file_types = []
        if self.process_pdf.isChecked():
            file_types.append(".pdf")
        if self.process_text.isChecked():
            file_types.append(".txt")
        if self.process_docx.isChecked():
            file_types.append(".docx")
        if self.process_html.isChecked():
            file_types.extend([".html", ".htm"])
        
        if not file_types:
            self.batch_status.setText("Error: No file types selected")
            return
        
        # Collect files to process
        files_to_process = []
        for root, dirs, files in os.walk(input_dir):
            if not recursive and root != input_dir:
                continue
                
            for file in files:
                file_ext = os.path.splitext(file)[1].lower()
                if file_ext in file_types:
                    files_to_process.append(os.path.join(root, file))
        
        if not files_to_process:
            self.batch_status.setText("Error: No matching files found")
            return
        
        # Update UI
        self.batch_start_btn.setEnabled(False)
        self.batch_stop_btn.setEnabled(True)
        self.batch_status.setText(f"Processing {len(files_to_process)} files...")
        
        # Start batch processing
        # In a real implementation, you'd determine the appropriate processor for each file
        # For now, just simulate a batch process
        
        # Categorize files by type
        pdf_files = [f for f in files_to_process if f.lower().endswith('.pdf')]
        text_files = [f for f in files_to_process if not f.lower().endswith('.pdf')]
        
        # Process PDFs with PDF processor
        if pdf_files:
            pdf_wrapper = self.processor_wrappers['pdf']
            pdf_wrapper.set_worker_threads(thread_count)
            pdf_wrapper.start_batch_processing(pdf_files)
        
        # Process text files with text processor
        if text_files:
            text_wrapper = self.processor_wrappers['text']
            text_wrapper.set_worker_threads(thread_count)
            text_wrapper.start_batch_processing(text_files)
            
        # Real implementation would coordinate these processes better

    def stop_batch_processing(self):
        # Stop all active processors
        for wrapper in self.processor_wrappers.values():
            wrapper.stop()
        
        # Update UI
        self.batch_start_btn.setEnabled(True)
        self.batch_stop_btn.setEnabled(False)
        self.batch_status.setText("Batch processing stopped")

    @pyqtSlot(dict)
    def on_pdf_batch_completed(self, results):
        self.pdf_start_btn.setEnabled(True)
        self.pdf_stop_btn.setEnabled(False)
        
        # Update status
        success_count = results.get('success_count', 0)
        fail_count = results.get('fail_count', 0)
        
        message = f"PDF processing completed: {success_count} successes, {fail_count} failures"
        self.pdf_status.setText(message)
        self.processing_status_label.setText(message)

    @pyqtSlot(dict)
    def on_text_batch_completed(self, results):
        self.text_start_btn.setEnabled(True)
        self.text_stop_btn.setEnabled(False)
        
        # Update status
        success_count = results.get('success_count', 0)
        fail_count = results.get('fail_count', 0)
        
        message = f"Text processing completed: {success_count} successes, {fail_count} failures"
        self.text_status.setText(message)
        self.processing_status_label.setText(message)

    def stop_all_processors(self):
        for wrapper in self.processor_wrappers.values():
            wrapper.stop()
            
        # Reset UI elements
        self.pdf_start_btn.setEnabled(True)
        self.pdf_stop_btn.setEnabled(False)
        self.text_start_btn.setEnabled(True)
        self.text_stop_btn.setEnabled(False)
        self.batch_start_btn.setEnabled(True)
        self.batch_stop_btn.setEnabled(False)
        
        self.processing_status_label.setText("All processors stopped")
