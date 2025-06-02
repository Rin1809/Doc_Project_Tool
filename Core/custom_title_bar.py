from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QComboBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from .constants import ( 
    TITLE_BAR_BG_COLOR, TEXT_COLOR, SUBTEXT_COLOR, SMALL_FONT_SIZE, TITLE_FONT_SIZE,
    ACCENT_COLOR, ERROR_COLOR
)
from .translations import Translations 

class CustomTitleBar(QWidget):
    language_changed_signal = Signal(str) 

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("customTitleBar")
        self.setFixedHeight(42) # Tang chieu cao

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 0, 6, 0) 
        layout.setSpacing(8)

        self.icon_label = QLabel("✧") # Icon moi
        font_icon = QFont() 
        font_icon.setPointSize(TITLE_FONT_SIZE - 3) 
        self.icon_label.setFont(font_icon)
        self.icon_label.setStyleSheet(f"color: {ACCENT_COLOR}; padding-bottom: 3px;") # Mau icon
        layout.addWidget(self.icon_label)

        self.title_label = QLabel() 
        self.title_label.setObjectName("titleBarLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.title_label)
        
        self.version_label = QLabel() 
        self.version_label.setObjectName("versionLabel")
        self.version_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)
        layout.addWidget(self.version_label)

        layout.addStretch(1)

        self.lang_combo = QComboBox(self)
        self.lang_combo.setObjectName("languageComboBox")
        self.lang_combo.setMinimumWidth(95) 
        self.lang_combo.currentIndexChanged.connect(self._on_lang_combo_changed)
        layout.addWidget(self.lang_combo)
        layout.addSpacerItem(QSpacerItem(8, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))


        self.btn_minimize = QPushButton("–")
        self.btn_minimize.setObjectName("minimizeButton")
        self.btn_minimize.setFixedSize(32, 32)
        self.btn_minimize.clicked.connect(self.window().showMinimized)
        layout.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton("□")
        self.btn_maximize_restore.setObjectName("maximizeRestoreButton")
        self.btn_maximize_restore.setFixedSize(32, 32)
        self.btn_maximize_restore.clicked.connect(self._toggle_maximize_restore)
        layout.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton("✕")
        self.btn_close.setObjectName("closeButton")
        self.btn_close.setFixedSize(32, 32)
        self.btn_close.clicked.connect(self.window().close)
        layout.addWidget(self.btn_close)

        self._apply_styles()
        self.retranslate_ui() 

    def _apply_styles(self):
        font_family = "Segoe UI, Arial, sans-serif"
        if Translations.current_lang == Translations.LANG_JA:
            font_family = "Meiryo, Segoe UI, Arial, sans-serif"

        button_hover_bg = QColor(ACCENT_COLOR).lighter(120).name()
        button_pressed_bg = QColor(ACCENT_COLOR).darker(110).name()
        close_hover_bg = QColor(ERROR_COLOR).lighter(110).name()
        close_pressed_bg = QColor(ERROR_COLOR).darker(110).name()


        self.setStyleSheet(f"""
            QWidget#customTitleBar {{
                background-color: {TITLE_BAR_BG_COLOR};
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom: 1px solid rgba(200, 205, 220, 0.12);
            }}
            QLabel#titleBarLabel {{
                color: {TEXT_COLOR};
                font-family: "{font_family}";
                font-size: {TITLE_FONT_SIZE - 5}pt; 
                font-weight: 600; /* hoi dam hon */
                padding-left: 6px;
                background-color: transparent;
            }}
            QLabel#versionLabel {{
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-size: {SMALL_FONT_SIZE -1}pt;
                padding-left: 10px;
                background-color: transparent;
            }}
            QComboBox#languageComboBox {{
                background-color: rgba(35,40,70,0.88); 
                color: {TEXT_COLOR};
                border: 1px solid rgba(150,160,200,0.6); 
                border-radius: 6px;
                padding: 4px 6px; 
                font-family: "{font_family}"; 
                font-size: {SMALL_FONT_SIZE -1}pt; 
                min-height: 22px;
            }}
            QComboBox#languageComboBox:hover {{ 
                border-color: {ACCENT_COLOR}; 
            }}
            QComboBox#languageComboBox::drop-down {{
                subcontrol-origin: padding; subcontrol-position: top right; width: 18px;
                border-left-width: 1px; border-left-color: rgba(150,160,200,0.6); border-left-style: solid;
                border-top-right-radius: 6px; border-bottom-right-radius: 6px;
            }}
            QComboBox QAbstractItemView {{ 
                background-color: rgb(28, 32, 55); 
                color: {TEXT_COLOR};
                border: 1px solid {ACCENT_COLOR};
                selection-background-color: {button_hover_bg};
                padding: 4px; border-radius: 5px; 
                font-family: "{font_family}"; font-size: {SMALL_FONT_SIZE -1}pt;
            }}
            QPushButton {{ 
                background-color: transparent;
                border: none;
                border-radius: 7px; /* bo tron hon */
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-size: 13pt; 
                font-weight: normal;
                min-width: 32px; max-width: 32px;
                min-height: 32px; max-height: 32px;
                padding: 0px;
            }}
            QPushButton:hover {{
                background-color: {button_hover_bg};
                color: white;
            }}
            QPushButton:pressed {{
                background-color: {button_pressed_bg};
            }}
            QPushButton#closeButton:hover {{
                background-color: {close_hover_bg}; 
                color: white;
            }}
            QPushButton#closeButton:pressed {{
                background-color: {close_pressed_bg};
            }}
        """)
        self.update()


    def _on_lang_combo_changed(self, index): 
        lang_code = self.lang_combo.itemData(index)
        if lang_code:
            self.language_changed_signal.emit(lang_code)

    def _toggle_maximize_restore(self):
        if self.window().isMaximized():
            self.window().showNormal()
            self.btn_maximize_restore.setText("□") 
        else:
            self.window().showMaximized()
            self.btn_maximize_restore.setText("▫") 
    
    def setTitle(self, title_key="app_title_on_bar"): 
        self.title_label.setText(Translations.get(title_key))

    def setVersion(self, version_key="app_version_pyside6"):
        self.version_label.setText(Translations.get(version_key))

    def retranslate_ui(self): 
        self.setTitle() 
        self.setVersion() 

        current_data = self.lang_combo.currentData()
        self.lang_combo.blockSignals(True)
        self.lang_combo.clear()
        for code, name in Translations.lang_map.items():
            self.lang_combo.addItem(name, code)
        
        current_index = self.lang_combo.findData(current_data if current_data else Translations.current_lang)
        if current_index != -1:
            self.lang_combo.setCurrentIndex(current_index)
        else: 
             fallback_idx = self.lang_combo.findData(Translations.current_lang)
             if fallback_idx != -1: self.lang_combo.setCurrentIndex(fallback_idx)

        self.lang_combo.blockSignals(False)
        self._apply_styles() 