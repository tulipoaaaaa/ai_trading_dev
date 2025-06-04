# File: app/ui/corpus_manager_enhancements.py

from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QPushButton, QCheckBox, QTableWidget, QTableWidgetItem,
                             QProgressBar, QMessageBox, QInputDialog, QHeaderView,
                             QMenu, QDialog, QFormLayout, QLineEdit, QTextEdit,
                             QDialogButtonBox, QLabel)
from PyQt6.QtCore import Qt, pyqtSignal, QThread, QMimeData, QUrl, QTimer
from PyQt6.QtGui import QDragEnterEvent, QDropEvent, QAction
import os
import json
import shutil
from typing import List, Dict, Any

class NotificationManager(QWidget):
    """Advanced notification system for long-running tasks."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.active_notifications = {}
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the notification UI."""
        layout = QVBoxLayout(self)
        
        # Header
        header = QLabel("System Notifications")
        header.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        layout.addWidget(header)
        
        # Notification area
        self.notification_area = QVBoxLayout()
        layout.addLayout(self.notification_area)
        
        # Clear all button
        self.clear_btn = QPushButton("Clear All")
        self.clear_btn.clicked.connect(self.clear_all_notifications)
        layout.addWidget(self.clear_btn)
        
    def add_notification(self, notification_id: str, title: str, message: str, 
                        notification_type: str = "info", auto_hide: bool = False):
        """Add a new notification."""
        notification_widget = NotificationWidget(
            notification_id, title, message, notification_type, auto_hide
        )
        notification_widget.dismissed.connect(self.remove_notification)
        
        self.notification_area.addWidget(notification_widget)
        self.active_notifications[notification_id] = notification_widget
        
        if auto_hide:
            QTimer.singleShot(5000, lambda: self.remove_notification(notification_id))
            
    def update_notification(self, notification_id: str, message: str, progress: int = None):
        """Update an existing notification."""
        if notification_id in self.active_notifications:
            notification = self.active_notifications[notification_id]
            notification.update_message(message)
            if progress is not None:
                notification.update_progress(progress)
                
    def remove_notification(self, notification_id: str):
        """Remove a notification."""
        if notification_id in self.active_notifications:
            widget = self.active_notifications[notification_id]
            self.notification_area.removeWidget(widget)
            widget.deleteLater()
            del self.active_notifications[notification_id]
            
    def clear_all_notifications(self):
        """Clear all notifications."""
        for notification_id in list(self.active_notifications.keys()):
            self.remove_notification(notification_id)

