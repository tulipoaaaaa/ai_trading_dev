from PySide6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, 
                             QLabel, QPushButton, QComboBox, QDateEdit,
                             QTabWidget, QSpinBox, QCheckBox, QSlider)
from PySide6.QtCore import Qt, QDate, Slot as pyqtSlot
from PySide6.QtCharts import QChart, QChartView, QPieSeries, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PySide6.QtGui import QPainter

import random
import datetime


class AnalyticsTab(QWidget):
    def __init__(self, project_config, parent=None):
        super().__init__(parent)
        self.project_config = project_config
        self.setup_ui()
        
    def setup_ui(self):
        main_layout = QVBoxLayout(self)
        
        # Filter bar
        filter_group = QGroupBox("Analytics Filters")
        filter_layout = QHBoxLayout(filter_group)
        
        # Date range filter
        filter_layout.addWidget(QLabel("From:"))
        self.date_from = QDateEdit()
        self.date_from.setDate(QDate.currentDate().addMonths(-3))
        filter_layout.addWidget(self.date_from)
        
        filter_layout.addWidget(QLabel("To:"))
        self.date_to = QDateEdit()
        self.date_to.setDate(QDate.currentDate())
        filter_layout.addWidget(self.date_to)
        
        # Domain filter
        filter_layout.addWidget(QLabel("Domain:"))
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
        filter_layout.addWidget(self.domain_filter)
        
        # Quality filter
        filter_layout.addWidget(QLabel("Min Quality:"))
        self.quality_filter = QSpinBox()
        self.quality_filter.setRange(0, 100)
        self.quality_filter.setValue(0)
        filter_layout.addWidget(self.quality_filter)
        
        # Apply button
        self.apply_filters_btn = QPushButton("Apply Filters")
        self.apply_filters_btn.clicked.connect(self.update_charts)
        filter_layout.addWidget(self.apply_filters_btn)
        
        main_layout.addWidget(filter_group)
        
        # Analytics tabs
        self.analytics_tabs = QTabWidget()
        
        # Distribution tab
        dist_tab = QWidget()
        dist_layout = QVBoxLayout(dist_tab)
        
        # Domain distribution chart
        self.domain_chart = self.create_domain_distribution_chart()
        dist_layout.addWidget(self.domain_chart)
        
        self.analytics_tabs.addTab(dist_tab, "Domain Distribution")
        
        # Quality metrics tab
        quality_tab = QWidget()
        quality_layout = QVBoxLayout(quality_tab)
        
        # Quality metrics chart
        self.quality_chart = self.create_quality_metrics_chart()
        quality_layout.addWidget(self.quality_chart)
        
        self.analytics_tabs.addTab(quality_tab, "Quality Metrics")
        
        # Time trends tab
        time_tab = QWidget()
        time_layout = QVBoxLayout(time_tab)
        
        # Time trends chart
        self.time_chart = self.create_time_trends_chart()
        time_layout.addWidget(self.time_chart)
        
        self.analytics_tabs.addTab(time_tab, "Time Trends")
        
        # Language analysis tab
        lang_tab = QWidget()
        lang_layout = QVBoxLayout(lang_tab)
        
        # Language chart
        self.lang_chart = self.create_language_chart()
        lang_layout.addWidget(self.lang_chart)
        
        self.analytics_tabs.addTab(lang_tab, "Language Analysis")
        
        main_layout.addWidget(self.analytics_tabs)
        
        # Update charts with initial data
        self.update_charts()
    
    def create_domain_distribution_chart(self):
        # Create a pie chart for domain distribution
        chart = QChart()
        chart.setTitle("Corpus Domain Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Create a chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        return chart_view
    
    def create_quality_metrics_chart(self):
        # Create a bar chart for quality metrics
        chart = QChart()
        chart.setTitle("Document Quality by Domain")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Create a chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        return chart_view
    
    def create_time_trends_chart(self):
        # Create a line chart for time trends
        chart = QChart()
        chart.setTitle("Document Collection Over Time")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Create a chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        return chart_view
    
    def create_language_chart(self):
        # Create a bar chart for language distribution
        chart = QChart()
        chart.setTitle("Language Distribution")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)
        
        # Create a chart view
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)
        
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
        
        # Add slices to the pie series
        for domain, count in zip(domains, counts):
            if domain_filter == "All Domains" or domain == domain_filter:
                slice = series.append(domain, count)
                slice.setLabelVisible(True)
        
        chart.addSeries(series)
        
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
        
        # Create a bar set for quality scores
        quality_set = QBarSet("Average Quality Score")
        
        # Add values to the bar set
        for domain, score in zip(domains, quality_scores):
            if domain_filter == "All Domains" or domain == domain_filter:
                if score >= min_quality:
                    quality_set.append(score)
                else:
                    # If below min quality, still show but with lower value
                    quality_set.append(min_quality)
        
        series.append(quality_set)
        chart.addSeries(series)
        
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
        
        # Create a bar set for document counts
        count_set = QBarSet("Document Count")
        
        # Add values to the bar set
        for count in document_counts:
            count_set.append(count)
        
        series.append(count_set)
        chart.addSeries(series)
        
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
        
        # Create a bar set for language counts
        lang_set = QBarSet("Document Count")
        
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
