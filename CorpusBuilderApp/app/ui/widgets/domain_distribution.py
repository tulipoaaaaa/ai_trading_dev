# File: app/ui/widgets/domain_distribution.py

from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QCheckBox)
from PySide6.QtCore import Qt, Signal as pyqtSignal
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QColor, QPainter

class DomainDistribution(QWidget):
    """Widget for displaying corpus domain distribution."""
    
    refresh_requested = pyqtSignal()
    balance_requested = pyqtSignal()
    
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.setup_ui()
        
    def setup_ui(self):
        """Set up the UI components."""
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Controls layout
        controls_layout = QHBoxLayout()
        
        # Chart type selector
        controls_layout.addWidget(QLabel("Chart Type:"))
        self.chart_type = QComboBox()
        self.chart_type.addItems(["Pie Chart", "Bar Chart"])
        self.chart_type.currentTextChanged.connect(self.update_chart_type)
        controls_layout.addWidget(self.chart_type)
        
        # Compare with target option
        self.show_target = QCheckBox("Compare with Target")
        self.show_target.setChecked(True)
        self.show_target.stateChanged.connect(self.update_chart)
        controls_layout.addWidget(self.show_target)
        
        # Add stretch to push buttons to the right
        controls_layout.addStretch()
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.refresh_requested)
        controls_layout.addWidget(refresh_btn)
        
        # Balance button
        balance_btn = QPushButton("Balance Corpus")
        balance_btn.clicked.connect(self.balance_requested)
        controls_layout.addWidget(balance_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Chart view
        self.chart = QChart()
        self.chart.setTitle("Corpus Domain Distribution")
        self.chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        main_layout.addWidget(self.chart_view)
        
        # Initial data (placeholder)
        self.domains = [
            "Crypto Derivatives", 
            "High Frequency Trading",
            "Risk Management",
            "Market Microstructure",
            "DeFi",
            "Portfolio Construction",
            "Valuation Models",
            "Regulation & Compliance"
        ]
        
        self.current_distribution = {
            "Crypto Derivatives": 25,
            "High Frequency Trading": 15,
            "Risk Management": 15,
            "Market Microstructure": 12,
            "DeFi": 15,
            "Portfolio Construction": 8,
            "Valuation Models": 5,
            "Regulation & Compliance": 5
        }
        
        self.target_distribution = {
            "Crypto Derivatives": {"allocation": 0.20},
            "High Frequency Trading": {"allocation": 0.15},
            "Risk Management": {"allocation": 0.15},
            "Market Microstructure": {"allocation": 0.15},
            "DeFi": {"allocation": 0.12},
            "Portfolio Construction": {"allocation": 0.10},
            "Valuation Models": {"allocation": 0.08},
            "Regulation & Compliance": {"allocation": 0.05},
        }
        
        # Initial chart
        self.update_chart()
    
    def update_distribution_data(self, current_distribution, target_distribution=None):
        """Update the distribution data and refresh the chart."""
        self.current_distribution = current_distribution
        if target_distribution:
            self.target_distribution = target_distribution
        
        self.update_chart()
    
    def update_chart_type(self):
        """Update the chart type based on selection."""
        self.update_chart()
    
    def update_chart(self):
        """Update the chart with current data."""
        # Clear existing series
        self.chart.removeAllSeries()
        if self.chart.axisX():
            self.chart.removeAxis(self.chart.axisX())
        if self.chart.axisY():
            self.chart.removeAxis(self.chart.axisY())
        
        if self.chart_type.currentText() == "Pie Chart":
            self._create_pie_chart()
        else:
            self._create_bar_chart()
    
    def _create_pie_chart(self):
        """Create and display a pie chart."""
        # Create pie series for current distribution
        series = QPieSeries()
        
        # Set chart title
        self.chart.setTitle("Current Corpus Domain Distribution")
        
        # Add slices
        for domain, data in self.current_distribution.items():
            # Handle both integer values and dictionary values
            if isinstance(data, dict):
                value = data.get("current", 0) * 100  # Convert to percentage
            else:
                # data is just an integer percentage
                value = data
                
            slice = series.append(f"{domain} ({value:.1f}%)", value)
            slice.setLabelVisible(True)
            
            # Color based on comparison with target
            target_data = self.target_distribution.get(domain, {})
            if isinstance(target_data, dict):
                target = target_data.get("allocation", 0) * 100
            else:
                target = target_data if target_data else 0
                
            if self.show_target.isChecked():
                if abs(value - target) <= 2:
                    # On target (±2%)
                    slice.setColor(QColor("green"))
                elif value < target:
                    # Below target
                    slice.setColor(QColor("orange"))
                else:
                    # Above target
                    slice.setColor(QColor("blue"))
        
        self.chart.addSeries(series)
    
    def _create_bar_chart(self):
        """Create and display a bar chart."""
        # Create bar series for current distribution
        current_set = QBarSet("Current")
        
        # Add target set if requested
        if self.show_target.isChecked():
            target_set = QBarSet("Target")
            self.chart.setTitle("Current vs Target Domain Distribution")
        else:
            self.chart.setTitle("Current Domain Distribution")
        
        # Add data
        for domain in self.domains:
            current_data = self.current_distribution.get(domain, {})
            # Handle both integer values and dictionary values
            if isinstance(current_data, dict):
                current_value = current_data.get("current", 0) * 100
            else:
                # current_data is just an integer percentage
                current_value = current_data if current_data else 0
                
            current_set.append(current_value)
            
            if self.show_target.isChecked():
                target_data = self.target_distribution.get(domain, {})
                if isinstance(target_data, dict):
                    target_value = target_data.get("allocation", 0) * 100
                else:
                    target_value = target_data if target_data else 0
                target_set.append(target_value)
        
        # Create and configure bar series
        series = QBarSeries()
        series.append(current_set)
        if self.show_target.isChecked():
            series.append(target_set)
        
        self.chart.addSeries(series)
        
        # Add axes
        axis_x = QBarCategoryAxis()
        axis_x.append(self.domains)
        self.chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(0, 100)  # Adjust range as needed for percentage
        axis_y.setTitleText("Percentage (%)")
        self.chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