class NotificationWidget(QWidget):
    """Individual notification widget."""
    
    dismissed = pyqtSignal(str)  # notification_id
    
    def __init__(self, notification_id: str, title: str, message: str, 
                 notification_type: str = "info", auto_hide: bool = False):
        super().__init__()
        self.notification_id = notification_id
        self.setup_ui(title, message, notification_type)
        
    def setup_ui(self, title: str, message: str, notification_type: str):
        """Set up the notification widget UI."""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Color coding based on type
        colors = {
            "info": "#e3f2fd",
            "success": "#e8f5e8",
            "warning": "#fff3cd",
            "error": "#f8d7da"
        }
        
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {colors.get(notification_type, colors['info'])};
                border: 1px solid #ccc;
                border-radius: 4px;
                margin: 2px;
            }}
        """)
        
        # Content area
        content_layout = QVBoxLayout()
        
        # Title
        title_label = QLabel(title)
        title_label.setStyleSheet("font-weight: bold;")
        content_layout.addWidget(title_label)
        
        # Message
        self.message_label = QLabel(message)
        self.message_label.setWordWrap(True)
        content_layout.addWidget(self.message_label)
        
        # Progress bar (initially hidden)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        content_layout.addWidget(self.progress_bar)
        
        layout.addLayout(content_layout, 1)
        
        # Dismiss button
        dismiss_btn = QPushButton("✖")
        dismiss_btn.setMaximumSize(20, 20)
        dismiss_btn.clicked.connect(self.dismiss)
        layout.addWidget(dismiss_btn, 0, Qt.AlignmentFlag.AlignTop)
        
    def update_message(self, message: str):
        """Update the notification message."""
        self.message_label.setText(message)
        
    def update_progress(self, progress: int):
        """Update the progress bar."""
        self.progress_bar.setVisible(True)
        self.progress_bar.setValue(progress)
        
    def dismiss(self):
        """Dismiss this notification."""
        self.dismissed.emit(self.notification_id)

class BatchMetadataEditor(QDialog):
    """Dialog for batch editing metadata."""
    
    def __init__(self, file_paths: List[str], parent=None):
        super().__init__(parent)
        self.file_paths = file_paths
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the batch metadata editor UI."""
        self.setWindowTitle(f"Batch Edit Metadata ({len(self.file_paths)} files)")
        self.setMinimumSize(500, 400)
        
        layout = QVBoxLayout(self)
        
        # Instructions
        instructions = QLabel(f"Edit metadata for {len(self.file_paths)} selected files. "
                             "Leave fields empty to skip updating that field.")
        instructions.setWordWrap(True)
        layout.addWidget(instructions)
        
        # Metadata fields
        form_layout = QFormLayout()
        
        self.domain_edit = QLineEdit()
        form_layout.addRow("Domain:", self.domain_edit)
        
        self.author_edit = QLineEdit()
        form_layout.addRow("Author:", self.author_edit)
        
        self.year_edit = QLineEdit()
        form_layout.addRow("Year:", self.year_edit)
        
        self.source_edit = QLineEdit()
        form_layout.addRow("Source:", self.source_edit)
        
        self.tags_edit = QLineEdit()
        self.tags_edit.setPlaceholderText("Comma-separated tags")
        form_layout.addRow("Tags:", self.tags_edit)
        
        self.notes_edit = QTextEdit()
        self.notes_edit.setMaximumHeight(100)
        form_layout.addRow("Notes:", self.notes_edit)
        
        layout.addLayout(form_layout)
        
        # Options
        options_group = QGroupBox("Options")
        options_layout = QVBoxLayout(options_group)
        
        self.overwrite_cb = QCheckBox("Overwrite existing values")
        self.overwrite_cb.setChecked(False)
        options_layout.addWidget(self.overwrite_cb)
        
        self.backup_cb = QCheckBox("Create backup of original metadata")
        self.backup_cb.setChecked(True)
        options_layout.addWidget(self.backup_cb)
        
        layout.addWidget(options_group)
        
        # Buttons
        button_box = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | 
            QDialogButtonBox.StandardButton.Cancel
        )
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)
        
    def get_metadata_updates(self) -> Dict[str, Any]:
        """Get the metadata updates from the form."""
        updates = {}
        
        if self.domain_edit.text().strip():
            updates['domain'] = self.domain_edit.text().strip()
            
        if self.author_edit.text().strip():
            updates['author'] = self.author_edit.text().strip()
            
        if self.year_edit.text().strip():
            updates['year'] = self.year_edit.text().strip()
            
        if self.source_edit.text().strip():
            updates['source'] = self.source_edit.text().strip()
            
        if self.tags_edit.text().strip():
            tags = [tag.strip() for tag in self.tags_edit.text().split(',')]
            updates['tags'] = tags
            
        if self.notes_edit.toPlainText().strip():
            updates['notes'] = self.notes_edit.toPlainText().strip()
            
        return updates
        
    def should_overwrite(self) -> bool:
        """Check if existing values should be overwritten."""
        return self.overwrite_cb.isChecked()
        
    def should_backup(self) -> bool:
        """Check if backups should be created."""
        return self.backup_cb.isChecked()

