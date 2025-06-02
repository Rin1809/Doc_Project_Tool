# Core/main_app.py
import os
import sys
import json
from datetime import datetime
import subprocess
import webbrowser
from threading import Thread

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QLineEdit, QListWidget, QListWidgetItem,
    QRadioButton, QCheckBox, QTabWidget, QProgressBar, QPlainTextEdit,
    QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QFormLayout
)
from PySide6.QtCore import Qt, Signal, Slot, QThread, QObject, QEventLoop, QAbstractAnimation
from PySide6.QtGui import QFont, QDesktopServices, QClipboard, QPalette, QColor, QIcon

from .base_main_window import BaseMainWindow
from .app_logic import tao_tai_lieu_du_an
from .gui_utils import format_output_for_tkinter
from .translations import Translations
from .constants import (
    DEFAULT_EXCLUDED_SUBDIRS, DEFAULT_EXCLUDED_FILES,
    DEFAULT_OUTPUT_DIR, DEFAULT_BASE_FILENAME,
    HISTORY_FILE, MAX_HISTORY_ITEMS,
    NORMAL_FONT_SIZE, HEADER_FONT_SIZE, SMALL_FONT_SIZE,
    TEXT_COLOR, SUBTEXT_COLOR, INPUT_BG_COLOR, INPUT_BORDER_COLOR, INPUT_FOCUS_BORDER_COLOR, INPUT_PLACEHOLDER_COLOR,
    PRIMARY_COLOR, ACCENT_COLOR, HOVER_COLOR, SUCCESS_COLOR, WARNING_COLOR, ERROR_COLOR,
    CONTAINER_BG_COLOR, WINDOW_BG_COLOR, SELECTED_COLOR, TEXT_HOVER_COLOR, ACCENT_GLOW_COLOR,
    SCROLLBAR_BG_COLOR, SCROLLBAR_HANDLE_COLOR, SCROLLBAR_HANDLE_HOVER_COLOR, SCROLLBAR_HANDLE_PRESSED_COLOR
)


class DocWorker(QObject):
    finished = Signal(tuple)
    progress_update = Signal(str)
    error_occurred = Signal(str)

    def __init__(self, project_dirs, excluded_subdirs, excluded_files,
                 base_filename, output_dir, verbose, output_format):
        super().__init__()
        self.project_dirs = project_dirs
        self.excluded_subdirs = excluded_subdirs
        self.excluded_files = excluded_files
        self.base_filename = base_filename
        self.output_dir = output_dir
        self.verbose = verbose
        self.output_format = output_format

    @Slot()
    def run(self):
        try:
            self.progress_update.emit(Translations.get("worker_starting_generation"))
            result = tao_tai_lieu_du_an(
                self.project_dirs, self.excluded_subdirs, self.excluded_files,
                self.base_filename, self.output_dir, self.verbose, self.output_format
            )
            self.finished.emit(result)
        except Exception as e:
            self.error_occurred.emit(Translations.get("worker_error_generic", error=str(e)))


