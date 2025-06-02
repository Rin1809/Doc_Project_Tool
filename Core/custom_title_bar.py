# Core/custom_title_bar.py
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QPushButton, QSpacerItem, QSizePolicy, QComboBox
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont, QColor

from .constants import (
    TITLE_BAR_BG_COLOR, TEXT_COLOR, SUBTEXT_COLOR, SMALL_FONT_SIZE, TITLE_FONT_SIZE, HEADER_FONT_SIZE,
    ACCENT_COLOR, ERROR_COLOR, TEXT_HOVER_COLOR, HOVER_COLOR, SELECTED_COLOR, INPUT_BG_COLOR, INPUT_BORDER_COLOR
)
from .translations import Translations

class CustomTitleBar(QWidget):
    language_changed_signal = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("customTitleBar")
        self.setFixedHeight(45) # Chieu cao thanh tieu de

        layout = QHBoxLayout(self)
        layout.setContentsMargins(15, 0, 8, 0) # dieu chinh margin
        layout.setSpacing(10)

        self.icon_label = QLabel("✧")
        font_icon = QFont()
        font_icon.setPointSize(TITLE_FONT_SIZE - 2) # Kich thuoc icon
        self.icon_label.setFont(font_icon)
        self.icon_label.setStyleSheet(f"color: {ACCENT_COLOR}; padding-bottom: 3px;")
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
        self.lang_combo.setMinimumWidth(100) # chieu rong combo
        self.lang_combo.currentIndexChanged.connect(self._on_lang_combo_changed)
        layout.addWidget(self.lang_combo)
        layout.addSpacerItem(QSpacerItem(10, 0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))


        self.btn_minimize = QPushButton("–") # ky tu to hon
        self.btn_minimize.setObjectName("minimizeButton")
        self.btn_minimize.setFixedSize(36, 36) # Kich thuoc nut
        self.btn_minimize.clicked.connect(self.window().showMinimized)
        layout.addWidget(self.btn_minimize)

        self.btn_maximize_restore = QPushButton("□")
        self.btn_maximize_restore.setObjectName("maximizeRestoreButton")
        self.btn_maximize_restore.setFixedSize(36, 36)
        self.btn_maximize_restore.clicked.connect(self._toggle_maximize_restore)
        layout.addWidget(self.btn_maximize_restore)

        self.btn_close = QPushButton("✕") # ky tu to hon
        self.btn_close.setObjectName("closeButton")
        self.btn_close.setFixedSize(36, 36)
        self.btn_close.clicked.connect(self.window().close)
        layout.addWidget(self.btn_close)

        self._apply_styles()
        self.retranslate_ui()

    def _apply_styles(self):
        font_family = "Segoe UI, Arial, sans-serif"
        if Translations.current_lang == Translations.LANG_JA:
            font_family = "Meiryo, Segoe UI, Arial, sans-serif"

        # Mau cho nut
        button_hover_bg = QColor(ACCENT_COLOR).lighter(130).name()
        button_pressed_bg = QColor(ACCENT_COLOR).darker(120).name()
        close_hover_bg = QColor(ERROR_COLOR).lighter(115).name()
        close_pressed_bg = QColor(ERROR_COLOR).darker(115).name()

        self.setStyleSheet(f"""
            QWidget#customTitleBar {{
                background-color: {TITLE_BAR_BG_COLOR};
                border-top-left-radius: 10px; /* Giu nguyen radius cua BaseMainWindow */
                border-top-right-radius: 10px;
                border-bottom: 1px solid rgba(200, 205, 220, 0.15); /* Vien duoi dam hon chut */
            }}
            QLabel#titleBarLabel {{
                color: {TEXT_COLOR};
                font-family: "{font_family}";
                font-size: {HEADER_FONT_SIZE -1}pt; /* Kich thuoc font tieu de */
                font-weight: 600;
                padding-left: 8px;
                padding-right: 5px;
                background-color: transparent;
            }}
            QLabel#titleBarLabel:hover {{
                color: {TEXT_HOVER_COLOR}; /* Hieu ung hover cho tieu de */
            }}
            QLabel#versionLabel {{
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-size: {SMALL_FONT_SIZE}pt; /* Kich thuoc font phien ban */
                padding-left: 0px; /* Gan hon voi title */
                background-color: transparent;
            }}
            QLabel#versionLabel:hover {{
                color: {TEXT_COLOR}; /* Hieu ung hover cho version */
            }}
            QComboBox#languageComboBox {{
                background-color: {INPUT_BG_COLOR};
                color: {TEXT_COLOR};
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 7px; /* Bo tron hon */
                padding: 5px 8px; /* Tang padding */
                font-family: "{font_family}";
                font-size: {SMALL_FONT_SIZE}pt;
                min-height: 24px; /* Chieu cao min */
            }}
            QComboBox#languageComboBox:hover {{
                border-color: {ACCENT_COLOR};
            }}
            QComboBox#languageComboBox::drop-down {{
                subcontrol-origin: padding; subcontrol-position: top right; width: 20px;
                border-left-width: 1px; border-left-color: {INPUT_BORDER_COLOR}; border-left-style: solid;
                border-top-right-radius: 7px; border-bottom-right-radius: 7px;
            }}
            QComboBox#languageComboBox::down-arrow {{
                image: url(none); /* An mui ten mac dinh, co the thay = icon SVG neu muon */
                width: 10px; height: 10px;
            }}
            QComboBox QAbstractItemView {{
                background-color: rgb(25, 30, 55); /* Dam hon chut */
                color: {TEXT_COLOR};
                border: 1px solid {ACCENT_COLOR};
                selection-background-color: {SELECTED_COLOR};
                selection-color: {INPUT_BG_COLOR}; /* Mau chu khi chon item */
                padding: 5px; border-radius: 7px;
                font-family: "{font_family}"; font-size: {SMALL_FONT_SIZE}pt;
                outline: 0px; /* An vien focus cua item view */
            }}
            QPushButton {{
                background-color: transparent;
                border: none;
                border-radius: 8px; /* Bo tron hon */
                color: {SUBTEXT_COLOR};
                font-family: "Segoe Fluent Icons, Segoe MDL2 Assets, Segoe UI Symbol"; /* Font cho icon min,max,close */
                font-size: 10pt; /* Kich thuoc icon */
                font-weight: normal;
                min-width: 36px; max-width: 36px;
                min-height: 36px; max-height: 36px;
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
            self.btn_maximize_restore.setText("□") # Ky tu Unicode chuan hon
        else:
            self.window().showMaximized()
            self.btn_maximize_restore.setText("") # Icon restore tu font Fluent Icons

    def setTitle(self, title_key="app_title_on_bar"):
        self.title_label.setText(Translations.get(title_key))

    def setVersion(self, version_key="app_version_pyside6"):
        self.version_label.setText(Translations.get(version_key))

    def retranslate_ui(self):
        self.setTitle()
        self.setVersion()

        # Cap nhat ky tu cho nut Max/Restore khi thay doi ngon ngu/style
        if self.window().isMaximized():
            self.btn_maximize_restore.setText("") # Icon restore
        else:
            self.btn_maximize_restore.setText("□") # Icon maximize

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