class BatchOperationsManager(QWidget):
    """Manager for batch operations on corpus files."""
    
    operation_started = pyqtSignal(str, int)  # operation_name, total_items
    operation_progress = pyqtSignal(str, int)  # operation_name, current_item
    operation_completed = pyqtSignal(str, dict)  # operation_name, results
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the batch operations UI."""
        layout = QVBoxLayout(self)
        
        # Operations group
        operations_group = QGroupBox("Batch Operations")
        operations_layout = QVBoxLayout(operations_group)
        
        # File operations
        file_ops_layout = QHBoxLayout()
        
        self.copy_btn = QPushButton("Copy Selected")
        self.copy_btn.clicked.connect(self.copy_selected_files)
        file_ops_layout.addWidget(self.copy_btn)
        
        self.move_btn = QPushButton("Move Selected")
        self.move_btn.clicked.connect(self.move_selected_files)
        file_ops_layout.addWidget(self.move_btn)
        
        self.delete_btn = QPushButton("Delete Selected")
        self.delete_btn.clicked.connect(self.delete_selected_files)
        file_ops_layout.addWidget(self.delete_btn)
        
        operations_layout.addLayout(file_ops_layout)
        
        # Metadata operations
        metadata_ops_layout = QHBoxLayout()
        
        self.edit_metadata_btn = QPushButton("Edit Metadata")
        self.edit_metadata_btn.clicked.connect(self.edit_selected_metadata)
        metadata_ops_layout.addWidget(self.edit_metadata_btn)
        
        self.export_metadata_btn = QPushButton("Export Metadata")
        self.export_metadata_btn.clicked.connect(self.export_metadata)
        metadata_ops_layout.addWidget(self.export_metadata_btn)
        
        self.validate_btn = QPushButton("Validate Files")
        self.validate_btn.clicked.connect(self.validate_selected_files)
        metadata_ops_layout.addWidget(self.validate_btn)
        
        operations_layout.addLayout(metadata_ops_layout)
        
        layout.addWidget(operations_group)
        
        # Selection info
        self.selection_info = QLabel("No files selected")
        layout.addWidget(self.selection_info)
        
        # Progress area
        self.progress_area = QVBoxLayout()
        layout.addLayout(self.progress_area)
        
        self.selected_files = []
        
    def set_selected_files(self, file_paths: List[str]):
        """Set the currently selected files."""
        self.selected_files = file_paths
        count = len(file_paths)
        self.selection_info.setText(f"{count} file{'s' if count != 1 else ''} selected")
        
        # Enable/disable buttons based on selection
        has_selection = count > 0
        self.copy_btn.setEnabled(has_selection)
        self.move_btn.setEnabled(has_selection)
        self.delete_btn.setEnabled(has_selection)
        self.edit_metadata_btn.setEnabled(has_selection)
        self.export_metadata_btn.setEnabled(has_selection)
        self.validate_btn.setEnabled(has_selection)
        
    def copy_selected_files(self):
        """Copy selected files to a destination."""
        if not self.selected_files:
            return
            
        from PyQt6.QtWidgets import QFileDialog
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        
        if destination:
            self.operation_started.emit("copy", len(self.selected_files))
            
            # Start copy operation in background
            worker = FileOperationWorker("copy", self.selected_files, destination)
            worker.progress.connect(lambda i: self.operation_progress.emit("copy", i))
            worker.completed.connect(lambda r: self.operation_completed.emit("copy", r))
            worker.start()
            
    def move_selected_files(self):
        """Move selected files to a destination."""
        if not self.selected_files:
            return
            
        from PyQt6.QtWidgets import QFileDialog
        destination = QFileDialog.getExistingDirectory(self, "Select Destination")
        
        if destination:
            reply = QMessageBox.question(
                self, "Confirm Move",
                f"Are you sure you want to move {len(self.selected_files)} files?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            if reply == QMessageBox.StandardButton.Yes:
                self.operation_started.emit("move", len(self.selected_files))
                
                worker = FileOperationWorker("move", self.selected_files, destination)
                worker.progress.connect(lambda i: self.operation_progress.emit("move", i))
                worker.completed.connect(lambda r: self.operation_completed.emit("move", r))
                worker.start()
                
    def delete_selected_files(self):
        """Delete selected files."""
        if not self.selected_files:
            return
            
        reply = QMessageBox.question(
            self, "Confirm Delete",
            f"Are you sure you want to delete {len(self.selected_files)} files? This cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.operation_started.emit("delete", len(self.selected_files))
            
            worker = FileOperationWorker("delete", self.selected_files)
            worker.progress.connect(lambda i: self.operation_progress.emit("delete", i))
            worker.completed.connect(lambda r: self.operation_completed.emit("delete", r))
            worker.start()
            
    def edit_selected_metadata(self):
        """Edit metadata for selected files."""
        if not self.selected_files:
            return
            
        dialog = BatchMetadataEditor(self.selected_files, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            updates = dialog.get_metadata_updates()
            if updates:
                self.operation_started.emit("metadata_edit", len(self.selected_files))
                
                worker = MetadataOperationWorker(
                    "edit", self.selected_files, updates,
                    dialog.should_overwrite(), dialog.should_backup()
                )
                worker.progress.connect(lambda i: self.operation_progress.emit("metadata_edit", i))
                worker.completed.connect(lambda r: self.operation_completed.emit("metadata_edit", r))
                worker.start()
                
    def export_metadata(self):
        """Export metadata for selected files."""
        if not self.selected_files:
            return
            
        from PyQt6.QtWidgets import QFileDialog
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Export Metadata", "", "JSON Files (*.json);;CSV Files (*.csv)"
        )
        
        if file_path:
            self.operation_started.emit("metadata_export", len(self.selected_files))
            
            worker = MetadataOperationWorker("export", self.selected_files, file_path)
            worker.progress.connect(lambda i: self.operation_progress.emit("metadata_export", i))
            worker.completed.connect(lambda r: self.operation_completed.emit("metadata_export", r))
            worker.start()
            
    def validate_selected_files(self):
        """Validate selected files."""
        if not self.selected_files:
            return
            
        self.operation_started.emit("validate", len(self.selected_files))
        
        worker = FileOperationWorker("validate", self.selected_files)
        worker.progress.connect(lambda i: self.operation_progress.emit("validate", i))
        worker.completed.connect(lambda r: self.operation_completed.emit("validate", r))
        worker.start()

class FileOperationWorker(QThread):
    """Worker thread for file operations."""
    
    progress = pyqtSignal(int)
    completed = pyqtSignal(dict)
    
    def __init__(self, operation: str, file_paths: List[str], destination: str = None):
        super().__init__()
        self.operation = operation
        self.file_paths = file_paths
        self.destination = destination
        
    def run(self):
        """Run the file operation."""
        results = {"success": [], "failed": []}
        
        for i, file_path in enumerate(self.file_paths):
            try:
                if self.operation == "copy":
                    dest_path = os.path.join(self.destination, os.path.basename(file_path))
                    shutil.copy2(file_path, dest_path)
                elif self.operation == "move":
                    dest_path = os.path.join(self.destination, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                elif self.operation == "delete":
                    os.remove(file_path)
                elif self.operation == "validate":
                    # Simple validation - check if file exists and is readable
                    if os.path.exists(file_path) and os.access(file_path, os.R_OK):
                        results["success"].append(file_path)
                    else:
                        results["failed"].append((file_path, "File not accessible"))
                        continue
                
                if self.operation != "validate":
                    results["success"].append(file_path)
                    
            except Exception as e:
                results["failed"].append((file_path, str(e)))
                
            self.progress.emit(i + 1)
            
        self.completed.emit(results)

class MetadataOperationWorker(QThread):
    """Worker thread for metadata operations."""
    
    progress = pyqtSignal(int)
    completed = pyqtSignal(dict)
    
    def __init__(self, operation: str, file_paths: List[str], 
                 data: Any = None, overwrite: bool = False, backup: bool = False):
        super().__init__()
        self.operation = operation
        self.file_paths = file_paths
        self.data = data
        self.overwrite = overwrite
        self.backup = backup
        
    def run(self):
        """Run the metadata operation."""
        results = {"success": [], "failed": []}
        
        if self.operation == "export":
            self._export_metadata(results)
        elif self.operation == "edit":
            self._edit_metadata(results)
            
        self.completed.emit(results)
        
    def _export_metadata(self, results):
        """Export metadata to file."""
        try:
            all_metadata = {}
            
            for i, file_path in enumerate(self.file_paths):
                try:
                    metadata_path = self._get_metadata_path(file_path)
                    if os.path.exists(metadata_path):
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                        all_metadata[file_path] = metadata
                        results["success"].append(file_path)
                    else:
                        results["failed"].append((file_path, "No metadata file found"))
                        
                except Exception as e:
                    results["failed"].append((file_path, str(e)))
                    
                self.progress.emit(i + 1)
                
            # Write to export file
            with open(self.data, 'w') as f:
                if self.data.endswith('.json'):
                    json.dump(all_metadata, f, indent=2)
                else:  # CSV
                    # Simple CSV export
                    import csv
                    writer = csv.writer(f)
                    writer.writerow(["File", "Domain", "Author", "Year", "Source"])
                    for file_path, metadata in all_metadata.items():
                        writer.writerow([
                            file_path,
                            metadata.get('domain', ''),
                            metadata.get('author', ''),
                            metadata.get('year', ''),
                            metadata.get('source', '')
                        ])
                        
        except Exception as e:
            results["failed"].append(("Export operation", str(e)))
            
    def _edit_metadata(self, results):
        """Edit metadata for files."""
        for i, file_path in enumerate(self.file_paths):
            try:
                metadata_path = self._get_metadata_path(file_path)
                
                # Load existing metadata
                metadata = {}
                if os.path.exists(metadata_path):
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        
                    # Create backup if requested
                    if self.backup:
                        backup_path = metadata_path + '.backup'
                        shutil.copy2(metadata_path, backup_path)
                
                # Update metadata
                for key, value in self.data.items():
                    if self.overwrite or key not in metadata:
                        metadata[key] = value
                        
                # Ensure metadata directory exists
                os.makedirs(os.path.dirname(metadata_path), exist_ok=True)
                
                # Save updated metadata
                with open(metadata_path, 'w') as f:
                    json.dump(metadata, f, indent=2)
                    
                results["success"].append(file_path)
                
            except Exception as e:
                results["failed"].append((file_path, str(e)))
                
            self.progress.emit(i + 1)
            
    def _get_metadata_path(self, file_path):
        """Get the metadata file path for a given file."""
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        base_name = os.path.splitext(file_name)[0]
        
        # Store metadata in a parallel structure
        metadata_dir = os.path.join(file_dir, ".metadata")
        return os.path.join(metadata_dir, f"{base_name}.json")