class ProjectDocApp(BaseMainWindow):
    def __init__(self, base_app_path):
        super().__init__(base_app_path) # Goi __init__ cua BaseMainWindow

        self._init_app_variables()
        self._create_ui_layout_and_tabs()
        self._apply_qss_styles() # QSS se duoc ap dung o day
        self._connect_signals()
        self.load_history_from_file()

        self.retranslate_app_specific_ui() # Goi sau khi UI da duoc tao va style
        self._update_control_states()

    def _init_app_variables(self):
        self.project_dirs = []
        self.excluded_subdirs_list = list(DEFAULT_EXCLUDED_SUBDIRS)
        self.excluded_files_list = list(DEFAULT_EXCLUDED_FILES)
        self.output_dir_path = DEFAULT_OUTPUT_DIR
        self.base_filename_str = DEFAULT_BASE_FILENAME
        self.verbose_state = False
        self.output_format_str = "txt"
        self.last_main_output_file = None
        self.history_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), HISTORY_FILE)
        self.history_data = []
        self.worker_thread = None
        self.doc_worker = None
        self._is_exiting_initiated_by_user = False


    def _create_ui_layout_and_tabs(self):
        # main_content_widget da duoc tao trong BaseMainWindow
        content_layout = QVBoxLayout(self.main_content_widget)
        content_layout.setContentsMargins(20, 15, 20, 15) # padding noi dung chinh
        content_layout.setSpacing(15) # khoang cach giua tab widget va status bar

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabWidget")

        self._create_config_tab_content()
        self._create_advanced_tab_content()
        self._create_history_tab_content()
        self._create_output_tab_content()

        self.tab_widget.addTab(self.tab_config, "...")
        self.tab_widget.addTab(self.tab_advanced, "...")
        self.tab_widget.addTab(self.tab_history, "...")
        self.tab_widget.addTab(self.tab_output, "...")

        content_layout.addWidget(self.tab_widget)
        self._create_status_bar(content_layout)

    def _create_config_tab_content(self):
        self.tab_config = QWidget()
        self.tab_config.setObjectName("configTab")
        layout = QVBoxLayout(self.tab_config)
        layout.setSpacing(20) # khoang cach group

        self.dir_group = QGroupBox()
        self.dir_group.setObjectName("configGroup")
        dir_layout = QVBoxLayout(self.dir_group)
        dir_layout.setSpacing(10) # KC trong group

        self.project_dir_list_widget = QListWidget()
        self.project_dir_list_widget.setObjectName("projectDirList")
        self.project_dir_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        dir_layout.addWidget(self.project_dir_list_widget)

        dir_buttons_layout = QHBoxLayout()
        dir_buttons_layout.setSpacing(8)
        self.add_dir_btn = QPushButton()
        self.add_dir_btn.setObjectName("primaryButton")
        self.remove_dir_btn = QPushButton()
        self.remove_dir_btn.setObjectName("warningButton")
        dir_buttons_layout.addWidget(self.add_dir_btn)
        dir_buttons_layout.addWidget(self.remove_dir_btn)
        dir_buttons_layout.addStretch()
        dir_layout.addLayout(dir_buttons_layout)
        layout.addWidget(self.dir_group)

        self.output_group = QGroupBox()
        self.output_group.setObjectName("configGroup")
        output_layout = QFormLayout(self.output_group)
        output_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        output_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        output_layout.setHorizontalSpacing(10) # KC giua label va field
        output_layout.setVerticalSpacing(12)  # KC giua cac row

        self.output_dir_label_widget = QLabel()
        self.output_dir_entry = QLineEdit(self.output_dir_path)
        self.browse_output_btn = QPushButton()
        self.browse_output_btn.setObjectName("secondaryButton")
        output_dir_hbox = QHBoxLayout()
        output_dir_hbox.setSpacing(8)
        output_dir_hbox.addWidget(self.output_dir_entry, 1) # Cho entry gian ra
        output_dir_hbox.addWidget(self.browse_output_btn)
        output_layout.addRow(self.output_dir_label_widget, output_dir_hbox)

        self.base_filename_label_widget = QLabel()
        self.base_filename_entry = QLineEdit(self.base_filename_str)
        output_layout.addRow(self.base_filename_label_widget, self.base_filename_entry)

        self.output_format_label_widget = QLabel()
        format_hbox = QHBoxLayout()
        format_hbox.setSpacing(15) # KC giua radio/checkbox
        self.txt_radio = QRadioButton()
        self.txt_radio.setChecked(True)
        self.md_radio = QRadioButton()
        self.verbose_checkbox = QCheckBox()
        format_hbox.addWidget(self.txt_radio)
        format_hbox.addWidget(self.md_radio)
        format_hbox.addSpacerItem(QSpacerItem(30,0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        format_hbox.addWidget(self.verbose_checkbox)
        format_hbox.addStretch()
        output_layout.addRow(self.output_format_label_widget, format_hbox)
        layout.addWidget(self.output_group)

        self.run_button = QPushButton()
        self.run_button.setObjectName("runButton")
        self.run_button.setFixedHeight(50) # nut chay cao hon, to hon
        layout.addWidget(self.run_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def _create_advanced_tab_content(self):
        self.tab_advanced = QWidget()
        self.tab_advanced.setObjectName("advancedTab")
        layout = QVBoxLayout(self.tab_advanced)
        layout.setSpacing(20)

        self.excluded_dirs_group = QGroupBox()
        self.excluded_dirs_group.setObjectName("configGroup")
        excluded_dirs_layout = QVBoxLayout(self.excluded_dirs_group)
        self.excluded_subdirs_entry = QLineEdit(", ".join(self.excluded_subdirs_list))
        self.excluded_subdirs_entry.setPlaceholderText(Translations.get("excluded_dirs_group_title")) # Them placeholder
        excluded_dirs_layout.addWidget(self.excluded_subdirs_entry)
        layout.addWidget(self.excluded_dirs_group)

        self.excluded_files_group = QGroupBox()
        self.excluded_files_group.setObjectName("configGroup")
        excluded_files_layout = QVBoxLayout(self.excluded_files_group)
        self.excluded_files_entry = QLineEdit(", ".join(self.excluded_files_list))
        self.excluded_files_entry.setPlaceholderText(Translations.get("excluded_files_group_title")) # Them placeholder
        excluded_files_layout.addWidget(self.excluded_files_entry)
        layout.addWidget(self.excluded_files_group)

        layout.addStretch()

    def _create_history_tab_content(self):
        self.tab_history = QWidget()
        self.tab_history.setObjectName("historyTab")
        layout = QVBoxLayout(self.tab_history)
        layout.setSpacing(15) # KC giua group va cac element khac (neu co)

        self.history_group = QGroupBox()
        self.history_group.setObjectName("configGroup")
        history_layout = QVBoxLayout(self.history_group)
        history_layout.setSpacing(10)

        self.history_list_widget = QListWidget()
        self.history_list_widget.setObjectName("historyList")
        history_layout.addWidget(self.history_list_widget)

        history_buttons_layout = QHBoxLayout()
        history_buttons_layout.setSpacing(8)
        self.load_history_btn = QPushButton()
        self.load_history_btn.setObjectName("primaryButton")
        self.delete_history_btn = QPushButton()
        self.delete_history_btn.setObjectName("warningButton")
        self.delete_all_history_btn = QPushButton()
        self.delete_all_history_btn.setObjectName("errorButton")

        history_buttons_layout.addWidget(self.load_history_btn)
        history_buttons_layout.addWidget(self.delete_history_btn)
        history_buttons_layout.addStretch()
        history_buttons_layout.addWidget(self.delete_all_history_btn)
        history_layout.addLayout(history_buttons_layout)
        layout.addWidget(self.history_group)

    def _create_output_tab_content(self):
        self.tab_output = QWidget()
        self.tab_output.setObjectName("outputTab")
        layout = QVBoxLayout(self.tab_output)
        layout.setSpacing(15)

        self.output_text_edit = QPlainTextEdit()
        self.output_text_edit.setObjectName("outputTextEdit")
        self.output_text_edit.setReadOnly(True)
        layout.addWidget(self.output_text_edit)

        output_buttons_layout = QHBoxLayout()
        output_buttons_layout.setSpacing(8)
        self.copy_output_btn = QPushButton()
        self.copy_output_btn.setObjectName("secondaryButton")
        self.clear_output_btn = QPushButton()
        self.clear_output_btn.setObjectName("warningButton")
        self.ai_studio_btn = QPushButton()
        self.ai_studio_btn.setObjectName("accentButton")
        self.open_output_folder_btn = QPushButton()
        self.open_output_folder_btn.setObjectName("primaryButton")

        output_buttons_layout.addWidget(self.copy_output_btn)
        output_buttons_layout.addWidget(self.clear_output_btn)
        output_buttons_layout.addStretch()
        output_buttons_layout.addWidget(self.ai_studio_btn)
        output_buttons_layout.addWidget(self.open_output_folder_btn)
        layout.addLayout(output_buttons_layout)

    def _create_status_bar(self, parent_layout):
        status_bar_widget = QFrame()
        status_bar_widget.setObjectName("statusBar")
        status_bar_widget.setFixedHeight(35) # status bar cao hon chut
        status_layout = QHBoxLayout(status_bar_widget)
        status_layout.setContentsMargins(15, 0, 15, 0) # padding status bar
        status_layout.setSpacing(10) # KC giua label va progress bar

        self.status_label = QLabel(Translations.get("status_ready"))
        self.status_label.setObjectName("statusLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0,100)

        status_layout.addWidget(self.status_label, 1) # Cho label gian ra
        status_layout.addWidget(self.progress_bar, 1) # Progress bar cung gian ra
        parent_layout.addWidget(status_bar_widget)

    def _connect_signals(self):
        self.add_dir_btn.clicked.connect(self.add_project_directory)
        self.remove_dir_btn.clicked.connect(self.remove_project_directory)
        self.browse_output_btn.clicked.connect(self.browse_output_directory)
        self.run_button.clicked.connect(self.run_documentation_process)

        self.load_history_btn.clicked.connect(self.load_selected_history_item)
        self.delete_history_btn.clicked.connect(self.delete_selected_history_item)
        self.delete_all_history_btn.clicked.connect(self.delete_all_history)
        self.history_list_widget.itemDoubleClicked.connect(self.load_selected_history_item)

        self.copy_output_btn.clicked.connect(self.copy_output_to_clipboard)
        self.clear_output_btn.clicked.connect(self.clear_output_display)
        self.ai_studio_btn.clicked.connect(self.open_ai_studio_and_copy)
        self.open_output_folder_btn.clicked.connect(self.open_output_folder_path)

        self.txt_radio.toggled.connect(lambda: self._on_output_format_changed("txt", self.txt_radio.isChecked()))
        self.md_radio.toggled.connect(lambda: self._on_output_format_changed("markdown", self.md_radio.isChecked()))

    def retranslate_app_specific_ui(self):
        # Tieu de cua so va title bar da duoc BaseMainWindow xu ly
        # self.setWindowTitle(Translations.get("app_window_title_default"))
        # self.custom_title_bar.setTitle("app_title_on_bar")
        # self.custom_title_bar.setVersion("app_version_pyside6")

        # Cap nhat text cho cac tab
        tab_map = {
            self.tab_config: "config_tab_title",
            self.tab_advanced: "advanced_tab_title",
            self.tab_history: "history_tab_title",
            self.tab_output: "output_tab_title"
        }
        for tab_widget, translation_key in tab_map.items():
            if hasattr(self, 'tab_widget') and tab_widget:
                idx = self.tab_widget.indexOf(tab_widget)
                if idx != -1: self.tab_widget.setTabText(idx, Translations.get(translation_key))

        # Config Tab
        if hasattr(self, 'dir_group'): self.dir_group.setTitle(Translations.get("project_dir_group_title"))
        if hasattr(self, 'add_dir_btn'): self.add_dir_btn.setText(Translations.get("add_dir_button"))
        if hasattr(self, 'remove_dir_btn'): self.remove_dir_btn.setText(Translations.get("remove_dir_button"))
        if hasattr(self, 'output_group'): self.output_group.setTitle(Translations.get("output_settings_group_title"))
        if hasattr(self, 'output_dir_label_widget'): self.output_dir_label_widget.setText(Translations.get("output_dir_label"))
        if hasattr(self, 'browse_output_btn'): self.browse_output_btn.setText(Translations.get("browse_button"))
        if hasattr(self, 'base_filename_label_widget'): self.base_filename_label_widget.setText(Translations.get("base_filename_label"))
        if hasattr(self, 'output_format_label_widget'): self.output_format_label_widget.setText(Translations.get("output_format_label"))
        if hasattr(self, 'txt_radio'): self.txt_radio.setText(Translations.get("txt_radio_label"))
        if hasattr(self, 'md_radio'): self.md_radio.setText(Translations.get("md_radio_label"))
        if hasattr(self, 'verbose_checkbox'): self.verbose_checkbox.setText(Translations.get("verbose_checkbox_label"))
        if hasattr(self, 'run_button'): self.run_button.setText(Translations.get("run_button_text"))

        # Advanced Tab
        if hasattr(self, 'excluded_dirs_group'): self.excluded_dirs_group.setTitle(Translations.get("excluded_dirs_group_title"))
        if hasattr(self, 'excluded_subdirs_entry'): self.excluded_subdirs_entry.setPlaceholderText(Translations.get("excluded_dirs_group_title"))
        if hasattr(self, 'excluded_files_group'): self.excluded_files_group.setTitle(Translations.get("excluded_files_group_title"))
        if hasattr(self, 'excluded_files_entry'): self.excluded_files_entry.setPlaceholderText(Translations.get("excluded_files_group_title"))

        # History Tab
        if hasattr(self, 'history_group'): self.history_group.setTitle(Translations.get("history_group_title"))
        if hasattr(self, 'load_history_btn'): self.load_history_btn.setText(Translations.get("load_history_button"))
        if hasattr(self, 'delete_history_btn'): self.delete_history_btn.setText(Translations.get("delete_history_button"))
        if hasattr(self, 'delete_all_history_btn'): self.delete_all_history_btn.setText(Translations.get("delete_all_history_button"))
        self.populate_history_listbox()

        # Output Tab
        if hasattr(self, 'copy_output_btn'): self.copy_output_btn.setText(Translations.get("copy_output_button"))
        if hasattr(self, 'clear_output_btn'): self.clear_output_btn.setText(Translations.get("clear_output_button"))
        if hasattr(self, 'ai_studio_btn'): self.ai_studio_btn.setText(Translations.get("ai_studio_button"))
        if hasattr(self, 'open_output_folder_btn'): self.open_output_folder_btn.setText(Translations.get("open_output_folder_button"))

        # Status Bar
        if hasattr(self, 'status_label'):
            # Chi cap nhat neu la trang thai "Ready" ban dau
            is_ready_status = False
            current_text = self.status_label.text()
            for lang_code_check in Translations.lang_map.keys():
                if current_text == Translations.get("status_ready", lang=lang_code_check):
                    is_ready_status = True
                    break
            if is_ready_status:
                self.status_label.setText(Translations.get("status_ready"))

        self._apply_qss_styles() # Ap dung lai QSS de cap nhat font family neu ngon ngu thay doi


    def _on_output_format_changed(self, fmt, checked):
        if checked:
            self.output_format_str = fmt

    @Slot()
    def add_project_directory(self):
        directory = QFileDialog.getExistingDirectory(self, Translations.get("project_dir_group_title"))
        if directory:
            directory = os.path.abspath(directory)
            items = [self.project_dir_list_widget.item(i).text() for i in range(self.project_dir_list_widget.count())]
            if directory not in items:
                self.project_dir_list_widget.addItem(QListWidgetItem(directory))
                self.project_dirs.append(directory)
            else:
                QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("msg_dir_already_in_list_text"))
        self._update_control_states()


    @Slot()
    def remove_project_directory(self):
        selected_items = self.project_dir_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("msg_select_dir_to_remove_text"))
            return
        for item in selected_items:
            row = self.project_dir_list_widget.row(item)
            self.project_dir_list_widget.takeItem(row)
        self.project_dirs = [self.project_dir_list_widget.item(i).text() for i in range(self.project_dir_list_widget.count())]
        self._update_control_states()


    @Slot()
    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, Translations.get("output_dir_label"))
        if directory:
            self.output_dir_path = os.path.abspath(directory)
            self.output_dir_entry.setText(self.output_dir_path)
        self._update_control_states()

    def _get_current_config_from_ui(self):
        self.project_dirs = [self.project_dir_list_widget.item(i).text() for i in range(self.project_dir_list_widget.count())]
        self.output_dir_path = self.output_dir_entry.text()
        self.base_filename_str = self.base_filename_entry.text()
        self.excluded_subdirs_list = [s.strip() for s in self.excluded_subdirs_entry.text().split(",") if s.strip()]
        self.excluded_files_list = [f.strip() for f in self.excluded_files_entry.text().split(",") if f.strip()]
        self.verbose_state = self.verbose_checkbox.isChecked()

    @Slot()
    def run_documentation_process(self):
        self._get_current_config_from_ui()

        if not self.project_dirs:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("msg_select_project_dir_text"))
            return
        if not self.output_dir_path:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("msg_select_output_dir_text"))
            return
        if not self.base_filename_str:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("msg_enter_base_filename_text"))
            return

        output_tab_widget = self.tab_widget.findChild(QWidget, "outputTab")
        if output_tab_widget:
            self.tab_widget.setCurrentWidget(output_tab_widget)

        self.output_text_edit.clear()
        self.status_label.setText(Translations.get("status_processing"))
        self.progress_bar.setRange(0,0) # Indeterminate progress
        self._update_control_states(is_running=True)
        self.last_main_output_file = None

        self.worker_thread = QThread()
        self.doc_worker = DocWorker(
            self.project_dirs, self.excluded_subdirs_list, self.excluded_files_list,
            self.base_filename_str, self.output_dir_path, self.verbose_state, self.output_format_str
        )
        self.doc_worker.moveToThread(self.worker_thread)

        self.worker_thread.started.connect(self.doc_worker.run)
        self.doc_worker.finished.connect(self._on_documentation_finished)
        self.doc_worker.progress_update.connect(self.update_status_label_slot)
        self.doc_worker.error_occurred.connect(self._on_documentation_error)

        # Quan ly thread
        self.doc_worker.finished.connect(self.worker_thread.quit)
        self.doc_worker.finished.connect(self.doc_worker.deleteLater)
        self.worker_thread.finished.connect(self.worker_thread.deleteLater)

        self.worker_thread.start()


    @Slot(str)
    def update_status_label_slot(self, message):
        self.status_label.setText(message)

    @Slot(tuple)
    def _on_documentation_finished(self, result):
        (message, execution_time, num_files, num_folders,
         errors, skipped_files, skipped_folders, output_paths_str) = result

        formatted_output = format_output_for_tkinter(
            message, execution_time, num_files, num_folders,
            errors, skipped_files, skipped_folders, self.output_format_str
        )
        self.output_text_edit.appendPlainText(formatted_output)
        self.status_label.setText(Translations.get("status_docs_generated_at", path=output_paths_str))
        self.progress_bar.setRange(0,100) # Determinate progress
        self.progress_bar.setValue(100)

        all_output_files = [p.strip() for p in output_paths_str.split(",") if p.strip()]
        if all_output_files:
            self.last_main_output_file = all_output_files[0]
        else:
            self.last_main_output_file = None

        # Luu lich su
        is_successful_run = not errors or all("khong ton tai" in str(v).lower() or "not found" in str(v).lower() for v in errors.values())
        if is_successful_run and self.project_dirs:
            first_proj_dir_name = os.path.basename(self.project_dirs[0])
            history_item_name = f"{first_proj_dir_name} ({datetime.now().strftime('%d/%m %H:%M')})"
            if len(self.project_dirs) > 1:
                history_item_name = f"{first_proj_dir_name},... ({datetime.now().strftime('%d/%m %H:%M')})"

            current_config_data = {
                "name": history_item_name,
                "project_dirs": list(self.project_dirs),
                "output_dir": self.output_dir_path,
                "base_filename": self.base_filename_str,
                "excluded_subdirs": self.excluded_subdirs_list,
                "excluded_files": self.excluded_files_list,
                "output_format": self.output_format_str,
                "verbose": self.verbose_state,
                "timestamp": datetime.now().isoformat()
            }
            self.add_to_history(current_config_data)

        self._update_control_states(is_running=False)

        if self._is_exiting_initiated_by_user:
            self._is_exiting_initiated_by_user = False
            self.close()


    @Slot(str)
    def _on_documentation_error(self, error_message):
        self.output_text_edit.appendPlainText(Translations.get("critical_error_occurred", error_message=error_message))
        self.status_label.setText(Translations.get("status_error"))
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(0) # Error state
        self.last_main_output_file = None
        self._update_control_states(is_running=False)

        # Khong can quan ly thread o day, vi finished se duoc emit va tu dong clean

        if self._is_exiting_initiated_by_user:
            self._is_exiting_initiated_by_user = False
            self.close()


    def populate_history_listbox(self):
        self.history_list_widget.clear()
        for item in self.history_data:
            no_tm_str = Translations.get("history_no_tm")
            first_proj_dir = os.path.basename(item["project_dirs"][0]) if item.get("project_dirs") else no_tm_str
            if len(item.get("project_dirs", [])) > 1:
                first_proj_dir += " (+...)"

            try:
                dt_obj = datetime.fromisoformat(item["timestamp"])
                timestamp_str = dt_obj.strftime("%d/%m/%y %H:%M")
            except:
                timestamp_str = Translations.get("history_timestamp_na")

            display_name = item.get("name", first_proj_dir)
            if not display_name or display_name == no_tm_str: display_name = first_proj_dir

            display_text = f"{display_name} [{timestamp_str}]"
            list_item = QListWidgetItem(display_text)
            list_item.setData(Qt.ItemDataRole.UserRole, item)
            self.history_list_widget.addItem(list_item)

    def load_history_from_file(self):
        try:
            if os.path.exists(self.history_file_path):
                with open(self.history_file_path, "r", encoding="utf-8") as f:
                    self.history_data = json.load(f)
                self.history_data.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
            else:
                self.history_data = []
        except json.JSONDecodeError:
            self.history_data = []
            QMessageBox.warning(self, Translations.get("history_file_corrupted_title"), Translations.get("history_file_corrupted_text"))
        except Exception as e:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("history_load_error_text", error=e))
            self.history_data = []
        self.populate_history_listbox()
        self._update_control_states()


    def save_history_to_file(self):
        try:
            with open(self.history_file_path, "w", encoding="utf-8") as f:
                json.dump(self.history_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("history_save_error_text", error=e))

    def add_to_history(self, current_config_data):
        new_config_key_parts = sorted(current_config_data["project_dirs"]) + \
                               [current_config_data["output_dir"], current_config_data["base_filename"]]
        new_config_key = "|".join(new_config_key_parts)

        filtered_history = []
        for item in self.history_data:
            item_key_parts = sorted(item["project_dirs"]) + \
                             [item["output_dir"], item["base_filename"]]
            item_key = "|".join(item_key_parts)
            if item_key != new_config_key:
                filtered_history.append(item)
        self.history_data = filtered_history
        self.history_data.insert(0, current_config_data)
        if len(self.history_data) > MAX_HISTORY_ITEMS:
            self.history_data = self.history_data[:MAX_HISTORY_ITEMS]
        self.save_history_to_file()
        self.populate_history_listbox()

    @Slot()
    def load_selected_history_item(self):
        selected_items = self.history_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("msg_select_history_item_text"))
            return

        config_data = selected_items[0].data(Qt.ItemDataRole.UserRole)
        if not config_data:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("history_item_load_error_text"))
            return

        self.project_dirs = list(config_data.get("project_dirs", []))
        self.project_dir_list_widget.clear()
        for p_dir in self.project_dirs:
            self.project_dir_list_widget.addItem(QListWidgetItem(p_dir))

        self.output_dir_path = config_data.get("output_dir", DEFAULT_OUTPUT_DIR)
        self.output_dir_entry.setText(self.output_dir_path)

        self.base_filename_str = config_data.get("base_filename", DEFAULT_BASE_FILENAME)
        self.base_filename_entry.setText(self.base_filename_str)

        self.output_format_str = config_data.get("output_format", "txt")
        if self.output_format_str == "markdown": self.md_radio.setChecked(True)
        else: self.txt_radio.setChecked(True)

        self.verbose_state = config_data.get("verbose", False)
        self.verbose_checkbox.setChecked(self.verbose_state)

        self.excluded_subdirs_list = list(config_data.get("excluded_subdirs", DEFAULT_EXCLUDED_SUBDIRS))
        self.excluded_subdirs_entry.setText(", ".join(self.excluded_subdirs_list))

        self.excluded_files_list = list(config_data.get("excluded_files", DEFAULT_EXCLUDED_FILES))
        self.excluded_files_entry.setText(", ".join(self.excluded_files_list))

        config_tab_widget = self.tab_widget.findChild(QWidget, "configTab")
        if config_tab_widget:
            self.tab_widget.setCurrentWidget(config_tab_widget)
        self._update_control_states()


    @Slot()
    def delete_selected_history_item(self):
        selected_items = self.history_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("msg_select_history_item_text"))
            return

        confirm = QMessageBox.question(self, Translations.get("dialog_confirm_delete_title"), Translations.get("confirm_delete_history_item_text"),
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                # Lay cac data tu UserRole thay vi index cua list widget
                # vi history_data co the sap xep khac
                items_to_delete_data = [item.data(Qt.ItemDataRole.UserRole) for item in selected_items]
                
                # Tao set cac timestamp de xoa cho nhanh
                timestamps_to_delete = {data['timestamp'] for data in items_to_delete_data if data and 'timestamp' in data}

                new_history_data = [item for item in self.history_data if item.get('timestamp') not in timestamps_to_delete]
                
                if len(new_history_data) < len(self.history_data):
                    self.history_data = new_history_data
                    self.save_history_to_file()
                    self.populate_history_listbox() # Load lai listbox
                    QMessageBox.information(self, Translations.get("dialog_deleted_title"), Translations.get("history_item_deleted_text"))
                else:
                    # Truong hop ko tim thay item de xoa (hiem khi)
                    QMessageBox.warning(self, Translations.get("dialog_error_title"), Translations.get("history_delete_error_text", error="Item not found in data source."))
            except Exception as e:
                 QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("history_delete_error_text", error=str(e)))
        self._update_control_states()


    @Slot()
    def delete_all_history(self):
        if not self.history_data:
            QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("history_empty_text"))
            return
        confirm = QMessageBox.question(self, Translations.get("confirm_delete_all_history_title"),
                                       Translations.get("confirm_delete_all_history_text"),
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.history_data = []
            self.save_history_to_file()
            self.populate_history_listbox()
            QMessageBox.information(self, Translations.get("dialog_deleted_title"), Translations.get("all_history_deleted_text"))
        self._update_control_states()

    @Slot()
    def copy_output_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text_edit.toPlainText())
        QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("output_copied_text"))

    @Slot()
    def clear_output_display(self):
        self.output_text_edit.clear()
        self.last_main_output_file = None
        self._update_control_states()


    @Slot()
    def open_output_folder_path(self):
        path_to_open = self.output_dir_entry.text()
        if path_to_open and os.path.isdir(path_to_open):
            try:
                QDesktopServices.openUrl(f"file:///{os.path.normpath(path_to_open)}")
            except Exception as e:
                 QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("cannot_open_folder_text", error=str(e)))
        else:
            QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("invalid_output_folder_path_text"))

    @Slot()
    def open_ai_studio_and_copy(self):
        ai_studio_url = "https://aistudio.google.com/app/prompts/new_chat"
        if self.last_main_output_file and os.path.exists(self.last_main_output_file):
            try:
                QDesktopServices.openUrl(ai_studio_url)
                clipboard = QApplication.clipboard()
                path_for_clipboard = os.path.normpath(self.last_main_output_file)
                clipboard.setText(path_for_clipboard) # Chi copy duong dan
                QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("ai_studio_opened_path_copied_text", path=path_for_clipboard))
            except Exception as e:
                QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("cannot_open_ai_studio_text", error=str(e)))
        else:
            QMessageBox.warning(self, Translations.get("dialog_notice_title"), Translations.get("no_doc_file_to_copy_path_text"))


    def _update_control_states(self, is_running=False):
        # Kiem tra tung widget truoc khi setEnable
        if hasattr(self, 'add_dir_btn'): self.add_dir_btn.setEnabled(not is_running)
        if hasattr(self, 'project_dir_list_widget') and hasattr(self, 'remove_dir_btn'):
            has_items = self.project_dir_list_widget.count() > 0
            has_selection = len(self.project_dir_list_widget.selectedItems()) > 0
            self.remove_dir_btn.setEnabled(not is_running and has_items and has_selection)
        if hasattr(self, 'output_dir_entry'): self.output_dir_entry.setEnabled(not is_running)
        if hasattr(self, 'browse_output_btn'): self.browse_output_btn.setEnabled(not is_running)
        if hasattr(self, 'base_filename_entry'): self.base_filename_entry.setEnabled(not is_running)
        if hasattr(self, 'txt_radio'): self.txt_radio.setEnabled(not is_running)
        if hasattr(self, 'md_radio'): self.md_radio.setEnabled(not is_running)
        if hasattr(self, 'verbose_checkbox'): self.verbose_checkbox.setEnabled(not is_running)
        if hasattr(self, 'run_button') and hasattr(self, 'project_dir_list_widget'):
            self.run_button.setEnabled(not is_running and self.project_dir_list_widget.count() > 0)

        if hasattr(self, 'excluded_subdirs_entry'): self.excluded_subdirs_entry.setEnabled(not is_running)
        if hasattr(self, 'excluded_files_entry'): self.excluded_files_entry.setEnabled(not is_running)

        if hasattr(self, 'history_list_widget'):
            has_history = self.history_list_widget.count() > 0
            has_selection = len(self.history_list_widget.selectedItems()) > 0
            if hasattr(self, 'load_history_btn'): self.load_history_btn.setEnabled(not is_running and has_selection)
            if hasattr(self, 'delete_history_btn'): self.delete_history_btn.setEnabled(not is_running and has_selection)
            if hasattr(self, 'delete_all_history_btn'): self.delete_all_history_btn.setEnabled(not is_running and has_history)

        if hasattr(self, 'output_text_edit'):
            has_output_text = bool(self.output_text_edit.toPlainText())
            if hasattr(self, 'copy_output_btn'): self.copy_output_btn.setEnabled(has_output_text)
            if hasattr(self, 'clear_output_btn'): self.clear_output_btn.setEnabled(has_output_text)

        if hasattr(self, 'ai_studio_btn'):
            self.ai_studio_btn.setEnabled(bool(self.last_main_output_file) and os.path.exists(str(self.last_main_output_file)))
        if hasattr(self, 'open_output_folder_btn') and hasattr(self, 'output_dir_entry'):
            self.open_output_folder_btn.setEnabled(os.path.isdir(self.output_dir_entry.text()))


    def _apply_qss_styles(self):
        font_family = "Segoe UI, Arial, sans-serif"
        if Translations.current_lang == Translations.LANG_JA:
            font_family = "Meiryo, Segoe UI, Arial, sans-serif"

        # Font chung cho ung dung, BaseMainWindow da set roi, chi can dam bao font family dung
        # QApplication.setFont(QFont(font_family, NORMAL_FONT_SIZE))

        qss = f"""
            /* === WIDGET CHUNG === */
            QWidget {{
                color: {TEXT_COLOR};
                font-family: "{font_family}";
                font-size: {NORMAL_FONT_SIZE}pt;
                outline: 0px; /* An vien focus mac dinh */
            }}
            QMainWindow {{
                background: transparent;
            }}
            QWidget#mainContentWidget {{ /* Padding cho toan bo noi dung trong BaseMainWindow */
                 background-color: transparent;
                 padding: 0px; /* BaseMainWindow's content_area_main_layout se co margin */
            }}
             QWidget#contentAreaWithBackground {{ /* Container cua mainContentWidget va background_label */
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: transparent;
            }}

            /* === TAB WIDGET === */
            QTabWidget::pane {{
                border: 1px solid {INPUT_BORDER_COLOR};
                border-bottom-left-radius: 9px;
                border-bottom-right-radius: 9px;
                border-top-right-radius: 9px; /* Bo tron goc tren phai cua pane */
                background-color: {CONTAINER_BG_COLOR};
                padding: 18px; /* Padding cho noi dung tab */
            }}
            QTabBar::tab {{
                background: rgba(30,35,60,0.75);
                border: 1px solid {INPUT_BORDER_COLOR};
                border-bottom: none;
                padding: 10px 20px; /* Tab rong hon, cao hon */
                margin-right: 4px; /* Khoang cach giua cac tab */
                border-top-left-radius: 8px;
                border-top-right-radius: 8px;
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}";
                font-weight: 500;
            }}
            QTabBar::tab:selected {{
                background: {CONTAINER_BG_COLOR}; /* Giong nen pane de lien mach */
                color: {SELECTED_COLOR};
                font-weight: bold;
                /* border-bottom: 1px solid {CONTAINER_BG_COLOR}; khong can vi pane co border */
            }}
            QTabBar::tab:hover:!selected {{ /* Chi hover khi khong duoc chon */
                background: {HOVER_COLOR};
                color: {TEXT_HOVER_COLOR};
            }}
            QTabBar::tab:disabled {{
                background: rgba(30,35,60,0.4);
                color: rgba(155,160,180,0.5);
            }}

            /* === GROUPBOX === */
            QGroupBox {{
                background-color: rgba(25,30,55,0.65);
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 9px;
                margin-top: 15px; /* Day groupbox xuong de title khong de len vien tab */
                padding: 20px 15px 15px 15px; /* top, right, bottom, left */
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 8px; /* Padding cho title */
                margin-left: 10px; /* Day title vao trong */
                color: {ACCENT_COLOR};
                font-size: {NORMAL_FONT_SIZE + 2}pt; /* Title to hon */
                font-weight: bold;
                background-color: {CONTAINER_BG_COLOR}; /* Nen cho title de che vien groupbox */
                border-radius: 5px;
            }}

            /* === TRUONG NHAP LIEU & DANH SACH === */
            QLineEdit, QPlainTextEdit, QListWidget {{
                background-color: {INPUT_BG_COLOR};
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 8px; /* Bo tron hon */
                padding: 10px; /* Padding input */
                color: {TEXT_COLOR};
            }}
            QLineEdit::placeholder, QPlainTextEdit::placeholder {{
                color: {INPUT_PLACEHOLDER_COLOR};
            }}
            QLineEdit:focus, QPlainTextEdit:focus, QListWidget:focus {{
                border: 1.5px solid {INPUT_FOCUS_BORDER_COLOR};
                background-color: rgba(15, 18, 38, 0.9); /* Nen toi hon khi focus */
                /* box-shadow: 0 0 8px {ACCENT_GLOW_COLOR}; Qt QSS ko ho tro box-shadow truc tiep */
            }}
            QPlainTextEdit, QListWidget {{
                /* Su dung thanh cuon tuy chinh */
            }}

            /* === QListWidget Items === */
            QListWidget::item {{
                padding: 8px 6px; /* Padding item */
                border-radius: 5px; /* Bo tron item */
                margin: 2px 0; /* Khoang cach giua cac item */
            }}
            QListWidget::item:selected {{
                background-color: {SELECTED_COLOR};
                color: {WINDOW_BG_COLOR}; /* Mau chu dam bao tuong phan */
            }}
            QListWidget::item:hover:!selected {{ /* Chi hover khi khong duoc chon */
                background-color: {HOVER_COLOR};
                color: {TEXT_HOVER_COLOR};
            }}

            /* === PUSHBUTTON CHUNG === */
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                border: none;
                border-radius: 8px;
                padding: 10px 20px; /* Padding nut */
                min-height: 24px;
                font-weight: 500;
                color: {TEXT_COLOR};
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
                color: {TEXT_HOVER_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {QColor(PRIMARY_COLOR).darker(125).name()};
            }}
            QPushButton:disabled {{
                background-color: rgba(80,85,110,0.5); /* Nhat hon cho disabled */
                color: {SUBTEXT_COLOR};
            }}

            /* === PUSHBUTTON DAC BIET === */
            QPushButton#runButton {{
                background-color: {SUCCESS_COLOR};
                font-size: {HEADER_FONT_SIZE - 1}pt; /* Font to hon */
                font-weight: bold;
                padding: 14px 28px; /* Nut run to hon */
                color: rgb(20,30,25); /* Mau chu dam bao tuong phan tren nen xanh la */
            }}
            QPushButton#runButton:hover {{
                background-color: {QColor(SUCCESS_COLOR).lighter(110).name()};
            }}
            QPushButton#runButton:pressed {{
                background-color: {QColor(SUCCESS_COLOR).darker(110).name()};
            }}

            QPushButton#primaryButton {{ background-color: {PRIMARY_COLOR}; }}
            QPushButton#primaryButton:hover {{ background-color: {HOVER_COLOR}; }}

            QPushButton#secondaryButton {{ background-color: {QColor(PRIMARY_COLOR).lighter(115).name()}; color: {SUBTEXT_COLOR}; }}
            QPushButton#secondaryButton:hover {{ background-color: {PRIMARY_COLOR}; color: {TEXT_COLOR}; }}

            QPushButton#accentButton {{ background-color: {ACCENT_COLOR}; color: {WINDOW_BG_COLOR}; }}
            QPushButton#accentButton:hover {{ background-color: {QColor(ACCENT_COLOR).lighter(110).name()}; }}

            QPushButton#warningButton {{
                background-color: {WARNING_COLOR};
                color: rgb(50,30,0); /* Mau chu dam bao tuong phan tren nen vang */
            }}
            QPushButton#warningButton:hover {{
                background-color: {QColor(WARNING_COLOR).lighter(110).name()};
            }}
            QPushButton#errorButton {{ background-color: {ERROR_COLOR}; color: white; }}
            QPushButton#errorButton:hover {{ background-color: {QColor(ERROR_COLOR).lighter(110).name()}; }}

            /* === RADIOBUTTON & CHECKBOX === */
            QRadioButton, QCheckBox {{ padding: 4px 0; }}
            QRadioButton::indicator, QCheckBox::indicator {{
                width: 18px; height: 18px; /* To hon chut */
                border-radius: 5px; /* Bo tron hon */
                border: 1.5px solid {SUBTEXT_COLOR};
                background-color: transparent; /* Trong suot de thay nen */
            }}
            QRadioButton::indicator {{ border-radius: 9px; /* Tron cho radio */ }}
            QRadioButton::indicator:checked, QCheckBox::indicator:checked {{
                background-color: {SELECTED_COLOR};
                border-color: {ACCENT_COLOR};
                image: none; /* An icon check mac dinh neu co */
            }}
            /* Them icon check tuy chinh (Unicode) */
            QCheckBox::indicator:checked {{
                /* content: "\\2713"; Unicode check mark, can be tricky with QSS */
                /* Better to use a small image or rely on background color change */
            }}
            QRadioButton::indicator:hover:!checked, QCheckBox::indicator:hover:!checked {{
                border-color: {TEXT_HOVER_COLOR};
            }}
            QRadioButton::indicator:disabled, QCheckBox::indicator:disabled {{
                border-color: rgba(155,160,180,0.5);
                background-color: rgba(12,15,32,0.3);
            }}
            QRadioButton:disabled, QCheckBox:disabled {{
                color: {SUBTEXT_COLOR};
            }}

            /* === PROGRESSBAR === */
            QProgressBar {{
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 7px; /* Bo tron hon */
                text-align: center;
                background-color: {INPUT_BG_COLOR};
                height: 15px; /* Thanh progress cao hon */
            }}
            QProgressBar::chunk {{
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {QColor(SUCCESS_COLOR).lighter(120).name()}, stop:1 {SUCCESS_COLOR});
                border-radius: 6px; /* Bo tron chunk */
                margin: 1px; /* Tao khoang cach vien */
            }}

            /* === STATUS BAR === */
            QFrame#statusBar {{
                border-top: 1px solid rgba(200, 205, 220, 0.15); /* Dam hon */
                background-color: transparent; /* Nen trong suot */
            }}
            QLabel#statusLabel {{
                color: {SUBTEXT_COLOR};
                font-size: {SMALL_FONT_SIZE}pt; /* Font status nho hon */
                padding-left: 5px;
            }}
            QLabel#statusLabel:hover {{
                color: {TEXT_HOVER_COLOR};
            }}

            /* === THANH CUON (SCROLLBAR) === */
            QScrollBar:vertical {{
                border: none;
                background: {SCROLLBAR_BG_COLOR};
                width: 14px; /* Thanh cuon rong hon */
                margin: 15px 0 15px 0; /* Khoang cach top/bottom cho mui ten */
                border-radius: 7px;
            }}
            QScrollBar::handle:vertical {{
                background: {SCROLLBAR_HANDLE_COLOR};
                min-height: 30px; /* Chieu cao toi thieu cua handle */
                border-radius: 6px;
                border: 1px solid rgba(20,25,50,0.5); /* Vien nhe cho handle */
            }}
            QScrollBar::handle:vertical:hover {{
                background: {SCROLLBAR_HANDLE_HOVER_COLOR};
            }}
            QScrollBar::handle:vertical:pressed {{
                background: {SCROLLBAR_HANDLE_PRESSED_COLOR};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                border: none;
                background: none; /* An mui ten mac dinh */
                height: 14px;
                subcontrol-position: top;
                subcontrol-origin: margin;
            }}
            QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
                 background: none; /* An mui ten */
            }}
            QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
                background: none; /* An vung trang */
            }}
            /* Tuong tu cho QScrollBar:horizontal */
            QScrollBar:horizontal {{
                border: none;
                background: {SCROLLBAR_BG_COLOR};
                height: 14px;
                margin: 0 15px 0 15px;
                border-radius: 7px;
            }}
            QScrollBar::handle:horizontal {{
                background: {SCROLLBAR_HANDLE_COLOR};
                min-width: 30px;
                border-radius: 6px;
                border: 1px solid rgba(20,25,50,0.5);
            }}
            QScrollBar::handle:horizontal:hover {{
                background: {SCROLLBAR_HANDLE_HOVER_COLOR};
            }}
            QScrollBar::handle:horizontal:pressed {{
                background: {SCROLLBAR_HANDLE_PRESSED_COLOR};
            }}
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
                border: none;
                background: none;
                width: 14px;
                subcontrol-position: left;
                subcontrol-origin: margin;
            }}
            QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {{
                 background: none;
            }}
            QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
                background: none;
            }}

            /* === QMESSAGEBOX === */
            QMessageBox {{
                background-color: {WINDOW_BG_COLOR}; /* Nen cua so thong bao */
                border: 1px solid {ACCENT_COLOR};
                border-radius: 10px;
            }}
            QMessageBox QLabel {{ /* Text trong MessageBox */
                color: {TEXT_COLOR};
                font-size: {NORMAL_FONT_SIZE}pt;
                padding: 15px;
                min-width: 300px; /* Chieu rong toi thieu cua text area */
            }}
            QMessageBox QPushButton {{ /* Nut trong MessageBox */
                background-color: {PRIMARY_COLOR};
                color: {TEXT_COLOR};
                border-radius: 7px;
                padding: 8px 18px; /* Padding nut */
                min-width: 80px; /* Chieu rong toi thieu nut */
                margin: 5px;
            }}
            QMessageBox QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
            QMessageBox QPushButton:pressed {{
                background-color: {QColor(PRIMARY_COLOR).darker(120).name()};
            }}
        """
        self.setStyleSheet(qss)
        if hasattr(self, 'custom_title_bar'):
            self.custom_title_bar._apply_styles() # Dam bao title bar cung cap nhat style
        self.update()


    def closeEvent(self, event):
        if self._animation_is_closing_flag:
            event.accept()
            return

        if self.opacity_animation_close and self.opacity_animation_close.state() == QAbstractAnimation.State.Running:
             event.ignore()
             return

        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(self, Translations.get("confirm_exit_title"),
                                         Translations.get("confirm_exit_text"),
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if hasattr(self, 'run_button'): self.run_button.setEnabled(False)
                if hasattr(self, 'status_label'): self.status_label.setText(Translations.get("status_finishing_before_exit"))
                self._is_exiting_initiated_by_user = True

                event.ignore() # Khong dong ngay, cho worker xong
                return
            else:
                event.ignore() # Huy dong
                return
        else:
            # Goi closeEvent cua BaseMainWindow de xu ly animation dong
            super().closeEvent(event)