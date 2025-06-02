import os
import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSizePolicy, QGraphicsOpacityEffect
)
from PySide6.QtCore import Qt, QPoint, QRect, QSize, QPropertyAnimation, QEasingCurve, QAbstractAnimation, Slot
from PySide6.QtGui import QPixmap, QIcon, QMouseEvent, QFont

from .constants import (
    RESIZE_MARGIN, NO_EDGE, TOP_EDGE, BOTTOM_EDGE, LEFT_EDGE, RIGHT_EDGE,
    WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT,
    WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT,
    ASSETS_DIR_NAME, DEFAULT_ICON_NAME, DEFAULT_BACKGROUND_NAME,
    TITLE_BAR_BG_COLOR, WINDOW_BG_COLOR
)
from .custom_title_bar import CustomTitleBar


class BaseMainWindow(QMainWindow):
    def __init__(self, base_app_path):
        super().__init__()
        self.base_app_path = base_app_path # path toi thu muc ung dung (Doc_Project_Tool)

        self._setup_window_properties()
        self._load_assets()
        self._init_ui_elements()
        self._apply_initial_styles()

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

        self.setMouseTracking(True) # De bat su kien hover cho resize

    def _setup_window_properties(self):
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)

    def _load_assets(self):
        assets_path = os.path.join(self.base_app_path, ASSETS_DIR_NAME)
        icon_path = os.path.join(assets_path, DEFAULT_ICON_NAME)
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        self.background_image_path = os.path.join(assets_path, DEFAULT_BACKGROUND_NAME)
        self.original_pixmap = QPixmap(self.background_image_path)
        if self.original_pixmap.isNull():
            print(f"Khong the tai hinh nen: {self.background_image_path}")


    def _init_ui_elements(self):
        self.main_container_widget = QWidget()
        self.main_container_widget.setObjectName("mainContainerWidget")
        self.setCentralWidget(self.main_container_widget)

        self.overall_layout = QVBoxLayout(self.main_container_widget)
        self.overall_layout.setContentsMargins(0, 0, 0, 0)
        self.overall_layout.setSpacing(0)

        self.custom_title_bar = CustomTitleBar(self)
        self.overall_layout.addWidget(self.custom_title_bar)

        self.content_area_with_background = QWidget() # Widget chua BG va content chinh
        self.content_area_with_background.setObjectName("contentAreaWithBackground")
        content_area_layout = QVBoxLayout(self.content_area_with_background)
        content_area_layout.setContentsMargins(0,0,0,0)
        content_area_layout.setSpacing(0)
        
        self.background_label = QLabel(self.content_area_with_background)
        self.background_label.setObjectName("backgroundLabel")
        self.background_label.setSizePolicy(QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Ignored)
        self.background_label.lower() # BG luon o duoi

        if self.original_pixmap.isNull():
            self.background_label.setText("Khong tim thay hinh nen")
            self.background_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Content chinh se duoc them vao content_area_layout boi lop con
        self.main_content_widget = QWidget() # Placeholder cho lop con them tabwidget vao day
        self.main_content_widget.setObjectName("mainContentWidget")
        content_area_layout.addWidget(self.main_content_widget)

        self.overall_layout.addWidget(self.content_area_with_background)
        
    def _apply_initial_styles(self):
        # Style co ban, QSS chi tiet se o lop con hoac file rieng
        self.main_container_widget.setStyleSheet(f"background-color: {WINDOW_BG_COLOR}; border-radius: 10px;")
        if self.original_pixmap.isNull():
             self.background_label.setStyleSheet(f"background-color: {WINDOW_BG_COLOR}; color: white; border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        else:
             self.background_label.setStyleSheet("border-bottom-left-radius: 10px; border-bottom-right-radius: 10px;")
        self.main_content_widget.setStyleSheet("background-color: transparent;")


    def _update_background_pixmap(self):
        if hasattr(self, 'background_label') and not self.original_pixmap.isNull():
            # Kich thuoc cua content_area_with_background
            bg_container_size = self.content_area_with_background.size()
            if bg_container_size.width() <= 0 or bg_container_size.height() <= 0:
                return

            scaled_pixmap = self.original_pixmap.scaled(
                bg_container_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            )
            self.background_label.setPixmap(scaled_pixmap)
            self.background_label.setGeometry(0, 0, bg_container_size.width(), bg_container_size.height())

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._update_background_pixmap()
        # Dieu chinh vi tri content_widget de no nam tren background_label
        if hasattr(self, 'main_content_widget') and hasattr(self, 'background_label'):
            self.main_content_widget.setGeometry(self.background_label.geometry())
            self.main_content_widget.raise_()


    def showEvent(self, event):
        super().showEvent(event)
        self._update_background_pixmap()
        if hasattr(self, 'main_content_widget') and hasattr(self, 'background_label'):
             self.main_content_widget.setGeometry(self.background_label.geometry())
             self.main_content_widget.raise_()

        if not self._first_show_animation_done:
            self._first_show_animation_done = True
            if not self.opacity_animation_open:
                self.opacity_animation_open = QPropertyAnimation(self, b"windowOpacity", self)
                self.opacity_animation_open.setDuration(480)
                self.opacity_animation_open.setEasingCurve(QEasingCurve.Type.InOutSine)
            self.setWindowOpacity(0.0)
            self.opacity_animation_open.setStartValue(0.0)
            self.opacity_animation_open.setEndValue(1.0)
            self.opacity_animation_open.start()
        
    def _get_current_resize_edge(self, local_pos: QPoint) -> int:
        edge = NO_EDGE
        rect = self.rect()
        if local_pos.x() < RESIZE_MARGIN: edge |= LEFT_EDGE
        if local_pos.x() > rect.width() - RESIZE_MARGIN: edge |= RIGHT_EDGE
        if local_pos.y() < RESIZE_MARGIN: edge |= TOP_EDGE
        if local_pos.y() > rect.height() - RESIZE_MARGIN: edge |= BOTTOM_EDGE
        return edge

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            local_pos = event.position().toPoint()
            global_pos = event.globalPosition().toPoint()
            
            self._resize_edge = self._get_current_resize_edge(local_pos)
            is_on_title_bar_geom = self.custom_title_bar.geometry().contains(local_pos)

            if self._resize_edge != NO_EDGE and not is_on_title_bar_geom :
                self._is_resizing = True
                self._is_dragging = False
                self._resize_start_mouse_pos = global_pos
                self._resize_start_window_geometry = self.geometry()
                event.accept()
                return
            
            interactive_widgets_on_title = self.custom_title_bar.findChildren(QWidget) # rong hon
            is_on_interactive_title_widget = False
            for child_widget in interactive_widgets_on_title:
                if child_widget.isVisible() and child_widget.geometry().contains(self.custom_title_bar.mapFromGlobal(global_pos)):
                    # Kiem tra xem co phai la QLabel ko, neu la title_label thi bo qua
                    if isinstance(child_widget, QLabel) and child_widget == self.custom_title_bar.title_label:
                        continue
                    is_on_interactive_title_widget = True
                    break
            
            if is_on_title_bar_geom and not is_on_interactive_title_widget:
                self._is_dragging = True
                self._is_resizing = False
                self._drag_start_pos = global_pos - self.frameGeometry().topLeft()
                event.accept()
                return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        local_pos = event.position().toPoint()
        if event.buttons() & Qt.LeftButton:
            if self._is_resizing:
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
            elif self._is_dragging:
                self.move(event.globalPosition().toPoint() - self._drag_start_pos)
                event.accept()
                return

        if not (self._is_resizing or self._is_dragging):
            current_hover_edge = self._get_current_resize_edge(local_pos)
            is_on_title_bar_geom = self.custom_title_bar.geometry().contains(local_pos)

            if is_on_title_bar_geom: # Neu tren title bar, ko doi cursor (tru khi la TOP_EDGE)
                 if current_hover_edge & TOP_EDGE : self.setCursor(Qt.SizeVerCursor)
                 else: self.unsetCursor()
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
                self.unsetCursor()
                event.accept()
                return
        super().mouseReleaseEvent(event)

    def closeEvent(self, event):
        if self._animation_is_closing_flag:
            event.accept()
            return

        if not self.opacity_animation_close:
            self.opacity_animation_close = QPropertyAnimation(self, b"windowOpacity", self)
            self.opacity_animation_close.setDuration(320)
            self.opacity_animation_close.setEasingCurve(QEasingCurve.Type.InOutSine)
            self.opacity_animation_close.finished.connect(self._handle_close_animation_finished)

        if self.opacity_animation_close.state() == QAbstractAnimation.State.Running:
            self.opacity_animation_close.stop() # Dung anim hien tai neu co

        self.opacity_animation_close.setStartValue(self.windowOpacity())
        self.opacity_animation_close.setEndValue(0.0)
        self.opacity_animation_close.start()
        event.ignore() # Bo qua su kien close goc, se close sau khi anim xong

    @Slot()
    def _handle_close_animation_finished(self):
        self._animation_is_closing_flag = True
        self.close() # Bay gio moi close that