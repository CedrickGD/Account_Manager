# enhanced_buttons.py
from PyQt6.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QLabel
from PyQt6.QtGui import QColor, QFont, QIcon
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QEasingCurve, pyqtProperty, QRect, QTimer


class EnhancedButton(QPushButton):
    """An enhanced button with modern styling and animation effects."""

    def __init__(self, text="", parent=None, icon=None, style="primary"):
        super().__init__(text, parent)

        # Properties
        self.style_type = style
        self.hovered = False
        self.pressed = False

        # Style colors - can be overridden
        self.colors = {
            "primary": {
                "base": "#8A2BE2",  # Blueviolet
                "hover": "#9A3BF2",
                "pressed": "#7A1BD2",
                "text": "#FFFFFF"
            },
            "secondary": {
                "base": "#6c5ce7",  # Secondary color
                "hover": "#7c6cf7",
                "pressed": "#5c4cd7",
                "text": "#FFFFFF"
            },
            "success": {
                "base": "#50FA7B",  # Success color
                "hover": "#70FF9B",
                "pressed": "#40EA6B",
                "text": "#121218"
            },
            "danger": {
                "base": "#FF5555",  # Danger color
                "hover": "#FF6E6E",
                "pressed": "#E64C4C",
                "text": "#FFFFFF"
            },
            "info": {
                "base": "#8BE9FD",  # Info color
                "hover": "#A5F0FF",
                "pressed": "#75D9ED",
                "text": "#121218"
            }
        }

        # Set icon if provided
        if icon:
            self.setIcon(icon)
            self.setIconSize(QSize(20, 20))

        # Default colors based on style
        self._base_color = self.colors[style]["base"]
        self._hover_color = self.colors[style]["hover"]
        self._pressed_color = self.colors[style]["pressed"]
        self._text_color = self.colors[style]["text"]

        # Current background color, will be animated
        self._color = self._base_color

        # Shadow effect
        self._create_shadow()

        # Setup style
        self.update_style()

    def _create_shadow(self):
        """Creates drop shadow effect for the button."""
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

    def update_style(self):
        """Updates button stylesheet based on current state."""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                color: {self._text_color};
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
        """)

    def enterEvent(self, event):
        """Mouse enter event - hover state."""
        self.hovered = True
        self._color = self._hover_color
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        """Mouse leave event - normal state."""
        self.hovered = False
        self._color = self._base_color
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        """Mouse press event - pressed state."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = True
            self._color = self._pressed_color
            self.update_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """Mouse release event - return to hover/normal state."""
        if event.button() == Qt.MouseButton.LeftButton:
            self.pressed = False
            self._color = self._hover_color if self.hovered else self._base_color
            self.update_style()
        super().mouseReleaseEvent(event)

    def set_style(self, style_type):
        """Changes button style."""
        if style_type in self.colors:
            self.style_type = style_type
            self._base_color = self.colors[style_type]["base"]
            self._hover_color = self.colors[style_type]["hover"]
            self._pressed_color = self.colors[style_type]["pressed"]
            self._text_color = self.colors[style_type]["text"]
            self._color = self._base_color if not self.hovered else self._hover_color
            self.update_style()

    def flash(self, color="#50FA7B", duration=300):
        """Creates a flash animation effect on the button."""
        original_color = self._color
        self._color = color
        self.update_style()

        # Reset color after delay
        QTimer.singleShot(duration, lambda: self._reset_color(original_color))

    def _reset_color(self, color):
        """Helper method to reset button color."""
        self._color = color
        self.update_style()


class IconButton(EnhancedButton):
    """A button that displays only an icon."""

    def __init__(self, icon, tooltip="", parent=None, style="primary", size=32):
        super().__init__("", parent, icon, style)

        # Set fixed size
        self.setFixedSize(QSize(size, size))

        # Set tooltip
        if tooltip:
            self.setToolTip(tooltip)

        # Center icon
        self.setIconSize(QSize(size-12, size-12))

        # Update style for icon button
        self.update_style()

    def update_style(self):
        """Updates button stylesheet for icon-only appearance."""
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                color: {self._text_color};
                border: none;
                border-radius: {self.width() // 2}px;  /* Makes it circular */
                padding: 0px;
            }}
        """)
