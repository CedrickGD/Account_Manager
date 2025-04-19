from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QListWidget, QMessageBox, QTextEdit,
    QComboBox, QListWidgetItem, QInputDialog, QGraphicsDropShadowEffect,
    QFrame, QSplitter, QScrollArea
)
from PyQt6.QtGui import QPainter, QBrush, QColor, QFont, QIcon, QLinearGradient, QPen
from PyQt6.QtCore import Qt, QTimer, QPoint, QSize, QPropertyAnimation, QEasingCurve, QRect, pyqtProperty, QUrl
import sys
import random
import json
import base64
import os
import time
import webbrowser

# Directory scanning instead of fixed file
DATABASE_DIR = os.path.dirname(os.path.abspath(__file__)) or os.getcwd()

# Modern color palette with transparency effects
COLOR_BG = "#121218"
COLOR_BG_GRADIENT_TOP = "#1A1A24"
COLOR_BG_GRADIENT_BOTTOM = "#0D0D12"
COLOR_PRIMARY = "#8A2BE2"  # Blueviolet
COLOR_PRIMARY_HOVER = "#9A3BF2"
COLOR_PRIMARY_PRESSED = "#7A1BD2"
COLOR_SECONDARY = "#6c5ce7"  # Secondary color
COLOR_SECONDARY_HOVER = "#7c6cf7"
COLOR_SECONDARY_PRESSED = "#5c4cd7"
COLOR_ACCENT = "#FF79C6"  # Accent color for highlights
COLOR_DANGER = "#FF5555"
COLOR_DANGER_HOVER = "#FF6E6E"
COLOR_DANGER_PRESSED = "#E64C4C"
COLOR_TEXT = "#F8F8F2"
COLOR_TEXT_SECONDARY = "#BFBFBF"
COLOR_PANEL = "rgba(30, 30, 40, 180)"
COLOR_PANEL_LIGHTER = "rgba(40, 40, 50, 200)"
COLOR_PANEL_SELECTED = "rgba(60, 50, 90, 200)"
COLOR_STATUS_INFO = "#8BE9FD"
COLOR_STATUS_SUCCESS = "#50FA7B"
COLOR_STATUS_ERROR = "#FF5555"

THEMES = {
    "dark": {
        "BG": "#121218",
        "BG_GRADIENT_TOP": "#1A1A24",
        "BG_GRADIENT_BOTTOM": "#0D0D12",
        "TEXT": "#F8F8F2",
        "TEXT_SECONDARY": "#BFBFBF",
        "PANEL": "rgba(30, 30, 40, 180)",
        "PANEL_LIGHTER": "rgba(40, 40, 50, 200)",
        "PANEL_SELECTED": "rgba(60, 50, 90, 200)"
    },
    "light": {
        "BG": "#f0f0f0",
        "BG_GRADIENT_TOP": "#ffffff",
        "BG_GRADIENT_BOTTOM": "#e0e0e0",
        "TEXT": "#2a2a2a",
        "TEXT_SECONDARY": "#555555",
        "PANEL": "rgba(255, 255, 255, 220)",
        "PANEL_LIGHTER": "rgba(250, 250, 250, 240)",
        "PANEL_SELECTED": "rgba(230, 230, 255, 220)"
    }
}


class ModernButton(QPushButton):
    def __init__(self, text, parent=None, primary=True):
        super().__init__(text, parent)
        self.current_theme = "dark"
        self.primary = primary
        self._base_color = COLOR_PRIMARY if primary else COLOR_SECONDARY
        self._hover_color = COLOR_PRIMARY_HOVER if primary else COLOR_SECONDARY_HOVER
        self._pressed_color = COLOR_PRIMARY_PRESSED if primary else COLOR_SECONDARY_PRESSED

        # Current background color, will be animated
        self._color = self._base_color

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)

        # Setup style
        self.update_style()

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self._color};
                color: {COLOR_TEXT};
                border: none;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                font-size: 14px;
            }}
        """)

    def enterEvent(self, event):
        self._color = self._hover_color
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._color = self._base_color
        self.update_style()
        super().leaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._color = self._pressed_color
            self.update_style()
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._color = self._hover_color if self.underMouse() else self._base_color
            self.update_style()
        super().mouseReleaseEvent(event)

    def update_theme_colors(self, theme_name):
        self.current_theme = theme_name


class DangerButton(ModernButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent, False)
        self._base_color = COLOR_DANGER
        self._hover_color = COLOR_DANGER_HOVER
        self._pressed_color = COLOR_DANGER_PRESSED
        self._color = self._base_color
        self.update_style()


class Snowflake:
    def __init__(self, x, y, size, speed, window_width, window_height):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.window_width = window_width
        self.window_height = window_height
        # Varying opacity for depth effect
        self.opacity = random.randint(30, 180)

    def fall(self):
        self.y += self.speed
        self.x += random.uniform(-0.5, 0.5)  # Slight horizontal drift
        if self.y > self.window_height:
            self.y = 0
            self.x = random.randint(0, self.window_width)


class ModernPanel(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            ModernPanel {{
                background-color: {COLOR_PANEL};
                border-radius: 12px;
                border: 1px solid rgba(80, 80, 100, 100);
            }}
        """)

        # Shadow effect
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 80))
        shadow.setOffset(0, 5)
        self.setGraphicsEffect(shadow)

    def update_style(self, panel_color):
        self.setStyleSheet(f"""
            ModernPanel {{
                background-color: {panel_color};
                border-radius: 12px;
                border: 1px solid rgba(80, 80, 100, 100);
            }}
        """)


class AccountManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Account Manager")
        self.setGeometry(100, 100, 1000, 600)  # Larger window for better UI

        # Current theme tracking
        self.current_theme = "dark"

        # Store current website URL
        self.current_website_url = None

        # Set window style
        self.setStyleSheet(f"""
            QWidget {{
                background-color: {COLOR_BG};
                color: {COLOR_TEXT};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {COLOR_TEXT};
            }}
            QLineEdit {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
            }}
            QTextEdit {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }}
            QListWidget {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                font-size: 14px;
                padding: 5px;
            }}
            QListWidget::item {{
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }}
            QListWidget::item:hover {{
                background-color: rgba(138, 43, 226, 30);
            }}
            QListWidget::item:selected {{
                background-color: {COLOR_PANEL_SELECTED};
                color: {COLOR_TEXT};
                border-left: 3px solid {COLOR_ACCENT};
            }}
            QComboBox {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                padding: 8px;
                padding-right: 20px;
                font-size: 14px;
                min-height: 25px;
            }}
            QComboBox:hover {{
                border: 1px solid {COLOR_PRIMARY};
            }}
            QComboBox::drop-down {{
                border: 0px;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLOR_PANEL};
                color: {COLOR_TEXT};
                selection-background-color: {COLOR_PANEL_SELECTED};
                selection-color: {COLOR_TEXT};
                border: 1px solid {COLOR_PRIMARY};
                border-radius: 8px;
                padding: 5px;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: rgba(40, 40, 50, 100);
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(138, 43, 226, 150);
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(154, 59, 242, 180);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background-color: rgba(40, 40, 50, 100);
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: rgba(138, 43, 226, 150);
                min-width: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: rgba(154, 59, 242, 180);
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QSplitter::handle {{
                background-color: rgba(138, 43, 226, 50);
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLOR_PRIMARY};
            }}
        """)

        # Dictionary to store all accounts by file
        self.all_db_accounts = {}  # Format: {filename: {account_name: password}}
        self.current_db_file = None

        # Initialize timer for periodic checking of database files
        self.file_check_timer = QTimer(self)
        self.file_check_timer.timeout.connect(self.scan_for_database_files)
        self.file_check_timer.start(5000)  # Check every 5 seconds

        # Animation effect for status messages
        self.status_animation = None

        # Initialize snowflakes animation
        self.snowflakes = []
        self.init_snowflakes()
        self.snowflake_timer = QTimer(self)
        self.snowflake_timer.timeout.connect(self.update_snowflakes)
        self.snowflake_timer.start(20)

        # Main layout with splitter for resizable panels
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(15, 15, 15, 15)

        # Create header for the app
        header_panel = ModernPanel()
        header_panel.setStyleSheet(f"""
            ModernPanel {{
                background-color: {COLOR_PANEL};
                border-radius: 12px;
                border: 1px solid rgba(80, 80, 100, 100);
            }}
            QLabel {{
                background: transparent;
            }}
        """)
        header_layout = QHBoxLayout(header_panel)

        app_title = QLabel("Vaultix Account Manager")
        app_title.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        app_title.setStyleSheet(
            f"color: {COLOR_ACCENT}; background: transparent;")

        # Title placed left side
        header_layout.addWidget(app_title)
        # Header layout with spacing
        header_layout.addStretch()

        # Status Label in header
        self.status_label = QLabel()
        self.status_label.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY}; font-style: italic; background: transparent;")
        header_layout.addWidget(self.status_label)

        # Toggle button placed right side
        self.theme_toggle = ModernButton("🌙", primary=False)
        self.theme_toggle.setFixedSize(QSize(40, 30))
        self.theme_toggle.setToolTip("Toggle Dark/Light Mode")
        self.theme_toggle.clicked.connect(self.toggle_theme)
        header_layout.addWidget(self.theme_toggle)

        # Current database indicator
        self.current_db_indicator = QLabel("")
        self.current_db_indicator.setFont(QFont("Segoe UI", 12))
        self.current_db_indicator.setStyleSheet(
            f"color: {COLOR_TEXT_SECONDARY};")
        header_layout.addWidget(self.current_db_indicator)

        main_layout.addWidget(header_panel)

        # Content splitter for left and right panels
        content_splitter = QSplitter(Qt.Orientation.Horizontal)

        # Left Panel
        left_panel = ModernPanel()
        self.left_panel = left_panel  # Store reference for theme updates
        left_layout = QVBoxLayout(left_panel)
        left_layout.setContentsMargins(10, 10, 10, 10)

        # Database selector section
        db_section = QFrame()
        db_section_layout = QVBoxLayout(db_section)
        db_section_layout.setContentsMargins(0, 0, 0, 0)

        db_header = QLabel("Databases")
        db_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        db_section_layout.addWidget(db_header)

        # Dropdown for file selection with label
        self.db_file_selector = QComboBox()
        self.db_file_selector.setMinimumHeight(40)
        self.db_file_selector.currentIndexChanged.connect(
            self.change_database_file)
        db_section_layout.addWidget(self.db_file_selector)

        # Database management buttons
        db_buttons_layout = QHBoxLayout()
        db_buttons_layout.setSpacing(10)

        self.new_db_button = ModernButton("Create Database", primary=False)
        self.new_db_button.clicked.connect(self.create_new_database)
        db_buttons_layout.addWidget(self.new_db_button)

        self.del_db_button = DangerButton("Delete Database")
        self.del_db_button.clicked.connect(self.delete_database)
        db_buttons_layout.addWidget(self.del_db_button)

        db_section_layout.addLayout(db_buttons_layout)
        left_layout.addWidget(db_section)

        # Separator
        separator = QFrame()
        separator.setFrameShape(QFrame.Shape.HLine)
        separator.setFrameShadow(QFrame.Shadow.Sunken)
        separator.setStyleSheet(
            "background-color: rgba(138, 43, 226, 50); margin: 10px 0;")
        left_layout.addWidget(separator)

        # Accounts section
        accounts_section = QFrame()
        accounts_layout = QVBoxLayout(accounts_section)
        accounts_layout.setContentsMargins(0, 0, 0, 0)

        accounts_header = QLabel("Accounts")
        accounts_header.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        accounts_layout.addWidget(accounts_header)

        # Account list with scroll area
        account_list_container = QScrollArea()
        account_list_container.setWidgetResizable(True)
        account_list_container.setStyleSheet(
            "border: none; background: transparent;")

        account_list_widget = QWidget()
        account_list_layout = QVBoxLayout(account_list_widget)
        account_list_layout.setContentsMargins(0, 0, 0, 0)

        self.account_list = QListWidget()
        self.account_list.setMinimumHeight(150)
        self.account_list.itemSelectionChanged.connect(
            self.display_account_details)
        account_list_layout.addWidget(self.account_list)

        account_list_container.setWidget(account_list_widget)
        accounts_layout.addWidget(account_list_container)

        # Input fields for new account
        input_section = QFrame()
        input_layout = QVBoxLayout(input_section)
        input_layout.setContentsMargins(0, 10, 0, 0)

        name_layout = QVBoxLayout()
        name_label = QLabel("Account Name")
        name_layout.addWidget(name_label)

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter account name")
        name_layout.addWidget(self.name_input)
        input_layout.addLayout(name_layout)

        # Add email field (optional)
        email_layout = QVBoxLayout()
        email_label = QLabel("Email (Optional)")
        email_layout.addWidget(email_label)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter email address")
        email_layout.addWidget(self.email_input)
        input_layout.addLayout(email_layout)

        # Add website field (optional)
        website_layout = QVBoxLayout()
        website_label = QLabel("Website URL (Optional)")
        website_layout.addWidget(website_label)

        self.website_input = QLineEdit()
        self.website_input.setPlaceholderText(
            "Enter website URL (e.g., https://example.com)")
        website_layout.addWidget(self.website_input)
        input_layout.addLayout(website_layout)

        pass_layout = QVBoxLayout()
        pass_label = QLabel("Password")
        pass_layout.addWidget(pass_label)

        self.pass_input = QLineEdit()
        self.pass_input.setPlaceholderText("Enter password")
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        pass_layout.addWidget(self.pass_input)
        input_layout.addLayout(pass_layout)

        # Account management buttons
        account_buttons_layout = QHBoxLayout()
        account_buttons_layout.setSpacing(10)

        self.add_button = ModernButton("Add Account")
        self.add_button.clicked.connect(self.add_account)
        account_buttons_layout.addWidget(self.add_button)

        self.del_button = DangerButton("Delete Account")
        self.del_button.clicked.connect(self.del_account)
        account_buttons_layout.addWidget(self.del_button)

        input_layout.addLayout(account_buttons_layout)
        accounts_layout.addWidget(input_section)

        left_layout.addWidget(accounts_section)
        content_splitter.addWidget(left_panel)

        # Right Panel (Account Details)
        right_panel = ModernPanel()
        self.right_panel = right_panel  # Store reference for theme updates
        right_layout = QVBoxLayout(right_panel)
        right_layout.setContentsMargins(10, 10, 10, 10)

        self.details_label = QLabel("Account Details")
        self.details_label.setFont(QFont("Segoe UI", 14, QFont.Weight.Bold))
        right_layout.addWidget(self.details_label)

        # Container for details
        details_container = QFrame()
        self.details_container = details_container  # Store reference for theme updates
        details_container.setStyleSheet(f"""
            QFrame {{
                background-color: {COLOR_PANEL_LIGHTER};
                border-radius: 8px;
                padding: 5px;
            }}
        """)
        details_container_layout = QVBoxLayout(details_container)

        self.details_view = QTextEdit()
        self.details_view.setReadOnly(True)
        self.details_view.setStyleSheet(
            "border: none; background: transparent;")
        details_container_layout.addWidget(self.details_view)

        right_layout.addWidget(details_container)

        # Action buttons for details
        details_buttons_layout = QHBoxLayout()

        self.copy_button = ModernButton("Copy Details", primary=False)
        self.copy_button.clicked.connect(self.copy_details)
        details_buttons_layout.addWidget(self.copy_button)

        # Website button
        self.website_button = ModernButton("Open Website", primary=True)
        self.website_button.clicked.connect(self.open_website)
        self.website_button.setVisible(False)  # Initially hidden
        details_buttons_layout.addWidget(self.website_button)

        # Edit password button
        self.edit_button = ModernButton("Edit Password")
        self.edit_button.clicked.connect(self.edit_password)
        details_buttons_layout.addWidget(self.edit_button)

        right_layout.addLayout(details_buttons_layout)

        # New feature: Password generator
        password_gen_section = QFrame()
        password_gen_layout = QVBoxLayout(password_gen_section)

        password_gen_header = QLabel("Password Generator")
        password_gen_header.setFont(QFont("Segoe UI", 12, QFont.Weight.Bold))
        password_gen_layout.addWidget(password_gen_header)

        password_gen_buttons = QHBoxLayout()

        self.gen_simple_button = ModernButton("Generate Simple", primary=False)
        self.gen_simple_button.clicked.connect(
            lambda: self.generate_password(simple=True))
        password_gen_buttons.addWidget(self.gen_simple_button)

        self.gen_strong_button = ModernButton("Generate Strong")
        self.gen_strong_button.clicked.connect(
            lambda: self.generate_password(simple=False))
        password_gen_buttons.addWidget(self.gen_strong_button)

        password_gen_layout.addLayout(password_gen_buttons)
        right_layout.addWidget(password_gen_section)

        content_splitter.addWidget(right_panel)

        # Set the initial split ratio (40% left, 60% right)
        content_splitter.setSizes([400, 600])
        main_layout.addWidget(content_splitter)

        # Initial search for database files
        self.scan_for_database_files()

    def toggle_theme(self):
        self.current_theme = "light" if self.current_theme == "dark" else "dark"
        self.theme_toggle.setText(
            "☀️" if self.current_theme == "dark" else "🌙")
        self.apply_theme()

    def apply_theme(self):
        if self.current_theme not in THEMES:
            self.set_status("Unknown theme: reverting to dark", "error")
            self.current_theme = "dark"

        theme = THEMES[self.current_theme]

        # Update global colors used in stylesheet
        global COLOR_BG, COLOR_BG_GRADIENT_TOP, COLOR_BG_GRADIENT_BOTTOM
        global COLOR_TEXT, COLOR_TEXT_SECONDARY, COLOR_PANEL, COLOR_PANEL_LIGHTER, COLOR_PANEL_SELECTED
        COLOR_BG = theme["BG"]
        COLOR_BG_GRADIENT_TOP = theme["BG_GRADIENT_TOP"]
        COLOR_BG_GRADIENT_BOTTOM = theme["BG_GRADIENT_BOTTOM"]
        COLOR_TEXT = theme["TEXT"]
        COLOR_TEXT_SECONDARY = theme["TEXT_SECONDARY"]
        COLOR_PANEL = theme["PANEL"]
        COLOR_PANEL_LIGHTER = theme["PANEL_LIGHTER"]
        COLOR_PANEL_SELECTED = theme["PANEL_SELECTED"]

        # Update Stylesheet
        try:
            self.setStyleSheet(self.generate_stylesheet())

            # Update ModernPanel styles
            self.left_panel.update_style(COLOR_PANEL)
            self.right_panel.update_style(COLOR_PANEL)

            # Update details container
            self.details_container.setStyleSheet(f"""
                QFrame {{
                    background-color: {COLOR_PANEL_LIGHTER};
                    border-radius: 8px;
                    padding: 5px;
                }}
            """)

            # Update buttons
            for widget in self.findChildren(ModernButton):
                widget.update_style()

            # Make sure current account details are displayed with new colors
            self.display_account_details()

        except Exception as e:
            print("Error applying Stylesheet:", e)
            self.set_status(f"Style Error: {e}", "error")

        # Repaint the window to apply new colors
        self.repaint()

    def generate_stylesheet(self):
        """Generates the stylesheet based on the current theme"""
        return f"""
            QWidget {{
                background-color: {COLOR_BG};
                color: {COLOR_TEXT};
                font-family: 'Segoe UI', Arial, sans-serif;
            }}
            QLabel {{
                color: {COLOR_TEXT};
            }}
            QLineEdit {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLOR_PRIMARY};
            }}
            QTextEdit {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                font-size: 14px;
                padding: 8px;
            }}
            QListWidget {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                font-size: 14px;
                padding: 5px;
            }}
            QListWidget::item {{
                border-radius: 5px;
                padding: 8px;
                margin: 2px;
            }}
            QListWidget::item:hover {{
                background-color: rgba(138, 43, 226, 30);
            }}
            QListWidget::item:selected {{
                background-color: {COLOR_PANEL_SELECTED};
                color: {COLOR_TEXT};
                border-left: 3px solid {COLOR_ACCENT};
            }}
            QComboBox {{
                background-color: {COLOR_PANEL_LIGHTER};
                color: {COLOR_TEXT};
                border: 1px solid rgba(138, 43, 226, 150);
                border-radius: 8px;
                padding: 8px;
                padding-right: 20px;
                font-size: 14px;
                min-height: 25px;
            }}
            QComboBox:hover {{
                border: 1px solid {COLOR_PRIMARY};
            }}
            QComboBox::drop-down {{
                border: 0px;
                width: 20px;
            }}
            QComboBox::down-arrow {{
                image: url(down_arrow.png);
                width: 12px;
                height: 12px;
            }}
            QComboBox QAbstractItemView {{
                background-color: {COLOR_PANEL};
                color: {COLOR_TEXT};
                selection-background-color: {COLOR_PANEL_SELECTED};
                selection-color: {COLOR_TEXT};
                border: 1px solid {COLOR_PRIMARY};
                border-radius: 8px;
                padding: 5px;
            }}
            QScrollBar:vertical {{
                border: none;
                background-color: rgba(40, 40, 50, 100);
                width: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical {{
                background-color: rgba(138, 43, 226, 150);
                min-height: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:vertical:hover {{
                background-color: rgba(154, 59, 242, 180);
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
            QScrollBar:horizontal {{
                border: none;
                background-color: rgba(40, 40, 50, 100);
                height: 10px;
                margin: 0px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal {{
                background-color: rgba(138, 43, 226, 150);
                min-width: 20px;
                border-radius: 5px;
            }}
            QScrollBar::handle:horizontal:hover {{
                background-color: rgba(154, 59, 242, 180);
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                width: 0px;
            }}
            QSplitter::handle {{
                background-color: rgba(138, 43, 226, 50);
                width: 2px;
            }}
            QSplitter::handle:hover {{
                background-color: {COLOR_PRIMARY};
            }}
        """

    def init_snowflakes(self):
        width = self.width()
        height = self.height()
        self.snowflakes = [
            Snowflake(
                random.randint(0, width),
                random.randint(0, height),
                random.randint(1, 4),
                random.uniform(0.5, 2.5),
                width, height
            ) for _ in range(150)
        ]

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.init_snowflakes()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Draw dark gradient background
        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor(COLOR_BG_GRADIENT_TOP))
        gradient.setColorAt(1, QColor(COLOR_BG_GRADIENT_BOTTOM))
        painter.fillRect(self.rect(), gradient)

        # Draw snowflakes
        for flake in self.snowflakes:
            painter.setBrush(QBrush(QColor(255, 255, 255, flake.opacity)))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(
                QPoint(int(flake.x), int(flake.y)), flake.size, flake.size)

    def update_snowflakes(self):
        for flake in self.snowflakes:
            flake.fall()
        self.update()

    def set_status(self, message, status_type="info"):
        """Sets status message with animation effect"""
        if status_type == "success":
            color = COLOR_STATUS_SUCCESS
        elif status_type == "error":
            color = COLOR_STATUS_ERROR
        else:
            color = COLOR_STATUS_INFO

        self.status_label.setText(message)
        self.status_label.setStyleSheet(
            f"color: {color}; font-style: italic; background: transparent;")

        # Clear any existing animation timer
        if self.status_animation is not None:
            self.status_animation.stop()

        # Set timer to clear status after a few seconds
        if status_type == "success" or status_type == "error":
            self.status_animation = QTimer(self)
            self.status_animation.timeout.connect(
                lambda: self.status_label.setText(""))
            self.status_animation.setSingleShot(True)
            self.status_animation.start(3000)  # 3 seconds

    def scan_for_database_files(self):
        """Searches the directory for compatible database files"""
        # Save previous selection
        previous_selection = self.db_file_selector.currentText()
        previous_file = previous_selection.split(
            " (")[0] if " (" in previous_selection else previous_selection

        selected_account = None
        if self.account_list.currentItem():
            selected_account = self.account_list.currentItem().text()

        # Update status
        self.set_status("Searching for database files...", "info")
        QApplication.processEvents()  # Update UI

        # Block signals during update
        self.db_file_selector.blockSignals(True)
        self.db_file_selector.clear()

        # Get current directory
        current_dir = DATABASE_DIR

        found_files = []

        # Search for compatible files
        for file in os.listdir(current_dir):
            file_path = os.path.join(current_dir, file)
            if os.path.isfile(file_path):
                try:
                    accounts = self.try_load_database(file_path)
                    if accounts is not None:  # If it's a valid database format
                        found_files.append((file, len(accounts)))
                        # Store accounts in the all_db_accounts dictionary
                        self.all_db_accounts[file] = accounts
                except Exception as e:
                    pass  # Ignore non-compatible files

        # Add found files to dropdown
        if found_files:
            for file, count in sorted(found_files):
                self.db_file_selector.addItem(f"{file} ({count} accounts)")

            # Try to restore previous selection
            index = -1
            for i in range(self.db_file_selector.count()):
                item_text = self.db_file_selector.itemText(i)
                file_name = item_text.split(
                    " (")[0] if " (" in item_text else item_text
                if file_name == previous_file:
                    index = i
                    break

            if index >= 0:
                self.db_file_selector.setCurrentIndex(index)
            else:
                self.db_file_selector.setCurrentIndex(0)  # Select first file

            # Update status
            self.set_status(
                f"{len(found_files)} database files found", "success")
        else:
            self.all_db_accounts = {}
            self.account_list.clear()
            self.details_view.clear()
            self.current_db_indicator.setText("")
            self.website_button.setVisible(False)
            self.set_status("No database files found", "error")

        # Release signals
        self.db_file_selector.blockSignals(False)

        # Load accounts for current file
        self.change_database_file()

        # Attempts to select the previously selected account again
        if selected_account:
            for i in range(self.account_list.count()):
                if self.account_list.item(i).text() == selected_account:
                    self.account_list.setCurrentRow(i)
                    break

    def try_load_database(self, file_path):
        """Attempts to load a file as a database"""
        try:
            with open(file_path, "rb") as f:
                encoded_data = f.read()
                # Try to decode Base64
                decoded_data = base64.b64decode(encoded_data)
                # Try to load as JSON
                json_data = json.loads(decoded_data.decode())
                # If that works, it's probably a valid database file
                if isinstance(json_data, dict):
                    return json_data
        except:
            pass
        return None

    def change_database_file(self):
        """Changes the current database file"""
        if self.db_file_selector.count() == 0:
            self.current_db_file = None
            self.account_list.clear()
            self.current_db_indicator.setText("")
            self.details_view.clear()
            return

        # Extract filename from ComboBox text (Format: "filename (X accounts)")
        full_text = self.db_file_selector.currentText()
        self.current_db_file = full_text.split(
            " (")[0] if " (" in full_text else full_text

        # Update the current database indicator in header
        self.current_db_indicator.setText(
            f"Current Database: {self.current_db_file}")

        # Load accounts for current file
        self.load_account_list()

    def create_new_database(self):
        """Creates a new database file"""
        name, ok = QInputDialog.getText(
            self, "New Database", "Enter filename:", QLineEdit.EchoMode.Normal, "")
        if ok and name:
            # Add .vault extension if not provided
            if not name.endswith('.vault') and not '.' in name:
                name = name + '.vault'

            # Ensure the file doesn't already exist
            file_path = os.path.join(DATABASE_DIR, name)
            if os.path.exists(file_path):
                QMessageBox.warning(
                    self, "Error", f"A file named '{name}' already exists.")
                return

            # Create empty database and save it immediately
            self.all_db_accounts[name] = {}

            # Create and save empty database
            try:
                json_data = json.dumps({}).encode()
                encoded_data = base64.b64encode(json_data)
                with open(file_path, "wb") as f:
                    f.write(encoded_data)

                # Update the view
                self.scan_for_database_files()

                # Select the new database
                for i in range(self.db_file_selector.count()):
                    if self.db_file_selector.itemText(i).startswith(f"{name} ("):
                        self.db_file_selector.setCurrentIndex(i)
                        break

                self.set_status(
                    f"Database '{name}' created successfully", "success")
            except Exception as e:
                QMessageBox.critical(self, "Creation Error",
                                     f"Could not create database: {e}")

    def delete_database(self):
        """Deletes the current database file"""
        if not self.current_db_file:
            QMessageBox.warning(self, "Error", "No database selected.")
            return

        # Ask for confirmation
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the database '{self.current_db_file}'?\nThis cannot be undone.",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Delete the file
                file_path = os.path.join(DATABASE_DIR, self.current_db_file)
                if os.path.exists(file_path):
                    os.remove(file_path)

                # Remove from dictionary
                if self.current_db_file in self.all_db_accounts:
                    del self.all_db_accounts[self.current_db_file]

                # Clear UI
                self.account_list.clear()
                self.details_view.clear()

                # Update the database list
                self.scan_for_database_files()

                self.set_status(
                    f"Database '{self.current_db_file}' deleted successfully", "success")

                # Reset current file
                self.current_db_file = None
            except Exception as e:
                QMessageBox.critical(self, "Deletion Error",
                                     f"Could not delete database: {e}")

    def add_account(self):
        """Adds an account to the current database"""
        if not self.current_db_file:
            QMessageBox.warning(self, "Error", "No database selected.")
            return

        name = self.name_input.text()
        password = self.pass_input.text()
        email = self.email_input.text()  # Get email value (optional)
        website = self.website_input.text()  # Get website value (optional)

        if not name:
            QMessageBox.warning(self, "Input Error",
                                "Please enter an account name.")
            return

        if not password:
            QMessageBox.warning(self, "Input Error",
                                "Please enter a password.")
            return

        # Check if account already exists
        if name in self.all_db_accounts[self.current_db_file]:
            confirm = QMessageBox.question(
                self,
                "Account Exists",
                f"An account named '{name}' already exists. Do you want to update it?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return

        # Create account data dictionary with all fields
        account_data = {
            "password": password,
            "email": email,
            "website": website,
            "created": time.strftime('%Y-%m-%d %H:%M:%S')
        }

        # Add account to current database
        self.all_db_accounts[self.current_db_file][name] = account_data
        self.save_accounts(self.current_db_file)
        self.load_account_list()

        # Clear input fields
        self.name_input.clear()
        self.email_input.clear()
        self.website_input.clear()
        self.pass_input.clear()

        # Update the filename in dropdown to show new account count
        self.scan_for_database_files()

        # Select the newly added account
        for i in range(self.account_list.count()):
            if self.account_list.item(i).text() == name:
                self.account_list.setCurrentRow(i)
                break

        self.set_status(f"Account '{name}' added successfully", "success")

    def del_account(self):
        """Deletes the selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No account selected.")
            return

        account_name = selected_items[0].text()

        # Ask for confirmation
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the account '{account_name}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if confirm == QMessageBox.StandardButton.Yes:
            # Delete account from database
            if account_name in self.all_db_accounts[self.current_db_file]:
                del self.all_db_accounts[self.current_db_file][account_name]
                self.save_accounts(self.current_db_file)
                self.load_account_list()
                self.details_view.clear()

                # Update the filename in dropdown to show new account count
                self.scan_for_database_files()

                self.set_status(
                    f"Account '{account_name}' deleted successfully", "success")

    def load_account_list(self):
        """Loads the account list for the current database"""
        self.account_list.clear()

        if not self.current_db_file:
            return

        if self.current_db_file not in self.all_db_accounts:
            return

        # Add accounts to list
        for account_name in sorted(self.all_db_accounts[self.current_db_file].keys()):
            item = QListWidgetItem(account_name)
            # Add hover animation effect via style
            item.setToolTip("Click to view details")
            self.account_list.addItem(item)

    def display_account_details(self):
        """Displays the details of the selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            self.details_view.clear()
            self.details_label.setText("Account Details")
            self.website_button.setVisible(False)
            self.current_website_url = None
            return

        account_name = selected_items[0].text()
        if self.current_db_file and account_name in self.all_db_accounts[self.current_db_file]:
            account_data = self.all_db_accounts[self.current_db_file][account_name]

            # Handle both old and new data format
            if isinstance(account_data, str):
                # Old format: password only
                password = account_data
                email = ""
                website = ""
                created_time = time.strftime('%Y-%m-%d %H:%M:%S')
            else:
                # New format: dictionary with all fields
                password = account_data.get("password", "")
                email = account_data.get("email", "")
                website = account_data.get("website", "")
                created_time = account_data.get(
                    "created", time.strftime('%Y-%m-%d %H:%M:%S'))

            # Store current website URL and update button visibility
            self.current_website_url = website
            self.website_button.setVisible(bool(website))

            # Update details view with formatted HTML
            self.details_view.setHtml(f"""
                <style>
                    body {{ font-family: 'Segoe UI', Arial, sans-serif; color: {COLOR_TEXT}; }}
                    .label {{ color: {COLOR_TEXT_SECONDARY}; font-size: 14px; margin-bottom: 5px; }}
                    .value {{ color: {COLOR_TEXT}; font-size: 16px; margin-bottom: 15px; 
                              background-color: rgba(60, 50, 90, 100); padding: 8px; border-radius: 5px; }}
                    .password {{ font-family: monospace; letter-spacing: 1px; }}
                </style>
                <div class="label">Account Name:</div>
                <div class="value">{account_name}</div>
                
                <div class="label">Password:</div>
                <div class="value password">{password}</div>
                
                <div class="label">Email:</div>
                <div class="value">{email or "Not provided"}</div>
                
                <div class="label">Website:</div>
                <div class="value">{website or "Not provided"}</div>
                
                <div class="label">Creation Time:</div>
                <div class="value">{created_time}</div>
            """)

            # Update header
            self.details_label.setText(f"Account Details: {account_name}")

    def open_website(self):
        """Open the website URL in the default browser"""
        if self.current_website_url:
            url = self.current_website_url

            # Add https:// prefix if missing
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url

            try:
                webbrowser.open(url)
                self.set_status(f"Opening website: {url}", "success")
            except Exception as e:
                self.set_status(f"Could not open website: {e}", "error")

    def save_accounts(self, filename):
        """Saves the accounts to the database file"""
        if not filename:
            return False

        try:
            # Get the accounts for the current file
            accounts = self.all_db_accounts.get(filename, {})

            # Convert to JSON and encode
            json_data = json.dumps(accounts).encode()
            encoded_data = base64.b64encode(json_data)

            # Save to file
            file_path = os.path.join(DATABASE_DIR, filename)
            with open(file_path, "wb") as f:
                f.write(encoded_data)

            return True
        except Exception as e:
            QMessageBox.critical(self, "Save Error",
                                 f"Could not save database: {e}")
            return False

    def copy_details(self):
        """Copies the selected account details to clipboard"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            return

        account_name = selected_items[0].text()
        if self.current_db_file and account_name in self.all_db_accounts[self.current_db_file]:
            account_data = self.all_db_accounts[self.current_db_file][account_name]

            # Handle both old and new data format
            if isinstance(account_data, str):
                # Old format: password only
                password = account_data
                email = ""
                website = ""
            else:
                # New format: dictionary with all fields
                password = account_data.get("password", "")
                email = account_data.get("email", "")
                website = account_data.get("website", "")

            # Copy account and password to clipboard
            clipboard_text = f"Account: {account_name}\nPassword: {password}"

            # Add email and website if available
            if email:
                clipboard_text += f"\nEmail: {email}"
            if website:
                clipboard_text += f"\nWebsite: {website}"

            QApplication.clipboard().setText(clipboard_text)

            # Show animation effect for confirmation
            self.set_status("Account details copied to clipboard", "success")

            # Flash effect on copy button
            original_color = self.copy_button._color
            self.copy_button._color = COLOR_STATUS_SUCCESS
            self.copy_button.update_style()

            # Reset color after delay
            QTimer.singleShot(300, lambda: self.reset_button_color(
                self.copy_button, original_color))

    def reset_button_color(self, button, color):
        """Helper to reset button color after animation"""
        button._color = color
        button.update_style()

    def edit_password(self):
        """Edits the password of the selected account"""
        selected_items = self.account_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Error", "No account selected.")
            return

        account_name = selected_items[0].text()
        if self.current_db_file and account_name in self.all_db_accounts[self.current_db_file]:
            account_data = self.all_db_accounts[self.current_db_file][account_name]

            # Handle both old and new data format
            if isinstance(account_data, str):
                # Old format: password only
                current_password = account_data
                current_email = ""
                current_website = ""
            else:
                # New format: dictionary with all fields
                current_password = account_data.get("password", "")
                current_email = account_data.get("email", "")
                current_website = account_data.get("website", "")

            # Ask for new password
            new_password, ok = QInputDialog.getText(
                self,
                "Edit Password",
                f"Enter new password for '{account_name}':",
                QLineEdit.EchoMode.Password,
                current_password
            )

            if ok and new_password:
                # Update account data
                if isinstance(account_data, str):
                    # Convert old format to new format
                    self.all_db_accounts[self.current_db_file][account_name] = {
                        "password": new_password,
                        "email": current_email,
                        "website": current_website,
                        "created": time.strftime('%Y-%m-%d %H:%M:%S')
                    }
                else:
                    # Update password in existing dictionary
                    account_data["password"] = new_password
                    self.all_db_accounts[self.current_db_file][account_name] = account_data

                # Save and update display
                self.save_accounts(self.current_db_file)
                self.display_account_details()

                # Show confirmation
                self.set_status(
                    f"Password for '{account_name}' updated", "success")
        if self.current_db_file and account_name in self.all_db_accounts[self.current_db_file]:
            current_password = self.all_db_accounts[self.current_db_file][account_name]

            # Ask for new password
            new_password, ok = QInputDialog.getText(
                self,
                "Edit Password",
                f"Enter new password for '{account_name}':",
                QLineEdit.EchoMode.Password,
                current_password
            )

            if ok and new_password:
                # Update password
                self.all_db_accounts[self.current_db_file][account_name] = new_password
                self.save_accounts(self.current_db_file)

                # Update display
                self.display_account_details()

                # Show confirmation
                self.set_status(
                    f"Password for '{account_name}' updated", "success")

    def generate_password(self, simple=True):
        """Generates a random password and places it in the password field"""
        import string

        if simple:
            # Generate simple but memorable password
            adjectives = ["happy", "clever", "brave",
                          "wise", "gentle", "swift", "bright", "calm"]
            nouns = ["tiger", "river", "mountain", "forest",
                     "ocean", "desert", "cloud", "star"]
            numbers = [str(random.randint(10, 99)) for _ in range(1)]

            password = random.choice(
                adjectives) + random.choice(nouns) + random.choice(numbers)
        else:
            # Generate strong random password with special characters
            length = 16
            chars = string.ascii_letters + string.digits + string.punctuation
            password = ''.join(random.choice(chars) for _ in range(length))

        # Set password in input field
        self.pass_input.setText(password)

        # Show animation to highlight the password field
        original_style = self.pass_input.styleSheet()
        highlight_style = f"""
            QLineEdit {{
                background-color: rgba(80, 250, 123, 50);
                color: {COLOR_TEXT};
                border: 2px solid {COLOR_STATUS_SUCCESS};
                border-radius: 8px;
                padding: 8px;
                font-size: 14px;
            }}
        """
        self.pass_input.setStyleSheet(highlight_style)

        # Reset style after delay
        QTimer.singleShot(
            500, lambda: self.pass_input.setStyleSheet(original_style))

        # Show confirmation
        complexity = "simple" if simple else "strong"
        self.set_status(f"Generated {complexity} password", "success")


def main():
    app = QApplication(sys.argv)
    window = AccountManager()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
