import os
import sys
import json
from datetime import datetime
import subprocess
import webbrowser
from threading import Thread # Giu lai Thread cho tac vu nen

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QFileDialog, QMessageBox, QLineEdit, QListWidget, QListWidgetItem,
    QRadioButton, QCheckBox, QTabWidget, QProgressBar, QPlainTextEdit,
    QScrollArea, QFrame, QGroupBox, QSpacerItem, QSizePolicy, QFormLayout
)
from PySide6.QtCore import Qt, Signal, Slot, QThread as QCoreThread, QObject, QEventLoop
from PySide6.QtGui import QFont, QDesktopServices, QClipboard, QPalette, QColor, QIcon

from .base_main_window import BaseMainWindow # Lop co so moi
from .app_logic import tao_tai_lieu_du_an
from .gui_utils import format_output_for_tkinter
from .constants import (
    DEFAULT_EXCLUDED_SUBDIRS, DEFAULT_EXCLUDED_FILES,
    DEFAULT_OUTPUT_DIR, DEFAULT_BASE_FILENAME,
    HISTORY_FILE, MAX_HISTORY_ITEMS,
    NORMAL_FONT_SIZE, HEADER_FONT_SIZE, SMALL_FONT_SIZE,
    TEXT_COLOR, SUBTEXT_COLOR, INPUT_BG_COLOR, INPUT_BORDER_COLOR, INPUT_FOCUS_BORDER_COLOR,
    PRIMARY_COLOR, ACCENT_COLOR, HOVER_COLOR, SUCCESS_COLOR, WARNING_COLOR, ERROR_COLOR,
    CONTAINER_BG_COLOR, WINDOW_BG_COLOR
)

# Worker cho tac vu tao tai lieu
class DocWorker(QObject):
    finished = Signal(tuple) # (message, exec_time, num_files, num_folders, errors, skipped_files, skipped_folders, output_paths_str)
    progress_update = Signal(str) # Cap nhat trang thai
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
            self.progress_update.emit("Bắt đầu tạo tài liệu...")
            result = tao_tai_lieu_du_an(
                self.project_dirs, self.excluded_subdirs, self.excluded_files,
                self.base_filename, self.output_dir, self.verbose, self.output_format
            )
            self.finished.emit(result)
        except Exception as e:
            self.error_occurred.emit(f"Lỗi trong worker: {str(e)}")


