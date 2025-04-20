# collapsible_panel.py
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QFrame, QGraphicsDropShadowEffect, QSizePolicy
)
from PyQt6.QtGui import QColor, QFont, QPainter, QBrush, QPixmap
from PyQt6.QtCore import Qt, QPropertyAnimation, QEasingCurve, QSize, pyqtSignal


class CollapsiblePanel(QWidget):
    """A collapsible panel widget that can be expanded and collapsed."""

    # Signal emitted when panel is expanded/collapsed
    expanded = pyqtSignal(bool)

    def __init__(self, title, parent=None, expanded=True, panel_color="rgba(30, 30, 40, 180)"):
        super().__init__(parent)

        # Main properties
        self.is_expanded = expanded
        self.panel_color = panel_color
        self.animation_duration = 300

        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        # Header frame
        self.header_frame = QFrame()
        self.header_frame.setObjectName("headerFrame")
        self.header_frame.setCursor(Qt.CursorShape.PointingHandCursor)
        self.header_frame.setMinimumHeight(40)
        self.header_frame.setMaximumHeight(40)

        # Header layout
        header_layout = QHBoxLayout(self.header_frame)
        header_layout.setContentsMargins(10, 5, 10, 5)

        # Header title
        self.title_label = QLabel(title)
        self.title_label.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))

        # Arrow indicator
        self.arrow_label = QLabel()
        self.arrow_label.setFixedSize(20, 20)

        # Add widgets to header layout
        header_layout.addWidget(self.title_label, 1)
        header_layout.addWidget(self.arrow_label, 0)

        # Content widget - container for user content
        self.content_frame = QFrame()
        self.content_frame.setObjectName("contentFrame")
        self.content_frame.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Content layout
        self.content_layout = QVBoxLayout(self.content_frame)
        self.content_layout.setContentsMargins(10, 0, 10, 10)

        # Add header and content to main layout
        self.main_layout.addWidget(self.header_frame)
        self.main_layout.addWidget(self.content_frame)

        # Animation
        self.animation = QPropertyAnimation(
            self.content_frame, b"maximumHeight")
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        self.animation.setDuration(self.animation_duration)

        # Connect signals/slots
        self.header_frame.mousePressEvent = self.toggle_expanded

        # Initial state
        self.update_styles()
        self.set_expanded(expanded, False)

    def toggle_expanded(self, event=None):
        """Toggle between expanded and collapsed state."""
        self.set_expanded(not self.is_expanded)

    def set_expanded(self, expanded, animate=True):
        """Set the expansion state with animation option."""
        self.is_expanded = expanded

        if not animate:
            # Set state without animation
            if expanded:
                self.content_frame.setMaximumHeight(
                    16777215)  # QWIDGETSIZE_MAX
            else:
                self.content_frame.setMaximumHeight(0)
            self.update_styles()
            self.expanded.emit(expanded)
            return

        # Setup animation based on target state
        if expanded:
            self.content_frame.setMaximumHeight(0)  # Start from collapsed
            self.animation.setStartValue(0)
            # Calculate content size
            content_height = self.content_layout.sizeHint().height() + 20
            self.animation.setEndValue(content_height)
        else:
            content_height = self.content_frame.height()
            self.animation.setStartValue(content_height)
            self.animation.setEndValue(0)

        # Start animation
        self.animation.start()

        # Update arrow and styles
        self.update_styles()

        # Emit signal
        self.expanded.emit(expanded)

    def update_styles(self):
        """Update styles based on current state."""
        # Update arrow
        self.arrow_label.setText("▼" if self.is_expanded else "►")

        # Update styles
        self.header_frame.setStyleSheet(f"""
            #headerFrame {{
                background-color: {self.panel_color};
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                border-bottom-left-radius: {0 if self.is_expanded else 8}px;
                border-bottom-right-radius: {0 if self.is_expanded else 8}px;
                border: 1px solid rgba(80, 80, 100, 100);
            }}
        """)

        self.content_frame.setStyleSheet(f"""
            #contentFrame {{
                background-color: {self.panel_color};
                border-bottom-left-radius: 8px;
                border-bottom-right-radius: 8px;
                border-left: 1px solid rgba(80, 80, 100, 100);
                border-right: 1px solid rgba(80, 80, 100, 100);
                border-bottom: 1px solid rgba(80, 80, 100, 100);
            }}
        """)

    def add_widget(self, widget):
        """Add a widget to the content layout."""
        self.content_layout.addWidget(widget)

    def add_layout(self, layout):
        """Add a layout to the content layout."""
        self.content_layout.addLayout(layout)

    def update_panel_color(self, color):
        """Update the panel color."""
        self.panel_color = color
        self.update_styles()
