from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

from .constants import TITLE_BAR_BG_COLOR, TEXT_COLOR, SUBTEXT_COLOR, SMALL_FONT_SIZE, TITLE_FONT_SIZE

class CustomTitleBar(QWidget):
    # Them cac signal neu can (vd: nut settings)
    # settings_button_clicked = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("customTitleBar")
        self.setFixedHeight(40) 

        layout = QHBoxLayout(self)
        layout.setContentsMargins(10, 0, 5, 0) 
        layout.setSpacing(6)

        self.icon_label = QLabel("📁") # Icon file
        font = QFont()
        font.setPointSize(TITLE_FONT_SIZE - 2) # Kich thuoc icon
        self.icon_label.setFont(font)
        self.icon_label.setStyleSheet(f"color: {TEXT_COLOR}; padding-bottom: 2px;")
        layout.addWidget(self.icon_label)

        self.title_label = QLabel("Tạo Tài Liệu Dự Án") # Ten App
        self.title_label.setObjectName("titleBarLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label)
        
        self.version_label = QLabel("v3.0.0-PySide6") # VD version
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.version_label)

        layout.addStretch(1)

        # Nut Minimize
        self.btn_minimize = QPushButton("–")
        self.btn_minimize.setObjectName("minimizeButton")
        self.btn_minimize.setFixedSize(30, 30)
        self.btn_minimize.clicked.connect(self.window().showMinimized)
        layout.addWidget(self.btn_minimize)

        # Nut Maximize/Restore
        self.btn_maximize_restore = QPushButton("□")
        self.btn_maximize_restore.setObjectName("maximizeRestoreButton")
        self.btn_maximize_restore.setFixedSize(30, 30)
        self.btn_maximize_restore.clicked.connect(self._toggle_maximize_restore)
        layout.addWidget(self.btn_maximize_restore)

        # Nut Close
        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("closeButton")
        self.btn_close.setFixedSize(30, 30)
        self.btn_close.clicked.connect(self.window().close)
        layout.addWidget(self.btn_close)

        self._apply_styles()

    def _apply_styles(self):
        font_family = "Segoe UI, Arial, sans-serif"
        self.setStyleSheet(f"""
            QWidget#customTitleBar {{
                background-color: {TITLE_BAR_BG_COLOR};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid rgba(224, 218, 230, 0.1);
            }}
            QLabel#titleBarLabel {{
                color: {TEXT_COLOR};
                font-family: "{font_family}";
                font-size: {TITLE_FONT_SIZE - 4}pt; /* Dieu chinh */
                font-weight: bold;
                padding-left: 5px;
                background-color: transparent;
            }}
            QLabel#versionLabel {{
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-size: {SMALL_FONT_SIZE}pt;
                padding-left: 8px;
                background-color: transparent;
            }}
            QPushButton {{ /* Base style for title bar buttons */
                background-color: transparent;
                border: none;
                border-radius: 6px;
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-size: 12pt; /* Kich thuoc icon nut */
                font-weight: bold;
                min-width: 30px; max-width: 30px;
                min-height: 30px; max-height: 30px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: rgba(224, 218, 230, 0.15);
                color: {TEXT_COLOR};
            }}
            QPushButton:pressed {{
                background-color: rgba(224, 218, 230, 0.08);
            }}
            QPushButton#closeButton:hover {{
                background-color: rgba(200, 90, 110, 0.75); /* Mau do khi hover nut close */
                color: white;
            }}
            QPushButton#closeButton:pressed {{
                background-color: rgba(190, 80, 100, 0.6);
            }}
        """)

    def _toggle_maximize_restore(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.btn_maximize_restore.setText("□") # Icon restore
        else:
            self.window().showMaximized()
            self.btn_maximize_restore.setText("▫") # Icon khi da maximize (hoac 2 o vuong chong nhau)
    
    def setTitle(self, title):
        self.title_label.setText(title)

    def setVersion(self, version_text):
        self.version_label.setText(version_text)