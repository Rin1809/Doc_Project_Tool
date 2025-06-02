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
    TEXT_COLOR, SUBTEXT_COLOR, INPUT_BG_COLOR, INPUT_BORDER_COLOR, INPUT_FOCUS_BORDER_COLOR,
    PRIMARY_COLOR, ACCENT_COLOR, HOVER_COLOR, SUCCESS_COLOR, WARNING_COLOR, ERROR_COLOR,
    CONTAINER_BG_COLOR, WINDOW_BG_COLOR
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
        super().__init__(base_app_path) 
        
        self._init_app_variables()
        self._create_ui_layout_and_tabs() # Ten ham dc cap nhat de phan anh ro hon
        self._apply_qss_styles() 
        self._connect_signals()
        self.load_history_from_file()
        
        self.retranslate_app_specific_ui() 
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


    def _create_ui_layout_and_tabs(self): # Truoc day la _create_ui
        # main_content_widget da ton tai tu BaseMainWindow, ta se them layout va noi dung vao do
        content_layout = QVBoxLayout(self.main_content_widget) # Layout nay cho main_content_widget
        content_layout.setContentsMargins(15, 15, 15, 15) 
        content_layout.setSpacing(10)

        # Tao QTabWidget
        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabWidget")

        # Tao noi dung cho tung tab (cac QWidget con)
        # Cac ham nay se tao self.tab_config, self.tab_advanced, v.v.
        self._create_config_tab_content()    
        self._create_advanced_tab_content()
        self._create_history_tab_content()
        self._create_output_tab_content()

        # QUAN TRONG: Them cac QWidget con vao QTabWidget duoi dang tab
        # Tieu de ban dau la placeholder, se duoc dich sau trong retranslate_app_specific_ui
        self.tab_widget.addTab(self.tab_config, "...") # Them tab config
        self.tab_widget.addTab(self.tab_advanced, "...")# Them tab advanced
        self.tab_widget.addTab(self.tab_history, "...") # Them tab history
        self.tab_widget.addTab(self.tab_output, "...")  # Them tab output
        
        # Them QTabWidget (da chua cac tab con) vao layout chinh cua main_content_widget
        content_layout.addWidget(self.tab_widget)

        # Tao status bar va them vao content_layout (se nam ben duoi QTabWidget)
        self._create_status_bar(content_layout) 

    # Doi ten cac ham tao tab content cho ro nghia hon
    def _create_config_tab_content(self): # Truoc la _create_config_tab
        self.tab_config = QWidget() # Day la widget se chua noi dung cua tab Config
        self.tab_config.setObjectName("configTab")
        layout = QVBoxLayout(self.tab_config) # Layout cho widget tab_config
        layout.setSpacing(15)

        self.dir_group = QGroupBox() 
        self.dir_group.setObjectName("configGroup")
        dir_layout = QVBoxLayout(self.dir_group)
        
        self.project_dir_list_widget = QListWidget()
        self.project_dir_list_widget.setObjectName("projectDirList")
        self.project_dir_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        dir_layout.addWidget(self.project_dir_list_widget)

        dir_buttons_layout = QHBoxLayout()
        self.add_dir_btn = QPushButton() 
        self.add_dir_btn.setObjectName("primaryButton")
        self.remove_dir_btn = QPushButton() 
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
        
        self.output_dir_label_widget = QLabel() 
        self.output_dir_entry = QLineEdit(self.output_dir_path)
        self.browse_output_btn = QPushButton() 
        self.browse_output_btn.setObjectName("secondaryButton")
        output_dir_hbox = QHBoxLayout()
        output_dir_hbox.addWidget(self.output_dir_entry)
        output_dir_hbox.addWidget(self.browse_output_btn)
        output_layout.addRow(self.output_dir_label_widget, output_dir_hbox)

        self.base_filename_label_widget = QLabel() 
        self.base_filename_entry = QLineEdit(self.base_filename_str)
        output_layout.addRow(self.base_filename_label_widget, self.base_filename_entry)
        
        self.output_format_label_widget = QLabel() 
        format_hbox = QHBoxLayout()
        self.txt_radio = QRadioButton() 
        self.txt_radio.setChecked(True)
        self.md_radio = QRadioButton() 
        self.verbose_checkbox = QCheckBox() 
        format_hbox.addWidget(self.txt_radio)
        format_hbox.addWidget(self.md_radio)
        format_hbox.addSpacerItem(QSpacerItem(20,0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        format_hbox.addWidget(self.verbose_checkbox)
        format_hbox.addStretch()
        output_layout.addRow(self.output_format_label_widget, format_hbox)
        layout.addWidget(self.output_group)

        self.run_button = QPushButton() 
        self.run_button.setObjectName("runButton")
        self.run_button.setFixedHeight(40) 
        layout.addWidget(self.run_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()

    def _create_advanced_tab_content(self): # Truoc la _create_advanced_tab
        self.tab_advanced = QWidget() 
        self.tab_advanced.setObjectName("advancedTab")
        layout = QVBoxLayout(self.tab_advanced)
        layout.setSpacing(15)

        self.excluded_dirs_group = QGroupBox() 
        self.excluded_dirs_group.setObjectName("configGroup")
        excluded_dirs_layout = QVBoxLayout(self.excluded_dirs_group)
        self.excluded_subdirs_entry = QLineEdit(", ".join(self.excluded_subdirs_list))
        excluded_dirs_layout.addWidget(self.excluded_subdirs_entry)
        layout.addWidget(self.excluded_dirs_group)

        self.excluded_files_group = QGroupBox() 
        self.excluded_files_group.setObjectName("configGroup")
        excluded_files_layout = QVBoxLayout(self.excluded_files_group)
        self.excluded_files_entry = QLineEdit(", ".join(self.excluded_files_list))
        excluded_files_layout.addWidget(self.excluded_files_entry)
        layout.addWidget(self.excluded_files_group)
        
        layout.addStretch()

    def _create_history_tab_content(self): # Truoc la _create_history_tab
        self.tab_history = QWidget() 
        self.tab_history.setObjectName("historyTab")
        layout = QVBoxLayout(self.tab_history)
        layout.setSpacing(10)
        
        self.history_group = QGroupBox() 
        self.history_group.setObjectName("configGroup")
        history_layout = QVBoxLayout(self.history_group)

        self.history_list_widget = QListWidget()
        self.history_list_widget.setObjectName("historyList")
        history_layout.addWidget(self.history_list_widget)

        history_buttons_layout = QHBoxLayout()
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

    def _create_output_tab_content(self): # Truoc la _create_output_tab
        self.tab_output = QWidget() 
        self.tab_output.setObjectName("outputTab")
        layout = QVBoxLayout(self.tab_output)
        layout.setSpacing(10)

        self.output_text_edit = QPlainTextEdit() 
        self.output_text_edit.setObjectName("outputTextEdit")
        self.output_text_edit.setReadOnly(True)
        layout.addWidget(self.output_text_edit)

        output_buttons_layout = QHBoxLayout()
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

    def _create_status_bar(self, parent_layout): # parent_layout la content_layout cua main_content_widget
        status_bar_widget = QFrame() 
        status_bar_widget.setObjectName("statusBar")
        status_bar_widget.setFixedHeight(30)
        status_layout = QHBoxLayout(status_bar_widget)
        status_layout.setContentsMargins(10, 0, 10, 0)

        self.status_label = QLabel(Translations.get("status_ready")) 
        self.status_label.setObjectName("statusLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0,100) 

        status_layout.addWidget(self.status_label)
        status_layout.addSpacerItem(QSpacerItem(20,0,QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        status_layout.addWidget(self.progress_bar, 1) 
        parent_layout.addWidget(status_bar_widget) # Them status bar vao layout cua main_content_widget, ben duoi TabWidget

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
        self.setWindowTitle(Translations.get("app_window_title_default"))
        self.custom_title_bar.setTitle("app_title_on_bar") 
        self.custom_title_bar.setVersion("app_version_pyside6") 

        # Cap nhat tieu de cac tab
        if hasattr(self, 'tab_widget') and hasattr(self, 'tab_config'):
            idx = self.tab_widget.indexOf(self.tab_config)
            if idx != -1: self.tab_widget.setTabText(idx, Translations.get("config_tab_title"))
        
        if hasattr(self, 'tab_widget') and hasattr(self, 'tab_advanced'):
            idx = self.tab_widget.indexOf(self.tab_advanced)
            if idx != -1: self.tab_widget.setTabText(idx, Translations.get("advanced_tab_title"))

        if hasattr(self, 'tab_widget') and hasattr(self, 'tab_history'):
            idx = self.tab_widget.indexOf(self.tab_history)
            if idx != -1: self.tab_widget.setTabText(idx, Translations.get("history_tab_title"))
        
        if hasattr(self, 'tab_widget') and hasattr(self, 'tab_output'):
            idx = self.tab_widget.indexOf(self.tab_output)
            if idx != -1: self.tab_widget.setTabText(idx, Translations.get("output_tab_title"))
        
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
        if hasattr(self, 'excluded_files_group'): self.excluded_files_group.setTitle(Translations.get("excluded_files_group_title"))
        
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
        if hasattr(self, 'status_label'): # Ktra xem status_label co ton tai ko
            current_status_text = self.status_label.text()
            is_ready_status = False
            for lang_code_check in Translations.lang_map.keys():
                if current_status_text == Translations.get("status_ready", lang=lang_code_check): # Su dung lang= de lay dung text
                    is_ready_status = True
                    break
            if is_ready_status:
                self.status_label.setText(Translations.get("status_ready")) # Set lai bang ngon ngu hien tai
        
        self._apply_qss_styles() 


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
            
        # Chuyen sang tab output truoc khi chay
        output_tab_widget = self.tab_widget.findChild(QWidget, "outputTab")
        if output_tab_widget:
            self.tab_widget.setCurrentWidget(output_tab_widget)

        self.output_text_edit.clear()
        self.status_label.setText(Translations.get("status_processing")) 
        self.progress_bar.setRange(0,0) 
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
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(100)
        
        all_output_files = [p.strip() for p in output_paths_str.split(",") if p.strip()]
        if all_output_files:
            self.last_main_output_file = all_output_files[0]
        else:
            self.last_main_output_file = None 

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
        self.progress_bar.setValue(0) 
        self.last_main_output_file = None
        self._update_control_states(is_running=False) 
        
        if self.worker_thread and self.worker_thread.isRunning():
            pass # Ko can lam gi them, worker se tu thoat
        
        if self._is_exiting_initiated_by_user:
            self._is_exiting_initiated_by_user = False 
            self.close() 


    # --- History Functions ---
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

        # Chuyen sang tab config sau khi load
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
                indices_to_delete = sorted([self.history_list_widget.row(item) for item in selected_items], reverse=True)
                
                # Xoa tu self.history_data dua tren index da sap xep nguoc
                # de ko bi loi index out of bounds
                for list_widget_index in indices_to_delete:
                    # Can map list_widget_index (co the bi filter/sort) voi index trong self.history_data
                    # Vi history_data duoc sort theo timestamp, va listbox cung vay, index nen tuong ung
                    if 0 <= list_widget_index < len(self.history_data):
                         del self.history_data[list_widget_index]
                
                self.save_history_to_file()
                self.populate_history_listbox() # Load lai listbox
                QMessageBox.information(self, Translations.get("dialog_deleted_title"), Translations.get("history_item_deleted_text")) 
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

    # --- Output Tab Functions ---
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
                # Su dung QDesktopServices de mo thu muc, ho tro da nen tang tot hon
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
                # path_for_clipboard = self.last_main_output_file.replace("\\", "/") # Old, gay / tren Win
                path_for_clipboard = os.path.normpath(self.last_main_output_file) # Dg dan chuan OS
                clipboard.setText(path_for_clipboard)
                QMessageBox.information(self, Translations.get("dialog_notice_title"), Translations.get("ai_studio_opened_path_copied_text", path=path_for_clipboard)) 
            except Exception as e:
                QMessageBox.critical(self, Translations.get("dialog_error_title"), Translations.get("cannot_open_ai_studio_text", error=str(e))) 
        else:
            QMessageBox.warning(self, Translations.get("dialog_notice_title"), Translations.get("no_doc_file_to_copy_path_text")) 


    def _update_control_states(self, is_running=False):
        # Kiem tra xem cac widget da duoc khoi tao chua truoc khi truy cap
        if hasattr(self, 'add_dir_btn'): self.add_dir_btn.setEnabled(not is_running)
        if hasattr(self, 'project_dir_list_widget') and hasattr(self, 'remove_dir_btn'):
            self.remove_dir_btn.setEnabled(not is_running and self.project_dir_list_widget.count() > 0)
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

        app_font = QFont(font_family, NORMAL_FONT_SIZE)
        QApplication.setFont(app_font)
        
        qss = f"""
            QWidget {{
                color: {TEXT_COLOR};
                font-family: "{font_family}"; 
                font-size: {NORMAL_FONT_SIZE}pt;
            }}
            QMainWindow {{
                background: transparent; 
            }}
            QWidget#mainContainerWidget {{ 
                /* border: 2px solid yellow; */ /* Debug */
            }}
            QWidget#mainContentWidget {{
                 background-color: transparent; 
                 padding: 10px; /* Giu padding de noi dung ko sat mep */
                 /* border: 1px solid lime; */ /* Debug */
            }}
             QWidget#contentAreaWithBackground {{
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: transparent; 
                /* border: 1px solid cyan; */ /* Debug */
            }}
            QTabWidget::pane {{
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 8px;
                background-color: {CONTAINER_BG_COLOR};
                padding: 10px;
            }}
            QTabBar::tab {{
                background: rgba(255,255,255,0.1);
                border: 1px solid {INPUT_BORDER_COLOR};
                border-bottom: none; 
                padding: 8px 15px;
                margin-right: 2px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                color: {SUBTEXT_COLOR};
                font-family: "{font_family}"; 
            }}
            QTabBar::tab:selected {{
                background: {CONTAINER_BG_COLOR}; 
                color: {TEXT_COLOR};
                font-weight: bold;
            }}
            QTabBar::tab:hover {{
                background: rgba(255,255,255,0.15);
            }}
            QGroupBox {{
                background-color: rgba(255,255,255,0.03); 
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 8px;
                margin-top: 10px; 
                padding: 15px 10px 10px 10px; 
                font-family: "{font_family}"; 
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px 0 5px;
                left: 10px;
                color: {SUBTEXT_COLOR};
                font-size: {NORMAL_FONT_SIZE + 1}pt;
                font-weight: bold;
                font-family: "{font_family}"; 
            }}
            QLineEdit, QPlainTextEdit, QListWidget {{
                background-color: {INPUT_BG_COLOR};
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 6px;
                padding: 8px;
                font-family: "{font_family}"; 
            }}
            QLineEdit:focus, QPlainTextEdit:focus, QListWidget:focus {{
                border: 1px solid {INPUT_FOCUS_BORDER_COLOR};
            }}
            QListWidget::item:selected {{
                background-color: {ACCENT_COLOR};
                color: white;
            }}
            QPushButton {{
                background-color: {PRIMARY_COLOR};
                border: none;
                border-radius: 6px;
                padding: 8px 15px;
                min-height: 20px; 
                font-family: "{font_family}"; 
            }}
            QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
            QPushButton:pressed {{
                background-color: {PRIMARY_COLOR}; 
            }}
            QPushButton:disabled {{
                background-color: rgba(80,80,80,0.5);
                color: {SUBTEXT_COLOR};
            }}
            QPushButton#runButton {{
                background-color: {SUCCESS_COLOR};
                font-size: {HEADER_FONT_SIZE - 2}pt;
                font-weight: bold;
                padding: 10px 20px;
            }}
            QPushButton#runButton:hover {{
                background-color: {QColor(SUCCESS_COLOR).lighter(120).name()};
            }}
            QPushButton#primaryButton {{ background-color: {PRIMARY_COLOR}; }}
            QPushButton#primaryButton:hover {{ background-color: {HOVER_COLOR}; }}
            QPushButton#secondaryButton {{ background-color: {QColor(PRIMARY_COLOR).darker(120).name()}; }}
            QPushButton#secondaryButton:hover {{ background-color: {PRIMARY_COLOR}; }}
            QPushButton#accentButton {{ background-color: {ACCENT_COLOR}; }}
            QPushButton#accentButton:hover {{ background-color: {QColor(ACCENT_COLOR).lighter(120).name()}; }}

            QPushButton#warningButton {{ 
                background-color: {WARNING_COLOR}; 
                color: white; 
            }}
            QPushButton#warningButton:hover {{ 
                background-color: {QColor(WARNING_COLOR).lighter(120).name()}; 
                color: white; 
            }}
            QPushButton#errorButton {{ background-color: {ERROR_COLOR}; color: white; }}
            QPushButton#errorButton:hover {{ background-color: {QColor(ERROR_COLOR).lighter(120).name()}; color: white; }}

            QRadioButton, QCheckBox {{ font-family: "{font_family}"; }}
            QRadioButton::indicator, QCheckBox::indicator {{
                width: 16px; height: 16px; border-radius: 3px;
            }}
            QRadioButton::indicator {{ border-radius: 8px; }}
            QRadioButton::indicator:checked, QCheckBox::indicator:checked {{
                background-color: {ACCENT_COLOR};
            }}
            QProgressBar {{
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 4px;
                text-align: center;
                background-color: {INPUT_BG_COLOR};
            }}
            QProgressBar::chunk {{
                background-color: {SUCCESS_COLOR};
                border-radius: 3px;
                margin: 0.5px;
            }}
            QFrame#statusBar {{
                border-top: 1px solid {INPUT_BORDER_COLOR};
                background-color: transparent; /* Giong voi mainContentWidget */
                 /* border: 1px solid orange; */ /* Debug */
            }}
            QLabel#statusLabel {{
                color: {SUBTEXT_COLOR};
                font-size: {SMALL_FONT_SIZE}pt;
                font-family: "{font_family}"; 
            }}
            QMessageBox {{ 
                background-color: {WINDOW_BG_COLOR}; 
                font-family: "{font_family}";
            }}
            QMessageBox QLabel {{ 
                color: {TEXT_COLOR};
                font-family: "{font_family}";
            }}
            QMessageBox QPushButton {{ 
                background-color: {PRIMARY_COLOR};
                color: {TEXT_COLOR};
                border-radius: 4px;
                padding: 6px 12px;
                min-width: 70px;
                font-family: "{font_family}";
            }}
            QMessageBox QPushButton:hover {{
                background-color: {HOVER_COLOR};
            }}
        """
        self.setStyleSheet(qss)
        if hasattr(self, 'custom_title_bar'): # Ktra truoc khi truy cap
            self.custom_title_bar._apply_styles() 
        self.update()


    def closeEvent(self, event):
        if self._animation_is_closing_flag: # Neu dang trong animation dong cua thi accept
            event.accept() 
            return
        
        # Neu animation dong cua dang chay thi bo qua event nay
        if self.opacity_animation_close and self.opacity_animation_close.state() == QAbstractAnimation.State.Running: 
             event.ignore() 
             return

        # Neu worker dang chay, hoi nguoi dung
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(self, Translations.get("confirm_exit_title"), 
                                         Translations.get("confirm_exit_text"), 
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                if hasattr(self, 'run_button'): self.run_button.setEnabled(False) 
                if hasattr(self, 'status_label'): self.status_label.setText(Translations.get("status_finishing_before_exit")) 
                self._is_exiting_initiated_by_user = True 
                
                event.ignore() 
                return 
            else:
                event.ignore() 
                return
        else: 
            super().closeEvent(event) 