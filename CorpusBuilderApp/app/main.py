"""
CryptoFinance Corpus Builder v3 - Main Application Entry Point
"""

import sys
import os
import logging
from pathlib import Path
from PyQt6.QtWidgets import QApplication, QMessageBox
from PyQt6.QtCore import QDir, QStandardPaths
from PyQt6.QtGui import QIcon
import traceback
import json

# Add shared_tools to path for imports
current_dir = Path(__file__).parent.parent
sys.path.insert(0, str(current_dir))

from main_window import CryptoCorpusMainWindow
from shared_tools.project_config import ProjectConfig
from app.helpers.theme_manager import ThemeManager

THEME_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'theme_config.json')

def load_user_theme():
    if os.path.exists(THEME_CONFIG_PATH):
        try:
            with open(THEME_CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('theme', 'light')
        except Exception:
            return 'light'
    return 'light'

def save_user_theme(theme):
    try:
        with open(THEME_CONFIG_PATH, 'w', encoding='utf-8') as f:
            json.dump({'theme': theme}, f)
    except Exception:
        pass

def load_user_sound_setting():
    if os.path.exists(THEME_CONFIG_PATH):
        try:
            with open(THEME_CONFIG_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('sound_enabled', True)
        except Exception:
            return True
    return True

class CryptoCorpusApp(QApplication):
    """Main application class"""
    
    def __init__(self, argv):
        super().__init__(argv)
        
        # Set application properties
        self.setApplicationName("CryptoFinance Corpus Builder")
        self.setApplicationVersion("3.0")
        self.setOrganizationName("CryptoFinance Research")
        self.setOrganizationDomain("cryptofinance.org")
        
        # Setup logging
        self.setup_logging()
        
        # Setup exception handling
        sys.excepthook = self.handle_exception
        
        # Create main window
        try:
            self.main_window = None
            self.init_config()
            self.create_main_window()
        except Exception as e:
            self.show_error("Initialization Error", f"Failed to initialize application: {e}")
            sys.exit(1)
    
    def setup_logging(self):
        """Setup application logging"""
        log_dir = Path.home() / ".cryptofinance" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / "app.log"),
                logging.StreamHandler(sys.stdout)
            ]
        )
        
        self.logger = logging.getLogger("CryptoCorpusApp")
        self.logger.info("Application starting...")
    
    def init_config(self):
        """Initialize project configuration"""
        try:
            # Look for config files in common locations
            config_locations = [
                Path.cwd() / "shared_tools" / "master_config.yaml",
                Path.cwd() / "shared_tools" / "test_config.yaml",
                Path.home() / ".cryptofinance" / "config.yaml"
            ]
            
            config_path = None
            for location in config_locations:
                if location.exists():
                    config_path = location
                    break
            
            if not config_path:
                # Create default config if none found
                config_path = self.create_default_config()
            
            self.config = ProjectConfig(str(config_path), environment='test')
            self.logger.info(f"Loaded configuration from: {config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            raise
    
    def create_default_config(self):
        """Create a default configuration file"""
        config_dir = Path.home() / ".cryptofinance"
        config_dir.mkdir(parents=True, exist_ok=True)
        
        config_path = config_dir / "config.yaml"
        
        default_config = {
            'environment': 'test',
            'environments': {
                'test': {
                    'corpus_dir': str(config_dir / 'corpus'),
                    'cache_dir': str(config_dir / 'cache'),
                    'log_dir': str(config_dir / 'logs')
                },
                'production': {
                    'corpus_dir': str(Path.home() / 'CryptoCorpus'),
                    'cache_dir': str(Path.home() / 'CryptoCorpus' / 'cache'),
                    'log_dir': str(Path.home() / 'CryptoCorpus' / 'logs')
                }
            }
        }
        
        import yaml
        with open(config_path, 'w') as f:
            yaml.dump(default_config, f, default_flow_style=False)
        
        return config_path
    
    def create_main_window(self):
        """Create and show the main window"""
        self.main_window = CryptoCorpusMainWindow(self.config)
        self.main_window.show()
        
        # Center window on screen
        self.main_window.center_on_screen()
        
        self.logger.info("Main window created and shown")
    
    def handle_exception(self, exc_type, exc_value, exc_traceback):
        """Handle uncaught exceptions"""
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return
        
        error_msg = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        self.logger.error(f"Uncaught exception: {error_msg}")
        
        self.show_error("Unexpected Error", 
                       f"An unexpected error occurred:\n\n{exc_value}\n\nSee logs for details.")
    
    def show_error(self, title, message):
        """Show error dialog"""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Critical)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()

def main():
    """Main entry point"""
    # Enable high DPI scaling
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        QApplication.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
    
    app = CryptoCorpusApp(sys.argv)

    # Load and apply theme from config
    user_theme = load_user_theme()
    ThemeManager.apply_theme(user_theme)

    # Connect settings dialog to save theme changes
    def on_settings_updated(settings):
        theme = settings.get('theme', None)
        if theme:
            save_user_theme(theme.lower())
    if hasattr(app, 'main_window') and hasattr(app.main_window, 'settings_dialog'):
        app.main_window.settings_dialog.settings_updated.connect(on_settings_updated)
    # If settings dialog is created dynamically, ensure this connection is made after creation.

    sound_enabled = load_user_sound_setting()

    # Run the application
    exit_code = app.exec()
    
    # Cleanup
    logging.getLogger("CryptoCorpusApp").info("Application exiting...")
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
