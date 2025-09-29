# Core/base_main_window.py
import os
import sys
import json
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSizePolicy, QGraphicsOpacityEffect, QMessageBox, QPushButton
)
from PySide6.QtCore import Qt, QPoint, QRect, QSize, QPropertyAnimation, QEasingCurve, QAbstractAnimation, Slot
from PySide6.QtGui import QPixmap, QIcon, QMouseEvent, QFont

from .constants import (
    RESIZE_MARGIN, NO_EDGE, TOP_EDGE, BOTTOM_EDGE, LEFT_EDGE, RIGHT_EDGE,
    WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    ASSETS_DIR_NAME, DEFAULT_ICON_NAME, DEFAULT_BACKGROUND_NAME,
    WINDOW_BG_COLOR, CONFIG_FILE_NAME, DEFAULT_LANGUAGE,
    NORMAL_FONT_SIZE
)
from .custom_title_bar import CustomTitleBar
from .translations import Translations


class BaseMainWindow(QMainWindow):
    def __init__(self, base_app_path):
        super().__init__()
        self.base_app_path = base_app_path
        self.config_file_path = os.path.join(self.base_app_path, "Core", CONFIG_FILE_NAME)

        self._load_app_config()

        self._setup_window_properties()
        self._load_assets()
        self._init_ui_elements()
        self._apply_initial_styles() # Styles se dc ap dung o day

        self._is_dragging = False
        self._drag_start_pos = QPoint()
        self._is_resizing = False
        self._resize_edge = NO_EDGE
        self._resize_start_mouse_pos = QPoint()
        self._resize_start_window_geometry = QRect()

        self._first_show_animation_done = False
        self._animation_is_closing_flag = False
        self.opacity_animation_open = None
        self.opacity_animation_close = None

        self.setMouseTracking(True)
        self.custom_title_bar.language_changed_signal.connect(self._handle_language_change)

    def _load_app_config(self):
        try:
            if os.path.exists(self.config_file_path):
                with open(self.config_file_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                Translations.set_language(config.get("language", DEFAULT_LANGUAGE))

                geom_array = config.get("window_geometry")
                if geom_array and len(geom_array) == 4:
                    self._initial_geometry = QRect(*geom_array)
                else:
                    self._initial_geometry = QRect(100, 100, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

                self._initial_maximized = config.get("window_maximized", False)

            else:
                Translations.set_language(DEFAULT_LANGUAGE)
                self._initial_geometry = QRect(100, 100, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
                self._initial_maximized = False
                self._save_app_config()
        except Exception as e:
            # Loi tai config
            print(f"Loi tai config: {e}. SD MDinh.")
            Translations.set_language(DEFAULT_LANGUAGE)
            self._initial_geometry = QRect(100, 100, WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
            self._initial_maximized = False

    def _save_app_config(self):
        config = {
            "language": Translations.current_lang,
            "window_geometry": self.normalGeometry().getRect() if self.isMaximized() else self.geometry().getRect(),
            "window_maximized": self.isMaximized()
        }
        try:
            os.makedirs(os.path.dirname(self.config_file_path), exist_ok=True)
            with open(self.config_file_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(Translations.get("config_file_save_error", path=self.config_file_path, error=str(e)))


    def _setup_window_properties(self):
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)

        initial_geom = QRect(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT, 100, 100) # MDinh
        if hasattr(self, '_initial_geometry'):
            initial_geom = self._initial_geometry
        
            # KTra xem window co nam ngoai man hinh ko
            screens = QApplication.screens()
            is_on_screen = False
            for screen in screens:
                if screen.availableGeometry().intersects(initial_geom):
                    is_on_screen = True
                    break
            
            if not is_on_screen:
                # Neu nam ngoai, can giua vao man hinh chinh
                primary_screen_rect = QApplication.primaryScreen().availableGeometry()
                initial_geom.moveCenter(primary_screen_rect.center())
        
        self.setGeometry(initial_geom)

        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setWindowTitle(Translations.get("app_window_title_default"))

    def _load_assets(self):
        assets_path = os.path.join(self.base_app_path, ASSETS_DIR_NAME)
        icon_path = os.path.join(assets_path, DEFAULT_ICON_NAME)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.background_image_path = os.path.join(assets_path, DEFAULT_BACKGROUND_NAME)
        self.original_pixmap = QPixmap(self.background_image_path)
        if self.original_pixmap.isNull():
            print(Translations.get("base_mw_bg_load_fail_console", path=self.background_image_path))


    def _init_ui_elements(self):
        self.main_container_widget = QWidget()
        self.main_container_widget.setObjectName("mainContainerWidget")
        self.setCentralWidget(self.main_container_widget)

        self.overall_layout = QVBoxLayout(self.main_container_widget)
        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.setSpacing(0)

        self.custom_title_bar = CustomTitleBar(self)
        self.overall_layout.addWidget(self.custom_title_bar)

        self.content_area_with_background = QWidget()
        self.content_area_with_background.setObjectName("contentAreaWithBackground")

        content_area_main_layout = QVBoxLayout(self.content_area_with_background)
        content_area_main_layout.setContentsMargins(0,0,0,0) # Margin cua vung content
        content_area_main_layout.setSpacing(0)

        self.background_label = QLabel(self.content_area_with_background)
        self.background_label.setObjectName("backgroundLabel")
        self.background_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)

        if self.original_pixmap.isNull():
            self.background_label.setText(Translations.get("base_mw_bg_not_found_ui"))
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_content_widget = QWidget() # Day la noi ProjectDocApp se them UI vao
        self.main_content_widget.setObjectName("mainContentWidget")
        content_area_main_layout.addWidget(self.main_content_widget)

        self.overall_layout.addWidget(self.content_area_with_background)

    def _apply_initial_styles(self):
        # Font chung cho app, co the duoc ProjectDocApp ghi de neu can
        font_family = "Segoe UI, Arial, sans-serif"
        if Translations.current_lang == Translations.LANG_JA:
            font_family = "Meiryo, Segoe UI, Arial, sans-serif"

        app_font = QFont(font_family, NORMAL_FONT_SIZE)
        QApplication.setFont(app_font) # Nen set font mot lan o day

        # Style cho container chinh cua cua so
        # Radius nen giong voi radius cua contentAreaWithBackground hoac TabWidget ben trong main_app
        self.main_container_widget.setStyleSheet(f"""
            QWidget#mainContainerWidget {{
                background-color: {WINDOW_BG_COLOR};
                border-radius: 10px; /* Dong bo voi border-radius cua contentAreaWithBackground */
            }}
        """)

        # Style cho vung chua hinh nen va content chinh
        # contentAreaWithBackground se co border radius o goc duoi
        # mainContentWidget se trong suot de hinh nen hien thi
        bg_label_style = f"""
            QWidget#contentAreaWithBackground {{
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: transparent; /* Cho phep nen cua mainContainerWidget hien thi */
            }}
            QLabel#backgroundLabel {{
                border-bottom-left-radius: 10px; /* Quan trong de hinh nen bo tron theo */
                border-bottom-right-radius: 10px;
            }}
            QWidget#mainContentWidget {{
                background-color: transparent;
                 /* padding se duoc ProjectDocApp quyet dinh */
            }}
        """

        if self.original_pixmap.isNull():
            bg_label_style += f"""
                QLabel#backgroundLabel {{
                    background-color: {WINDOW_BG_COLOR}; /* Mau nen fallback */
                    color: {Translations.get("base_mw_bg_not_found_ui")};
                    font-family: "{font_family}";
                }}
            """
        self.content_area_with_background.setStyleSheet(bg_label_style)
        self.custom_title_bar._apply_styles() # Title bar tu style


    def _update_background_pixmap(self):
        if hasattr(self, 'background_label') and not self.original_pixmap.isNull():
            bg_container_size = self.content_area_with_background.size()
            if bg_container_size.width() <= 0 or bg_container_size.height() <= 0:
                return

            scaled_pixmap = self.original_pixmap.scaled(
                bg_container_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding, # De anh nen full vung
                Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            # background_label nen fill content_area_with_background
            self.background_label.setGeometry(self.content_area_with_background.rect())


    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_background_pixmap()

        if hasattr(self, 'main_content_widget') and hasattr(self, 'background_label'):
            # Dam bao main_content_widget luon nam tren background_label
            self.main_content_widget.raise_()
            self.background_label.lower()


    def showEvent(self, event):
        super().showEvent(event)
        if hasattr(self, '_initial_maximized') and self._initial_maximized:
            self.showMaximized()
            if hasattr(self.custom_title_bar, 'btn_maximize_restore'):
                 # Su dung icon khi maximized
                 self.custom_title_bar.btn_maximize_restore.setText("")


        self._update_background_pixmap()
        if hasattr(self, 'main_content_widget') and hasattr(self, 'background_label'):
             self.main_content_widget.raise_()
             self.background_label.lower()

        if not self._first_show_animation_done:
            self._first_show_animation_done = True
            if not self.opacity_animation_open:
                self.opacity_animation_open = QPropertyAnimation(self, b"windowOpacity", self)
                self.opacity_animation_open.setDuration(500) # T.gian mo cua so, nhanh hon chut
                self.opacity_animation_open.setEasingCurve(QEasingCurve.Type.OutQuad) # Easing curve khac
            self.setWindowOpacity(0.0)
            self.opacity_animation_open.setStartValue(0.0)
            self.opacity_animation_open.setEndValue(1.0)
            self.opacity_animation_open.start()

    def _get_current_resize_edge(self, local_pos: QPoint) -> int:
        edge = NO_EDGE
        rect = self.rect()
        # Giam margin resize de tranh chong lan voi title bar
        actual_resize_margin = RESIZE_MARGIN if not self.custom_title_bar.geometry().contains(local_pos) else RESIZE_MARGIN // 2
        if local_pos.x() < actual_resize_margin: edge |= LEFT_EDGE
        if local_pos.x() > rect.width() - actual_resize_margin: edge |= RIGHT_EDGE
        if local_pos.y() < actual_resize_margin: edge |= TOP_EDGE
        if local_pos.y() > rect.height() - actual_resize_margin: edge |= BOTTOM_EDGE
        return edge

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            local_pos = event.position().toPoint()
            global_pos = event.globalPosition().toPoint()

            self._resize_edge = self._get_current_resize_edge(local_pos)
            is_on_title_bar_geom = self.custom_title_bar.geometry().contains(local_pos)

            if self._resize_edge != NO_EDGE and not self.isMaximized() and not is_on_title_bar_geom : # Ko resize khi maximized
                self._is_resizing = True
                self._is_dragging = False
                self._resize_start_mouse_pos = global_pos
                self._resize_start_window_geometry = self.geometry()
                event.accept()
                return

            interactive_widgets_on_title = (
                self.custom_title_bar.findChildren(QPushButton) +
                [self.custom_title_bar.lang_combo]
            )
            is_on_interactive_title_widget = False
            for child_widget in interactive_widgets_on_title:
                if child_widget == self.custom_title_bar.title_label: continue

                if child_widget.isVisible() and child_widget.geometry().contains(self.custom_title_bar.mapFromGlobal(global_pos)):
                    is_on_interactive_title_widget = True
                    break

            if is_on_title_bar_geom and not is_on_interactive_title_widget:
                if self.isMaximized(): # Neu maximized, chi cho phep drag neu double click
                    if event.type() == QMouseEvent.Type.MouseButtonDblClick:
                        self.custom_title_bar._toggle_maximize_restore() # Day la cach gian tiep
                else:
                    self._is_dragging = True
                self._is_resizing = False # Reset resizing
                self._drag_start_pos = global_pos - self.frameGeometry().topLeft()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        local_pos = event.position().toPoint()
        if event.buttons() & Qt.LeftButton:
            if self._is_resizing and not self.isMaximized():
                delta = event.globalPosition().toPoint() - self._resize_start_mouse_pos
                start_geom = self._resize_start_window_geometry
                new_geom = QRect(start_geom)
                min_w, min_h = self.minimumSize().width(), self.minimumSize().height()

                if self._resize_edge & LEFT_EDGE:
                    new_width = max(min_w, start_geom.width() - delta.x())
                    new_geom.setLeft(start_geom.right() - new_width)
                    new_geom.setWidth(new_width)
                if self._resize_edge & RIGHT_EDGE:
                    new_geom.setWidth(max(min_w, start_geom.width() + delta.x()))
                if self._resize_edge & TOP_EDGE:
                    new_height = max(min_h, start_geom.height() - delta.y())
                    new_geom.setTop(start_geom.bottom() - new_height)
                    new_geom.setHeight(new_height)
                if self._resize_edge & BOTTOM_EDGE:
                    new_geom.setHeight(max(min_h, start_geom.height() + delta.y()))

                self.setGeometry(new_geom)
                event.accept()
                return
            elif self._is_dragging and not self.isMaximized(): # Ko drag khi maximized theo kieu thong thuong
                self.move(event.globalPosition().toPoint() - self._drag_start_pos)
                event.accept()
                return

        if not (self._is_resizing or self._is_dragging) and not self.isMaximized():
            current_hover_edge = self._get_current_resize_edge(local_pos)
            is_on_title_bar_geom = self.custom_title_bar.geometry().contains(local_pos)

            is_on_interactive_title_widget = False
            interactive_widgets_on_title = (
                self.custom_title_bar.findChildren(QPushButton) +
                [self.custom_title_bar.lang_combo]
            )
            for child_widget in interactive_widgets_on_title:
                 if child_widget == self.custom_title_bar.title_label: continue
                 if child_widget.isVisible() and child_widget.geometry().contains(self.custom_title_bar.mapFromGlobal(event.globalPosition().toPoint())):
                    is_on_interactive_title_widget = True
                    break

            if is_on_interactive_title_widget:
                self.unsetCursor()
            elif is_on_title_bar_geom:
                 if current_hover_edge & TOP_EDGE : self.setCursor(Qt.SizeVerCursor)
                 else: self.unsetCursor() # Mac dinh la mui ten tren title bar
            elif current_hover_edge == (TOP_EDGE | LEFT_EDGE) or current_hover_edge == (BOTTOM_EDGE | RIGHT_EDGE):
                self.setCursor(Qt.SizeFDiagCursor)
            elif current_hover_edge == (TOP_EDGE | RIGHT_EDGE) or current_hover_edge == (BOTTOM_EDGE | LEFT_EDGE):
                self.setCursor(Qt.SizeBDiagCursor)
            elif current_hover_edge & LEFT_EDGE or current_hover_edge & RIGHT_EDGE:
                self.setCursor(Qt.SizeHorCursor)
            elif current_hover_edge & TOP_EDGE or current_hover_edge & BOTTOM_EDGE:
                self.setCursor(Qt.SizeVerCursor)
            else:
                self.unsetCursor()
        elif self.isMaximized(): # Neu maximized, khong hien thi con tro resize
            self.unsetCursor()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            changed_state = False
            if self._is_resizing:
                self._is_resizing = False
                changed_state = True
            if self._is_dragging:
                self._is_dragging = False
                changed_state = True

            if changed_state:
                self._resize_edge = NO_EDGE
                self.unsetCursor() # Reset cursor ve mac dinh
                if not self.isMaximized(): self._save_app_config() # Luu config neu thay doi kich thuoc/vi tri
                event.accept()
                return
        super().mouseReleaseEvent(event)

    def retranslate_base_ui(self):
        self.setWindowTitle(Translations.get("app_window_title_default"))
        self.custom_title_bar.retranslate_ui()
        if self.original_pixmap.isNull():
            self.background_label.setText(Translations.get("base_mw_bg_not_found_ui"))
        self._apply_initial_styles() # Ap dung lai style de cap nhat font family


    @Slot(str)
    def _handle_language_change(self, lang_code):
        Translations.set_language(lang_code)
        self.retranslate_base_ui() # Goi truoc de title bar cap nhat dung font

        if hasattr(self, 'retranslate_app_specific_ui'):
            self.retranslate_app_specific_ui() # Goi sau de cac widget con cap nhat

        self._save_app_config()

    def closeEvent(self, event):
        if not self._animation_is_closing_flag and \
           not (self.opacity_animation_close and self.opacity_animation_close.state() == QAbstractAnimation.State.Running) :
            self._save_app_config() # Luu config truoc khi bat dau animation dong

        if self._animation_is_closing_flag: # Neu da trong qua trinh dong thuc su
            event.accept()
            return

        # Neu animation dong dang chay, bo qua event nay
        if self.opacity_animation_close and self.opacity_animation_close.state() == QAbstractAnimation.State.Running:
            event.ignore()
            return

        if not self.opacity_animation_close:
            self.opacity_animation_close = QPropertyAnimation(self, b"windowOpacity", self)
            self.opacity_animation_close.setDuration(350) # T.gian dong cua so, nhanh hon chut
            self.opacity_animation_close.setEasingCurve(QEasingCurve.Type.InQuad) # Easing curve khac
            self.opacity_animation_close.finished.connect(self._handle_close_animation_finished)

        self.opacity_animation_close.setStartValue(self.windowOpacity())
        self.opacity_animation_close.setEndValue(0.0)
        self.opacity_animation_close.start()
        event.ignore() # Bo qua event close goc de cho animation chay

    @Slot()
    def _handle_close_animation_finished(self):
        self._animation_is_closing_flag = True # Dat co
        self.close() # Goi lai close(), luc nay se di vao nhanh _animation_is_closing_flag