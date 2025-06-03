from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QSplitter, 
                             QTreeView, QGroupBox, QTextEdit, QPushButton, 
                             QLabel, QLineEdit, QFileDialog, QComboBox,
                             QTableView, QHeaderView, QMenu, QMessageBox)
from PyQt6.QtCore import Qt, QDir, QFileSystemModel, QSortFilterProxyModel, QModelIndex, pyqtSlot, QPoint
from PyQt6.QtGui import QAction, QStandardItemModel, QStandardItem
import os
import json

class CorpusManagerTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Create a splitter for file browser and metadata panel
        splitter = QSplitter(Qt.Orientation.Horizontal)
        
        # Left side: File browser
        file_browser_widget = QWidget()
        file_browser_layout = QVBoxLayout(file_browser_widget)
        
        # Search bar
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for files...")
        self.search_input.textChanged.connect(self.filter_files)
        search_layout.addWidget(self.search_input)
        
        # Domain filter
        search_layout.addWidget(QLabel("Domain:"))
        self.domain_filter = QComboBox()
        self.domain_filter.addItem("All Domains")
        # Add the 8 domain categories from your project requirements
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
        self.domain_filter.addItems(domains)
        self.domain_filter.currentIndexChanged.connect(self.filter_files)
        search_layout.addWidget(self.domain_filter)
        
        file_browser_layout.addLayout(search_layout)
        
        # File system navigation
        nav_layout = QHBoxLayout()
        self.path_input = QLineEdit()
        self.path_input.setReadOnly(True)
        nav_layout.addWidget(self.path_input)
        
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_directory)
        nav_layout.addWidget(self.browse_btn)
        
        file_browser_layout.addLayout(nav_layout)
        
        # File tree view
        self.file_model = QFileSystemModel()
        self.file_model.setReadOnly(False)
        
        # Proxy model for filtering
        self.proxy_model = QSortFilterProxyModel()
        self.proxy_model.setSourceModel(self.file_model)
        self.proxy_model.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        
        self.file_tree = QTreeView()
        self.file_tree.setModel(self.proxy_model)
        self.file_tree.setSortingEnabled(True)
        self.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree.customContextMenuRequested.connect(self.show_context_menu)
        self.file_tree.clicked.connect(self.on_file_selected)
        
        # Hide unnecessary columns
        self.file_tree.setColumnHidden(1, True)  # Size
        self.file_tree.setColumnHidden(2, True)  # Type
        self.file_tree.setColumnHidden(3, True)  # Date modified
        
        file_browser_layout.addWidget(self.file_tree)
        
        # Add controls at the bottom
        controls_layout = QHBoxLayout()
        self.create_folder_btn = QPushButton("Create Folder")
        self.create_folder_btn.clicked.connect(self.create_folder)
        controls_layout.addWidget(self.create_folder_btn)
        
        self.refresh_btn = QPushButton("Refresh")
        self.refresh_btn.clicked.connect(self.refresh_file_view)
        controls_layout.addWidget(self.refresh_btn)
        
        file_browser_layout.addLayout(controls_layout)
        
        # Right side: Metadata panel
        metadata_widget = QWidget()
        metadata_layout = QVBoxLayout(metadata_widget)
        
        # File info
        file_info_group = QGroupBox("File Information")
        file_info_layout = QVBoxLayout(file_info_group)
        
        self.file_name_label = QLabel("No file selected")
        self.file_path_label = QLabel("")
        self.file_type_label = QLabel("")
        self.file_size_label = QLabel("")
        
        file_info_layout.addWidget(self.file_name_label)
        file_info_layout.addWidget(self.file_path_label)
        file_info_layout.addWidget(self.file_type_label)
        file_info_layout.addWidget(self.file_size_label)
        
        metadata_layout.addWidget(file_info_group)
        
        # Metadata viewer/editor
        metadata_group = QGroupBox("Metadata")
        metadata_inner_layout = QVBoxLayout(metadata_group)
        
        # Use a table view for structured metadata display and editing
        self.metadata_table = QTableView()
        self.metadata_model = QStandardItemModel(0, 2)
        self.metadata_model.setHorizontalHeaderLabels(["Property", "Value"])
        self.metadata_table.setModel(self.metadata_model)
        
        # Make the table more user-friendly
        self.metadata_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self.metadata_table.verticalHeader().setVisible(False)
        
        metadata_inner_layout.addWidget(self.metadata_table)
        
        # Metadata control buttons
        metadata_buttons_layout = QHBoxLayout()
        self.save_metadata_btn = QPushButton("Save Metadata")
        self.save_metadata_btn.clicked.connect(self.save_metadata)
        self.save_metadata_btn.setEnabled(False)
        metadata_buttons_layout.addWidget(self.save_metadata_btn)
        
        self.add_metadata_btn = QPushButton("Add Field")
        self.add_metadata_btn.clicked.connect(self.add_metadata_field)
        self.add_metadata_btn.setEnabled(False)
        metadata_buttons_layout.addWidget(self.add_metadata_btn)
        
        metadata_inner_layout.addLayout(metadata_buttons_layout)
        
        metadata_layout.addWidget(metadata_group)
        
        # Content preview
        preview_group = QGroupBox("Content Preview")
        preview_layout = QVBoxLayout(preview_group)
        
        self.content_preview = QTextEdit()
        self.content_preview.setReadOnly(True)
        preview_layout.addWidget(self.content_preview)
        
        metadata_layout.addWidget(preview_group)
        
        # Add both panels to the splitter
        splitter.addWidget(file_browser_widget)
        splitter.addWidget(metadata_widget)
        
        # Set initial sizes (30% for file browser, 70% for metadata)
        splitter.setSizes([300, 700])
        
        main_layout.addWidget(splitter)
        
        # Try to set default directory to the corpus root
        try:
            corpus_root = self.project_config.get_corpus_root()
            if os.path.isdir(corpus_root):
                self.set_root_directory(corpus_root)
            else:
                # Fallback to documents folder
                docs_path = QDir.homePath() + "/Documents"
                self.set_root_directory(docs_path)
        except Exception as e:
            print(f"Error setting root directory: {e}")
            # Just use home directory as fallback
            self.set_root_directory(QDir.homePath())
            
    def set_root_directory(self, path):
        self.file_model.setRootPath(path)
        self.path_input.setText(path)
        
        # Set the root index correctly in the proxy model
        source_index = self.file_model.index(path)
        proxy_index = self.proxy_model.mapFromSource(source_index)
        self.file_tree.setRootIndex(proxy_index)
    
    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(
            self, "Select Directory", self.path_input.text()
        )
        if directory:
            self.set_root_directory(directory)
    
    def filter_files(self):
        # Get filter text
        filter_text = self.search_input.text()
        
        # If domain filter is not "All Domains", add it to the filter text
        if self.domain_filter.currentIndex() > 0:
            domain = self.domain_filter.currentText()
            if filter_text:
                filter_text = f"{filter_text} {domain}"
            else:
                filter_text = domain
        
        self.proxy_model.setFilterFixedString(filter_text)
    
    def refresh_file_view(self):
        current_path = self.path_input.text()
        self.set_root_directory(current_path)
    
    def create_folder(self):
        current_path = self.path_input.text()
        
        # Get folder name from user
        folder_name, ok = QInputDialog.getText(
            self, "Create Folder", "Enter folder name:"
        )
        
        if ok and folder_name:
            new_folder_path = os.path.join(current_path, folder_name)
            try:
                os.makedirs(new_folder_path, exist_ok=True)
                self.refresh_file_view()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Could not create folder: {str(e)}"
                )
    
    def on_file_selected(self, index):
        # Convert from proxy model index to file model index
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.file_model.filePath(source_index)
        
        if os.path.isfile(file_path):
            # Update file info
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_type = os.path.splitext(file_name)[1]
            
            self.file_name_label.setText(f"Name: {file_name}")
            self.file_path_label.setText(f"Path: {file_path}")
            self.file_type_label.setText(f"Type: {file_type}")
            self.file_size_label.setText(f"Size: {self.format_size(file_size)}")
            
            # Enable metadata buttons
            self.save_metadata_btn.setEnabled(True)
            self.add_metadata_btn.setEnabled(True)
            
            # Load metadata if available
            self.load_metadata(file_path)
            
            # Load content preview
            self.load_content_preview(file_path)
    
    def format_size(self, size_bytes):
        """Format file size in a human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.2f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.2f} TB"
    
    def load_metadata(self, file_path):
        """Load metadata for the selected file"""
        # Clear existing metadata
        self.metadata_model.setRowCount(0)
        
        # Check for metadata file
        metadata_path = self.get_metadata_path(file_path)
        
        if os.path.exists(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                
                # Populate the table with metadata
                for key, value in metadata.items():
                    self.add_metadata_row(key, value)
            except Exception as e:
                print(f"Error loading metadata: {e}")
        else:
            # If no metadata file exists, add some default fields
            default_fields = [
                ("title", ""),
                ("author", ""),
                ("year", ""),
                ("domain", ""),
                ("quality_score", ""),
                ("language", ""),
                ("source", "")
            ]
            for key, value in default_fields:
                self.add_metadata_row(key, value)
    
    def add_metadata_row(self, key, value):
        """Add a row to the metadata table"""
        row = self.metadata_model.rowCount()
        self.metadata_model.insertRow(row)
        self.metadata_model.setItem(row, 0, QStandardItem(key))
        self.metadata_model.setItem(row, 1, QStandardItem(str(value)))
    
    def add_metadata_field(self):
        """Add a new metadata field"""
        row = self.metadata_model.rowCount()
        self.metadata_model.insertRow(row)
        self.metadata_model.setItem(row, 0, QStandardItem("new_field"))
        self.metadata_model.setItem(row, 1, QStandardItem(""))
    
    def save_metadata(self):
        """Save metadata for the current file"""
        # Get current file
        index = self.file_tree.currentIndex()
        if not index.isValid():
            return
            
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.file_model.filePath(source_index)
        
        if not os.path.isfile(file_path):
            return
            
        # Collect metadata from the table
        metadata = {}
        for row in range(self.metadata_model.rowCount()):
            key = self.metadata_model.item(row, 0).text()
            value = self.metadata_model.item(row, 1).text()
            metadata[key] = value
        
        # Save to metadata file
        metadata_path = self.get_metadata_path(file_path)
        
        try:
            # Ensure metadata directory exists
            os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
            
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
                
            QMessageBox.information(
                self, "Success", "Metadata saved successfully"
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error", f"Could not save metadata: {str(e)}"
            )
    
    def get_metadata_path(self, file_path):
        """Get the path to the metadata file for a given file"""
        # In a real implementation, this would follow your project's metadata storage convention
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        
        # Store metadata in a parallel structure
        metadata_dir = os.path.join(file_dir, ".metadata")
        return os.path.join(metadata_dir, f"{base_name}.json")
    
    def load_content_preview(self, file_path):
        """Load a preview of the file content"""
        # Clear existing preview
        self.content_preview.clear()
        
        # Check file extension
        _, ext = os.path.splitext(file_path)
        ext = ext.lower()
        
        try:
            # Handle different file types
            if ext in ['.txt', '.md', '.csv', '.json']:
                # Text files - read directly
                with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                    # Read first 5000 chars for preview
                    content = f.read(5000)
                    self.content_preview.setPlainText(content)
            elif ext == '.pdf':
                self.content_preview.setPlainText("PDF content preview not available")
            elif ext in ['.docx', '.doc']:
                self.content_preview.setPlainText("Word document preview not available")
            else:
                self.content_preview.setPlainText(f"Preview not available for {ext} files")
        except Exception as e:
            self.content_preview.setPlainText(f"Error loading preview: {str(e)}")
    
    def show_context_menu(self, position):
        """Show context menu for file tree"""
        index = self.file_tree.indexAt(position)
        if not index.isValid():
            return
            
        source_index = self.proxy_model.mapToSource(index)
        file_path = self.file_model.filePath(source_index)
        
        menu = QMenu()
        
        open_action = QAction("Open", self)
        open_action.triggered.connect(lambda: self.open_file(file_path))
        menu.addAction(open_action)
        
        if os.path.isdir(file_path):
            # Directory-specific actions
            create_folder_action = QAction("Create Folder", self)
            create_folder_action.triggered.connect(self.create_folder)
            menu.addAction(create_folder_action)
        else:
            # File-specific actions
            edit_metadata_action = QAction("Edit Metadata", self)
            edit_metadata_action.triggered.connect(lambda: self.on_file_selected(index))
            menu.addAction(edit_metadata_action)
            
            process_action = QAction("Process File", self)
            process_action.triggered.connect(lambda: self.process_file(file_path))
            menu.addAction(process_action)
        
        # Common actions
        menu.addSeparator()
        
        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_file(file_path))
        menu.addAction(delete_action)
        
        menu.exec(self.file_tree.viewport().mapToGlobal(position))
    
    def open_file(self, file_path):
        """Open file with default application"""
        # Use QDesktopServices to open file with system default program
        from PyQt6.QtGui import QDesktopServices
        from PyQt6.QtCore import QUrl
        
        QDesktopServices.openUrl(QUrl.fromLocalFile(file_path))
    
    def delete_file(self, file_path):
        """Delete file or directory"""
        confirm = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {os.path.basename(file_path)}?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                if os.path.isdir(file_path):
                    import shutil
                    shutil.rmtree(file_path)
                else:
                    os.remove(file_path)
                    
                # Also remove metadata if it exists
                metadata_path = self.get_metadata_path(file_path)
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)
                    
                self.refresh_file_view()
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Could not delete: {str(e)}"
                )
    
    def process_file(self, file_path):
        """Process the selected file"""
        # This would typically dispatch to the appropriate processor
        # based on the file type
        
        # For now, just show a message
        QMessageBox.information(
            self, "Process File",
            f"Processing {os.path.basename(file_path)}...\n"
            "This would call the appropriate processor wrapper."
        )
