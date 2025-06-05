from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QPushButton, QComboBox, QDateEdit,
                             QGridLayout, QSpinBox, QCheckBox, QSlider, QFrame)
from PySide6.QtCore import Qt, QDate, Slot as pyqtSlot
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter, QColor
from app.helpers.chart_manager import ChartManager

import random
import datetime


class AnalyticsTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.chart_manager = ChartManager('dark')  # Will be updated based on actual theme
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Analytics Filters header (restored as requested)
        filters_header = QLabel("Analytics Filters")
        filters_header.setObjectName("analytics-filters-header")
        filters_header.setStyleSheet("font-size: 16px; font-weight: 600; color: #32B8C6; margin-bottom: 8px;")
        main_layout.addWidget(filters_header)
        
        # Filter bar with improved spacing and layout (moved down to create separation)
        filter_group = QGroupBox()  # Remove text to eliminate gray background behind header
        filter_group.setObjectName("filter_group")
        filter_layout = QHBoxLayout(filter_group)
        filter_layout.setContentsMargins(20, 16, 20, 12)  # More right padding as requested
        filter_layout.setSpacing(12)  # Better spacing between elements
        
        # Date range filter with smaller, left-aligned controls
        date_label = QLabel("From:")
        date_label.setMinimumWidth(40)
        filter_layout.addWidget(date_label)
        
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-3))
        self.date_from.setMaximumWidth(85)  # Even smaller as requested
        filter_layout.addWidget(self.date_from)
        
        to_label = QLabel("To:")
        to_label.setMinimumWidth(25)
        filter_layout.addWidget(to_label)
        
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        self.date_to.setMaximumWidth(85)  # Even smaller as requested
        filter_layout.addWidget(self.date_to)
        
        # Add larger spacer to push domain selector further away from dates
        filter_layout.addSpacing(30)
        
        # Domain filter with even more space allocation
        domain_label = QLabel("Domain:")
        domain_label.setMinimumWidth(50)
        filter_layout.addWidget(domain_label)
        
        self.domain_filter = QComboBox()
        self.domain_filter.addItem("All Domains")
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
        self.domain_filter.setMinimumWidth(240)  # Even more space for domain selector
        filter_layout.addWidget(self.domain_filter)
        
        # Quality filter
        quality_label = QLabel("Min Quality:")
        quality_label.setMinimumWidth(75)
        filter_layout.addWidget(quality_label)
        
        self.quality_filter = QSpinBox()
        self.quality_filter.setRange(0, 100)
        self.quality_filter.setValue(0)
        self.quality_filter.setMaximumWidth(80)
        filter_layout.addWidget(self.quality_filter)
        
        # Apply button
        self.apply_filters_btn = QPushButton("Apply Filters")
        self.apply_filters_btn.clicked.connect(self.update_charts)
        self.apply_filters_btn.setMinimumWidth(120)
        filter_layout.addWidget(self.apply_filters_btn)
        
        main_layout.addWidget(filter_group)
        
        # Consolidated headers bar with dark gray background
        headers_bar = QFrame()
        headers_bar.setObjectName("analytics-headers-bar")
        headers_bar.setStyleSheet("""
            QFrame#analytics-headers-bar {
                background-color: #2D2F31;
                border-radius: 8px;
                padding: 12px;
                margin: 8px 0px;
            }
        """)
        
        headers_layout = QGridLayout(headers_bar)
        headers_layout.setSpacing(16)
        
        # Create consolidated headers with dark gray backgrounds
        domain_header = QLabel("Corpus Domain Distribution")
        domain_header.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px; padding: 8px 12px; background-color: #2D2F31; border-radius: 6px;")
        headers_layout.addWidget(domain_header, 0, 0)
        
        quality_header = QLabel("Document Quality by Domain / Quality Score")
        quality_header.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px; padding: 8px 12px; background-color: #2D2F31; border-radius: 6px;")
        headers_layout.addWidget(quality_header, 0, 1)
        
        time_header = QLabel("Document Collection Over Time / Document Count")
        time_header.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px; padding: 8px 12px; background-color: #2D2F31; border-radius: 6px;")
        headers_layout.addWidget(time_header, 1, 0)
        
        lang_header = QLabel("Language Distribution / Language Count")
        lang_header.setStyleSheet("color: #FFFFFF; font-weight: 600; font-size: 14px; padding: 8px 12px; background-color: #2D2F31; border-radius: 6px;")
        headers_layout.addWidget(lang_header, 1, 1)
        
        main_layout.addWidget(headers_bar)
        
        # Modern 2x2 grid layout for charts without individual headers
        charts_grid = QGridLayout()
        charts_grid.setSpacing(16)
        charts_grid.setContentsMargins(8, 8, 8, 8)
        
        # Create chart containers WITHOUT headers (charts only, bigger size)
        self.domain_chart_container = self.create_chart_container_no_header(
            self.create_domain_distribution_chart()
        )
        self.quality_chart_container = self.create_chart_container_no_header(
            self.create_quality_metrics_chart()
        )
        self.time_chart_container = self.create_chart_container_no_header(
            self.create_time_trends_chart()
        )
        self.lang_chart_container = self.create_chart_container_no_header(
            self.create_language_chart()
        )
        
        # Add to grid: 2x2 layout
        charts_grid.addWidget(self.domain_chart_container, 0, 0)    # Top-left
        charts_grid.addWidget(self.quality_chart_container, 0, 1)   # Top-right
        charts_grid.addWidget(self.time_chart_container, 1, 0)      # Bottom-left
        charts_grid.addWidget(self.lang_chart_container, 1, 1)      # Bottom-right
        
        # Set equal column and row stretch
        charts_grid.setColumnStretch(0, 1)
        charts_grid.setColumnStretch(1, 1)
        charts_grid.setRowStretch(0, 1)
        charts_grid.setRowStretch(1, 1)
        
        # Create container widget for the grid
        charts_container = QWidget()
        charts_container.setLayout(charts_grid)
        main_layout.addWidget(charts_container)
        
        # Update charts with initial data
        self.update_charts()
    
    def update_theme(self, theme_name):
        """Update the chart manager theme and refresh charts"""
        self.chart_manager.set_theme(theme_name)
        self.update_charts()
    
    def create_chart_container_no_header(self, chart_view):
        """Create a chart container without header to maximize chart space"""
        container = QFrame()
        container.setObjectName("card")
        container.setFrameShape(QFrame.Shape.Box)
        container.setLineWidth(1)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(8, 8, 8, 8)  # Minimal margins for bigger charts
        layout.setSpacing(0)
        
        # Chart view takes full space
        chart_view.setMinimumSize(450, 350)  # Bigger charts to fill space
        layout.addWidget(chart_view)
        
        return container
    
    def create_chart_container(self, title, chart_view, subtitle=None):
        """Create a styled container for a chart with modern consolidated title"""
        container = QFrame()
        container.setObjectName("card")
        container.setFrameShape(QFrame.Shape.Box)
        container.setLineWidth(1)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(16, 12, 16, 16)
        layout.setSpacing(8)
        
        # Simple title (no more consolidated format)
        title_label = QLabel(title)
        title_label.setObjectName("card__header")
        layout.addWidget(title_label)
        
        # Chart view
        chart_view.setMinimumSize(400, 300)
        layout.addWidget(chart_view)
        
        return container
    
    def create_domain_distribution_chart(self):
        # Create a pie chart for domain distribution using ChartManager with bigger size
        chart_view = self.chart_manager.create_chart_view("Corpus Domain Distribution")
        self.domain_chart = chart_view  # Store reference for updates
        return chart_view
    
    def create_quality_metrics_chart(self):
        # Create a bar chart for quality metrics using ChartManager
        chart_view = self.chart_manager.create_chart_view("Document Quality by Domain")
        self.quality_chart = chart_view  # Store reference for updates
        return chart_view
    
    def create_time_trends_chart(self):
        # Create a line chart for time trends using ChartManager
        chart_view = self.chart_manager.create_chart_view("Document Collection Over Time")
        self.time_chart = chart_view  # Store reference for updates
        return chart_view
    
    def create_language_chart(self):
        # Create a bar chart for language distribution using ChartManager
        chart_view = self.chart_manager.create_chart_view("Language Distribution")
        self.lang_chart = chart_view  # Store reference for updates
        return chart_view
    
    def update_charts(self):
        """Update all analytics charts with current data"""
        # Get filter values
        from_date = self.date_from.date().toPython()
        to_date = self.date_to.date().toPython()
        domain = self.domain_filter.currentText()
        min_quality = self.quality_filter.value()
        
        # In a real implementation, this would fetch and analyze actual corpus data
        # For demonstration, we'll use simulated data
        
        self.update_domain_distribution_chart(domain, min_quality)
        self.update_quality_metrics_chart(domain, min_quality)
        self.update_time_trends_chart(from_date, to_date, domain)
        self.update_language_chart(domain, min_quality)
    
    def update_domain_distribution_chart(self, domain_filter, min_quality):
        """Update the domain distribution pie chart"""
        # Get the chart
        chart_view = self.domain_chart
        chart = chart_view.chart()
        
        # Clear existing series
        chart.removeAllSeries()
        
        # Create a new pie series
        series = QPieSeries()
        
        # Simulated domain distribution data
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
        
        # If a specific domain is selected, only show that one
        if domain_filter != "All Domains":
            domains = [domain_filter]
        
        # Simulated counts
        counts = [
            320,  # Crypto Derivatives
            180,  # High Frequency Trading
            175,  # Risk Management
            160,  # Market Microstructure
            200,  # DeFi
            100,  # Portfolio Construction
            75,   # Valuation Models
            40    # Regulation & Compliance
        ]
        
        # Add slices to the pie series with improved styling and colors
        for domain, count in zip(domains, counts):
            if domain_filter == "All Domains" or domain == domain_filter:
                slice_obj = series.append(f"{domain} ({count})", count)
                slice_obj.setLabelVisible(True)
                
                # Apply consistent domain colors from ChartManager
                slice_obj.setColor(self.chart_manager.get_domain_color(domain))
                
                # Add white borders for better definition (same as dashboard)
                slice_obj.setBorderColor(QColor(255, 255, 255))
                slice_obj.setBorderWidth(2)
                
                # Set label color to white for better contrast
                slice_obj.setLabelColor(QColor(255, 255, 255))
                # Note: Label position will use default positioning for compatibility
        
        chart.addSeries(series)
        
        # Hide legend to make pie circle bigger as requested
        legend = chart.legend()
        legend.setVisible(False)
        
        # Update chart title
        title = "Corpus Domain Distribution"
        if domain_filter != "All Domains":
            title = f"Domain: {domain_filter}"
        if min_quality > 0:
            title += f" (Quality >= {min_quality})"
        chart.setTitle(title)
    
    def update_quality_metrics_chart(self, domain_filter, min_quality):
        """Update the quality metrics bar chart"""
        # Get the chart
        chart_view = self.quality_chart
        chart = chart_view.chart()
        
        # Clear existing series
        chart.removeAllSeries()
        chart.removeAxis(chart.axisX())
        chart.removeAxis(chart.axisY())
        
        # Create a new bar series
        series = QBarSeries()
        
        # Simulated domain quality data
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
        
        # If a specific domain is selected, only show that one
        if domain_filter != "All Domains":
            domains = [domain_filter]
        
        # Simulated quality metrics (average quality score per domain)
        quality_scores = [
            85,  # Crypto Derivatives
            78,  # High Frequency Trading
            82,  # Risk Management
            75,  # Market Microstructure
            88,  # DeFi
            90,  # Portfolio Construction
            83,  # Valuation Models
            79   # Regulation & Compliance
        ]
        
        # Create a bar set for quality scores with consistent colors
        quality_set = QBarSet("Average Quality Score")
        
        # Add values to the bar set
        filtered_domains = []
        for domain, score in zip(domains, quality_scores):
            if domain_filter == "All Domains" or domain == domain_filter:
                filtered_domains.append(domain)
                if score >= min_quality:
                    quality_set.append(score)
                else:
                    # If below min quality, still show but with lower value
                    quality_set.append(min_quality)
        
        # Use orange for top right position as requested - harmonious with pie chart colors
        quality_set.setColor(QColor("#E68161"))  # Orange matching the pie chart
        series.append(quality_set)
        chart.addSeries(series)
        
        # Apply white legend text for better contrast
        legend = chart.legend()
        if legend:
            legend.setLabelColor(QColor(255, 255, 255))  # White text for maximum contrast
        
        # Set up the axes
        axis_x = QBarCategoryAxis()
        axis_x.append(domains if domain_filter == "All Domains" else [domain_filter])
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        axis_y.setRange(min_quality, 100)
        axis_y.setTitleText("Quality Score")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        # Update chart title
        title = "Document Quality by Domain"
        if domain_filter != "All Domains":
            title = f"Quality for Domain: {domain_filter}"
        if min_quality > 0:
            title += f" (Min: {min_quality})"
        chart.setTitle(title)
    
    def update_time_trends_chart(self, from_date, to_date, domain_filter):
        """Update the time trends chart"""
        # Get the chart
        chart_view = self.time_chart
        chart = chart_view.chart()
        
        # Clear existing series
        chart.removeAllSeries()
        chart.removeAxis(chart.axisX())
        chart.removeAxis(chart.axisY())
        
        # Create a new bar series
        series = QBarSeries()
        
        # Simulated time series data - document counts by month
        # Generate 6 months of data
        months = []
        current_date = datetime.date.today()
        for i in range(5, -1, -1):
            month_date = current_date - datetime.timedelta(days=i*30)
            months.append(month_date.strftime("%b %Y"))
        
        # Generate simulated document counts for each month
        # Using random but with a trend
        document_counts = []
        base_count = 100  # Starting point
        for i in range(6):
            # Increasing trend with some randomness
            count = base_count + i*20 + random.randint(-10, 10)
            document_counts.append(count)
        
        # Create a bar set for document counts with harmonious color
        count_set = QBarSet("Document Count")
        count_set.setColor(QColor("#26A69A"))  # Medium teal that works well with brand
        
        # Add values to the bar set
        for count in document_counts:
            count_set.append(count)
        
        series.append(count_set)
        chart.addSeries(series)
        
        # Apply white legend text for better contrast
        legend = chart.legend()
        if legend:
            legend.setLabelColor(QColor(255, 255, 255))  # White text for maximum contrast
        
        # Set up the axes
        axis_x = QBarCategoryAxis()
        axis_x.append(months)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        max_count = max(document_counts) + 20  # Add some padding
        axis_y.setRange(0, max_count)
        axis_y.setTitleText("Document Count")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        # Update chart title
        title = "Document Collection Over Time"
        if domain_filter != "All Domains":
            title += f" - {domain_filter}"
        chart.setTitle(title)
    
    def update_language_chart(self, domain_filter, min_quality):
        """Update the language distribution chart"""
        # Get the chart
        chart_view = self.lang_chart
        chart = chart_view.chart()
        
        # Clear existing series
        chart.removeAllSeries()
        chart.removeAxis(chart.axisX())
        chart.removeAxis(chart.axisY())
        
        # Create a new bar series
        series = QBarSeries()
        
        # Simulated language distribution data
        languages = ["English", "Chinese", "Spanish", "French", "German", "Japanese", "Russian"]
        
        # Simulated language counts
        language_counts = [850, 150, 100, 50, 40, 30, 30]  # Total: 1250
        
        # Create a bar set for language counts with harmonious color
        lang_set = QBarSet("Document Count")
        
        # Use purple for bottom right position as requested - same tones as pie chart
        lang_set.setColor(QColor("#B45BCF"))  # Purple matching the pie chart Valuation Models
        
        # Add values to the bar set
        for count in language_counts:
            # Apply domain filter (this is simulated - in real implementation would filter actual data)
            filtered_count = count
            if domain_filter != "All Domains":
                # Simulate domain filtering by reducing counts
                filtered_count = int(count * 0.3)  # Just an example
            lang_set.append(filtered_count)
        
        series.append(lang_set)
        chart.addSeries(series)
        
        # Apply white legend text for better contrast
        legend = chart.legend()
        if legend:
            legend.setLabelColor(QColor(255, 255, 255))  # White text for maximum contrast
        
        # Set up the axes
        axis_x = QBarCategoryAxis()
        axis_x.append(languages)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axis_x)
        
        axis_y = QValueAxis()
        max_count = max(language_counts) + 50  # Add some padding
        axis_y.setRange(0, max_count)
        axis_y.setTitleText("Document Count")
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axis_y)
        
        # Update chart title
        title = "Language Distribution"
        if domain_filter != "All Domains":
            title += f" - {domain_filter}"
        if min_quality > 0:
            title += f" (Quality >= {min_quality})"
        chart.setTitle(title)