class ProjectDocApp(BaseMainWindow): # Ke thua tu BaseMainWindow
    def __init__(self, base_app_path):
        super().__init__(base_app_path) # Goi init cua BaseMainWindow
        self.setWindowTitle("Tạo Tài Liệu Dự Án - PySide6")
        self.custom_title_bar.setTitle("Tạo Tài Liệu Dự Án")
        self.custom_title_bar.setVersion("v3.0.0-PySide6")

        # Khoi tao cac bien trang thai va cau hinh
        self._init_app_variables()
        self._create_ui() # Tao UI trong main_content_widget cua BaseMainWindow
        self._apply_qss_styles() # Ap dung QSS
        self._connect_signals()
        self.load_history_from_file()
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
        self._is_exiting_initiated_by_user = False # Flag cho closeEvent


    def _create_ui(self):
        # main_content_widget da duoc tao trong BaseMainWindow
        # Tao layout cho main_content_widget
        content_layout = QVBoxLayout(self.main_content_widget)
        content_layout.setContentsMargins(15, 15, 15, 15) # Padding cho content
        content_layout.setSpacing(10)

        self.tab_widget = QTabWidget()
        self.tab_widget.setObjectName("mainTabWidget")
        content_layout.addWidget(self.tab_widget)

        self._create_config_tab()
        self._create_advanced_tab()
        self._create_history_tab()
        self._create_output_tab()

        self._create_status_bar(content_layout) # Them status bar vao layout chinh

    def _create_config_tab(self):
        tab_config = QWidget()
        tab_config.setObjectName("configTab")
        layout = QVBoxLayout(tab_config)
        layout.setSpacing(15)

        # Muc Thu muc du an
        dir_group = QGroupBox("Thư mục dự án")
        dir_group.setObjectName("configGroup")
        dir_layout = QVBoxLayout(dir_group)
        
        self.project_dir_list_widget = QListWidget()
        self.project_dir_list_widget.setObjectName("projectDirList")
        self.project_dir_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        dir_layout.addWidget(self.project_dir_list_widget)

        dir_buttons_layout = QHBoxLayout()
        self.add_dir_btn = QPushButton("Thêm thư mục")
        self.add_dir_btn.setObjectName("primaryButton")
        self.remove_dir_btn = QPushButton("Xóa thư mục đã chọn")
        dir_buttons_layout.addWidget(self.add_dir_btn)
        dir_buttons_layout.addWidget(self.remove_dir_btn)
        dir_buttons_layout.addStretch()
        dir_layout.addLayout(dir_buttons_layout)
        layout.addWidget(dir_group)

        # Muc Thu muc dau ra
        output_group = QGroupBox("Thiết lập đầu ra")
        output_group.setObjectName("configGroup")
        output_layout = QFormLayout(output_group)
        output_layout.setRowWrapPolicy(QFormLayout.RowWrapPolicy.WrapAllRows)
        output_layout.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        
        self.output_dir_entry = QLineEdit(self.output_dir_path)
        self.browse_output_btn = QPushButton("Duyệt...")
        self.browse_output_btn.setObjectName("secondaryButton")
        output_dir_hbox = QHBoxLayout()
        output_dir_hbox.addWidget(self.output_dir_entry)
        output_dir_hbox.addWidget(self.browse_output_btn)
        output_layout.addRow("Thư mục đầu ra:", output_dir_hbox)

        self.base_filename_entry = QLineEdit(self.base_filename_str)
        output_layout.addRow("Tên tệp cơ sở:", self.base_filename_entry)
        
        # Dinh dang dau ra
        format_hbox = QHBoxLayout()
        self.txt_radio = QRadioButton("Văn bản (.txt)")
        self.txt_radio.setChecked(True)
        self.md_radio = QRadioButton("Markdown (.md)")
        self.verbose_checkbox = QCheckBox("Chi tiết (verbose)")
        format_hbox.addWidget(self.txt_radio)
        format_hbox.addWidget(self.md_radio)
        format_hbox.addSpacerItem(QSpacerItem(20,0, QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        format_hbox.addWidget(self.verbose_checkbox)
        format_hbox.addStretch()
        output_layout.addRow("Định dạng:", format_hbox)
        layout.addWidget(output_group)

        # Nut Chay
        self.run_button = QPushButton("🚀 Tạo Tài Liệu")
        self.run_button.setObjectName("runButton")
        self.run_button.setFixedHeight(40) # Lam nut to hon
        layout.addWidget(self.run_button, 0, Qt.AlignmentFlag.AlignCenter)
        layout.addStretch()
        self.tab_widget.addTab(tab_config, "Cấu hình")

    def _create_advanced_tab(self):
        tab_advanced = QWidget()
        tab_advanced.setObjectName("advancedTab")
        layout = QVBoxLayout(tab_advanced)
        layout.setSpacing(15)

        excluded_dirs_group = QGroupBox("Thư mục con loại trừ (cách nhau bởi dấu phẩy)")
        excluded_dirs_group.setObjectName("configGroup")
        excluded_dirs_layout = QVBoxLayout(excluded_dirs_group)
        self.excluded_subdirs_entry = QLineEdit(", ".join(self.excluded_subdirs_list))
        excluded_dirs_layout.addWidget(self.excluded_subdirs_entry)
        layout.addWidget(excluded_dirs_group)

        excluded_files_group = QGroupBox("Tệp loại trừ (đuôi tệp hoặc tên tệp, cách nhau bởi dấu phẩy)")
        excluded_files_group.setObjectName("configGroup")
        excluded_files_layout = QVBoxLayout(excluded_files_group)
        self.excluded_files_entry = QLineEdit(", ".join(self.excluded_files_list))
        excluded_files_layout.addWidget(self.excluded_files_entry)
        layout.addWidget(excluded_files_group)
        
        layout.addStretch()
        self.tab_widget.addTab(tab_advanced, "Nâng cao")

    def _create_history_tab(self):
        tab_history = QWidget()
        tab_history.setObjectName("historyTab")
        layout = QVBoxLayout(tab_history)
        layout.setSpacing(10)
        
        history_group = QGroupBox("Lịch sử cấu hình đã chạy")
        history_group.setObjectName("configGroup")
        history_layout = QVBoxLayout(history_group)

        self.history_list_widget = QListWidget()
        self.history_list_widget.setObjectName("historyList")
        history_layout.addWidget(self.history_list_widget)

        history_buttons_layout = QHBoxLayout()
        self.load_history_btn = QPushButton("Tải Cấu Hình")
        self.load_history_btn.setObjectName("primaryButton")
        self.delete_history_btn = QPushButton("Xóa Mục")
        self.delete_history_btn.setObjectName("warningButton")
        self.delete_all_history_btn = QPushButton("Xóa Tất Cả")
        self.delete_all_history_btn.setObjectName("errorButton")

        history_buttons_layout.addWidget(self.load_history_btn)
        history_buttons_layout.addWidget(self.delete_history_btn)
        history_buttons_layout.addStretch()
        history_buttons_layout.addWidget(self.delete_all_history_btn)
        history_layout.addLayout(history_buttons_layout)
        layout.addWidget(history_group)
        self.tab_widget.addTab(tab_history, "Lịch sử")

    def _create_output_tab(self):
        tab_output = QWidget()
        tab_output.setObjectName("outputTab")
        layout = QVBoxLayout(tab_output)
        layout.setSpacing(10)

        self.output_text_edit = QPlainTextEdit() 
        self.output_text_edit.setObjectName("outputTextEdit")
        self.output_text_edit.setReadOnly(True)
        layout.addWidget(self.output_text_edit)

        output_buttons_layout = QHBoxLayout()
        self.copy_output_btn = QPushButton("Sao chép Kết quả")
        self.copy_output_btn.setObjectName("secondaryButton")
        self.clear_output_btn = QPushButton("Xóa Kết quả")
        self.clear_output_btn.setObjectName("warningButton")
        self.ai_studio_btn = QPushButton("🚀 Mở AI Studio (và sao chép đường dẫn tệp)")
        self.ai_studio_btn.setObjectName("accentButton") 
        self.open_output_folder_btn = QPushButton("Mở Thư mục Đầu ra")
        self.open_output_folder_btn.setObjectName("primaryButton")
        
        output_buttons_layout.addWidget(self.copy_output_btn)
        output_buttons_layout.addWidget(self.clear_output_btn)
        output_buttons_layout.addStretch()
        output_buttons_layout.addWidget(self.ai_studio_btn)
        output_buttons_layout.addWidget(self.open_output_folder_btn)
        layout.addLayout(output_buttons_layout)
        self.tab_widget.addTab(tab_output, "Kết quả")

    def _create_status_bar(self, parent_layout):
        status_bar_widget = QFrame() 
        status_bar_widget.setObjectName("statusBar")
        status_bar_widget.setFixedHeight(30)
        status_layout = QHBoxLayout(status_bar_widget)
        status_layout.setContentsMargins(10, 0, 10, 0)

        self.status_label = QLabel("Sẵn sàng")
        self.status_label.setObjectName("statusLabel")
        self.progress_bar = QProgressBar()
        self.progress_bar.setObjectName("progressBar")
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0,100) 

        status_layout.addWidget(self.status_label)
        status_layout.addSpacerItem(QSpacerItem(20,0,QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum))
        status_layout.addWidget(self.progress_bar, 1) 
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


    def _on_output_format_changed(self, fmt, checked):
        if checked:
            self.output_format_str = fmt

    @Slot()
    def add_project_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Chọn Thư mục Dự án")
        if directory:
            directory = os.path.abspath(directory)
            items = [self.project_dir_list_widget.item(i).text() for i in range(self.project_dir_list_widget.count())]
            if directory not in items:
                self.project_dir_list_widget.addItem(QListWidgetItem(directory))
                self.project_dirs.append(directory) 
            else:
                QMessageBox.information(self, "Thông báo", "Thư mục bạn chọn đã có trong danh sách.")
        self._update_control_states()


    @Slot()
    def remove_project_directory(self):
        selected_items = self.project_dir_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Thông báo", "Vui lòng chọn ít nhất một thư mục để xóa.")
            return
        for item in selected_items:
            row = self.project_dir_list_widget.row(item)
            self.project_dir_list_widget.takeItem(row)
        self.project_dirs = [self.project_dir_list_widget.item(i).text() for i in range(self.project_dir_list_widget.count())]
        self._update_control_states()


    @Slot()
    def browse_output_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "Chọn Thư mục Đầu ra")
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
            QMessageBox.critical(self, "Lỗi", "Vui lòng chọn ít nhất một thư mục dự án.")
            return
        if not self.output_dir_path:
            QMessageBox.critical(self, "Lỗi", "Vui lòng chọn thư mục đầu ra.")
            return
        if not self.base_filename_str:
            QMessageBox.critical(self, "Lỗi", "Vui lòng nhập tên tệp cơ sở.")
            return
            
        self.tab_widget.setCurrentWidget(self.tab_widget.findChild(QWidget, "outputTab")) 
        self.output_text_edit.clear()
        self.status_label.setText("Đang xử lý...")
        self.progress_bar.setRange(0,0) 
        self._update_control_states(is_running=True)
        self.last_main_output_file = None

        self.worker_thread = QCoreThread()
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
        # Khi QThread finished, nó sẽ tự dọn dẹp worker nếu worker là con của thread.
        # Ở đây worker được moveToThread, deleteLater là cách tốt.

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
        self.status_label.setText(f"Hoàn tất! Tài liệu tại: {output_paths_str}")
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(100)
        self._update_control_states(is_running=False)

        all_output_files = [p.strip() for p in output_paths_str.split(",") if p.strip()]
        if all_output_files:
            self.last_main_output_file = all_output_files[0]

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
        
        # Ko can set worker_thread/doc_worker = None. deleteLater se xu ly.
        # Neu co flag yeu cau thoat, xu ly o day
        if self._is_exiting_initiated_by_user:
            self._is_exiting_initiated_by_user = False # Reset flag
            self.close() # Goi lai self.close() de kich hoat animation dong cua BaseMainWindow


    @Slot(str)
    def _on_documentation_error(self, error_message):
        self.output_text_edit.appendPlainText(f"Đã xảy ra lỗi nghiêm trọng:\n{error_message}")
        self.status_label.setText("Lỗi")
        self.progress_bar.setRange(0,100)
        self.progress_bar.setValue(0) 
        self._update_control_states(is_running=False)
        self.last_main_output_file = None

        # KTr worker_thread truoc khi thao tac, phong TH loi xay ra som
        if self.worker_thread and self.worker_thread.isRunning():
            # Ko can quit() va wait() o day vi da ket noi finished voi quit roi.
            # Neu loi xay ra truoc khi worker.run() hoan tat, worker.finished se ko emit.
            # Nhung error_occurred emit nghia la worker.run() da ket thuc (bang exception).
            # Slot deleteLater se duoc goi.
            pass
        
        # Ko can set worker_thread/doc_worker = None.
        if self._is_exiting_initiated_by_user:
            self._is_exiting_initiated_by_user = False # Reset flag
            self.close() 


    # --- History Functions ---
    def populate_history_listbox(self):
        self.history_list_widget.clear()
        for item in self.history_data:
            first_proj_dir = os.path.basename(item["project_dirs"][0]) if item.get("project_dirs") else "Không TM"
            if len(item.get("project_dirs", [])) > 1:
                first_proj_dir += " (+...)"
            
            try:
                dt_obj = datetime.fromisoformat(item["timestamp"])
                timestamp_str = dt_obj.strftime("%d/%m/%y %H:%M")
            except:
                timestamp_str = "N/A"
            
            display_name = item.get("name", first_proj_dir)
            if not display_name or display_name == "Không TM": display_name = first_proj_dir
            
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
            QMessageBox.warning(self, "Lỗi Lịch sử", "Tệp lịch sử bị lỗi và không thể đọc.")
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể tải lịch sử: {e}")
            self.history_data = []
        self.populate_history_listbox()
        self._update_control_states()


    def save_history_to_file(self):
        try:
            with open(self.history_file_path, "w", encoding="utf-8") as f:
                json.dump(self.history_data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            QMessageBox.critical(self, "Lỗi", f"Không thể lưu lịch sử: {e}")

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
            QMessageBox.information(self, "Thông Báo", "Vui lòng chọn một mục từ lịch sử.")
            return
        
        config_data = selected_items[0].data(Qt.ItemDataRole.UserRole) 
        if not config_data:
            QMessageBox.critical(self, "Lỗi", "Không thể lấy dữ liệu từ mục lịch sử đã chọn.")
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

        self.tab_widget.setCurrentWidget(self.tab_widget.findChild(QWidget, "configTab"))
        self._update_control_states()


    @Slot()
    def delete_selected_history_item(self):
        selected_items = self.history_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Thông Báo", "Vui lòng chọn một mục để xóa.")
            return
        
        confirm = QMessageBox.question(self, "Xác Nhận Xóa", "Bạn có chắc chắn muốn xóa mục lịch sử này?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            try:
                config_to_delete = selected_items[0].data(Qt.ItemDataRole.UserRole)
                self.history_data = [item for item in self.history_data if item != config_to_delete]
                
                self.save_history_to_file()
                self.populate_history_listbox() 
                QMessageBox.information(self, "Đã Xóa", "Mục lịch sử đã được xóa.")
            except Exception as e:
                 QMessageBox.critical(self, "Lỗi", f"Không thể xóa mục lịch sử: {str(e)}.")
        self._update_control_states()


    @Slot()
    def delete_all_history(self):
        if not self.history_data:
            QMessageBox.information(self, "Thông Báo", "Lịch sử trống.")
            return
        confirm = QMessageBox.question(self, "Xác Nhận Xóa Tất Cả", 
                                       "Bạn có chắc chắn muốn xóa TOÀN BỘ lịch sử chạy?",
                                       QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                       QMessageBox.StandardButton.No)
        if confirm == QMessageBox.StandardButton.Yes:
            self.history_data = []
            self.save_history_to_file()
            self.populate_history_listbox()
            QMessageBox.information(self, "Đã Xóa", "Toàn bộ lịch sử đã được xóa.")
        self._update_control_states()

    # --- Output Tab Functions ---
    @Slot()
    def copy_output_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text_edit.toPlainText())
        QMessageBox.information(self, "Đã sao chép", "Nội dung kết quả đã được sao chép.")

    @Slot()
    def clear_output_display(self):
        self.output_text_edit.clear()
        self.last_main_output_file = None
        self._update_control_states()


    @Slot()
    def open_output_folder_path(self):
        path_to_open = self.output_dir_entry.text() 
        if path_to_open and os.path.isdir(path_to_open):
            QDesktopServices.openUrl(f"file:///{os.path.normpath(path_to_open)}")
        else:
            QMessageBox.critical(self, "Lỗi", "Đường dẫn thư mục đầu ra không hợp lệ hoặc không tồn tại.")

    @Slot()
    def open_ai_studio_and_copy(self):
        ai_studio_url = "https://aistudio.google.com/app/prompts/new_chat" 
        if self.last_main_output_file and os.path.exists(self.last_main_output_file):
            try:
                QDesktopServices.openUrl(ai_studio_url)
                clipboard = QApplication.clipboard()
                clipboard.setText(self.last_main_output_file)
            except Exception as e:
                QMessageBox.critical(self, "Lỗi", f"Không thể mở AI Studio hoặc sao chép đường dẫn: {str(e)}")
        else:
            QMessageBox.warning(self, "Thông Báo", "Không tìm thấy tệp tài liệu để sao chép đường dẫn.")


    def _update_control_states(self, is_running=False):
        self.add_dir_btn.setEnabled(not is_running)
        self.remove_dir_btn.setEnabled(not is_running and self.project_dir_list_widget.count() > 0)
        self.output_dir_entry.setEnabled(not is_running)
        self.browse_output_btn.setEnabled(not is_running)
        self.base_filename_entry.setEnabled(not is_running)
        self.txt_radio.setEnabled(not is_running)
        self.md_radio.setEnabled(not is_running)
        self.verbose_checkbox.setEnabled(not is_running)
        self.run_button.setEnabled(not is_running and self.project_dir_list_widget.count() > 0)

        self.excluded_subdirs_entry.setEnabled(not is_running)
        self.excluded_files_entry.setEnabled(not is_running)

        has_history = self.history_list_widget.count() > 0
        has_selection = len(self.history_list_widget.selectedItems()) > 0
        self.load_history_btn.setEnabled(not is_running and has_selection)
        self.delete_history_btn.setEnabled(not is_running and has_selection)
        self.delete_all_history_btn.setEnabled(not is_running and has_history)

        has_output_text = bool(self.output_text_edit.toPlainText())
        self.copy_output_btn.setEnabled(has_output_text)
        self.clear_output_btn.setEnabled(has_output_text)
        self.ai_studio_btn.setEnabled(bool(self.last_main_output_file))
        self.open_output_folder_btn.setEnabled(os.path.isdir(self.output_dir_entry.text()))


    def _apply_qss_styles(self):
        default_font = QFont("Segoe UI", NORMAL_FONT_SIZE)
        QApplication.setFont(default_font)
        
        qss = f"""
            QWidget {{
                color: {TEXT_COLOR};
                font-size: {NORMAL_FONT_SIZE}pt;
            }}
            QMainWindow {{
                background: transparent; 
            }}
            QWidget#mainContainerWidget {{ 
                /* background-color: {WINDOW_BG_COLOR}; Da set trong BaseMainWindow */
                /* border-radius: 10px; */
            }}
            QWidget#mainContentWidget {{
                 background-color: transparent; 
                 padding: 10px;
            }}
             QWidget#contentAreaWithBackground {{
                border-bottom-left-radius: 10px;
                border-bottom-right-radius: 10px;
                background-color: transparent; 
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
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                subcontrol-position: top left;
                padding: 0 5px 0 5px;
                left: 10px;
                color: {SUBTEXT_COLOR};
                font-size: {NORMAL_FONT_SIZE + 1}pt;
                font-weight: bold;
            }}
            QLineEdit, QPlainTextEdit, QListWidget {{
                background-color: {INPUT_BG_COLOR};
                border: 1px solid {INPUT_BORDER_COLOR};
                border-radius: 6px;
                padding: 8px;
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
            QPushButton#warningButton {{ background-color: {WARNING_COLOR}; color: black; }}
            QPushButton#warningButton:hover {{ background-color: {QColor(WARNING_COLOR).lighter(120).name()}; }}
            QPushButton#errorButton {{ background-color: {ERROR_COLOR}; }}
            QPushButton#errorButton:hover {{ background-color: {QColor(ERROR_COLOR).lighter(120).name()}; }}

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
                background-color: transparent; 
            }}
            QLabel#statusLabel {{
                color: {SUBTEXT_COLOR};
                font-size: {SMALL_FONT_SIZE}pt;
            }}
        """
        self.setStyleSheet(qss)

    def closeEvent(self, event):
        # KTra xem co phai la dang dong tu animation cua BaseMainWindow ko
        if self._animation_is_closing_flag:
            event.accept() # Cho phep dong that
            return
        
        # KTra xem animation dong cua BaseMainWindow co dang chay ko
        if self.opacity_animation_close and self.opacity_animation_close.state() == QObject.property(" Estadual"): #.Running
             event.ignore() # De animation chay xong
             return

        # Neu co worker thread dang chay
        if self.worker_thread and self.worker_thread.isRunning():
            reply = QMessageBox.question(self, "Xác nhận thoát",
                                         "Một tác vụ đang chạy. Bạn có chắc muốn thoát?\n"
                                         "Ứng dụng sẽ đợi tác vụ hoàn thành trước khi đóng.",
                                         QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                         QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.Yes:
                self.run_button.setEnabled(False) 
                self.status_label.setText("Đang hoàn tất tác vụ trước khi thoát...")
                self._is_exiting_initiated_by_user = True 
                
                event.ignore()
                return 
            else:
                event.ignore() 
                return
        else:
            super().closeEvent(event)