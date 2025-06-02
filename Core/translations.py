# Core/translations.py

class Translations:
    LANG_VI = "vi"
    LANG_EN = "en"
    LANG_JA = "ja"

    # Map code voi ten hien thi
    lang_map = {
        LANG_VI: "Tiếng Việt",
        LANG_EN: "English",
        LANG_JA: "日本語"
    }

    # Chuoi dich
    translations = {
        # CustomTitleBar & BaseMainWindow
        "app_window_title_default": { # Tieu de cua so mac dinh
            LANG_VI: "Tạo Tài Liệu Dự Án",
            LANG_EN: "Project Document Generator",
            LANG_JA: "プロジェクトドキュメント生成"
        },
        "app_title_on_bar": { # Tieu de tren title bar
            LANG_VI: "Tạo Tài Liệu Dự Án",
            LANG_EN: "Project Document Generator",
            LANG_JA: "プロジェクトドキュメント生成"
        },
        "app_version_pyside6": {
            LANG_VI: "v3.1.0-PySide6", # Vd: Cap nhat phien ban
            LANG_EN: "v3.1.0-PySide6",
            LANG_JA: "v3.1.0-PySide6"
        },
        "base_mw_bg_load_fail_console": { # path
            LANG_VI: "Khong the tai hinh nen: {path}",
            LANG_EN: "Cannot load background image: {path}",
            LANG_JA: "背景画像を読み込めません: {path}"
        },
        "base_mw_bg_not_found_ui": {
            LANG_VI: "Khong tim thay hinh nen",
            LANG_EN: "Background image not found",
            LANG_JA: "背景画像が見つかりません"
        },
         # Config Tab
        "config_tab_title": {
            LANG_VI: "Cấu hình",
            LANG_EN: "Configuration",
            LANG_JA: "設定"
        },
        "project_dir_group_title": {
            LANG_VI: "Thư mục dự án",
            LANG_EN: "Project Directories",
            LANG_JA: "プロジェクトディレクトリ"
        },
        "add_dir_button": {
            LANG_VI: "Thêm thư mục",
            LANG_EN: "Add Directory",
            LANG_JA: "ディレクトリ追加"
        },
        "remove_dir_button": {
            LANG_VI: "Xóa thư mục đã chọn",
            LANG_EN: "Remove Selected",
            LANG_JA: "選択項目削除"
        },
        "output_settings_group_title": {
            LANG_VI: "Thiết lập đầu ra",
            LANG_EN: "Output Settings",
            LANG_JA: "出力設定"
        },
        "output_dir_label": {
            LANG_VI: "Thư mục đầu ra:",
            LANG_EN: "Output Directory:",
            LANG_JA: "出力ディレクトリ:"
        },
        "browse_button": {
            LANG_VI: "Duyệt...",
            LANG_EN: "Browse...",
            LANG_JA: "参照..."
        },
        "base_filename_label": {
            LANG_VI: "Tên tệp cơ sở:",
            LANG_EN: "Base Filename:",
            LANG_JA: "ベースファイル名:"
        },
        "output_format_label": {
            LANG_VI: "Định dạng:",
            LANG_EN: "Format:",
            LANG_JA: "フォーマット:"
        },
        "txt_radio_label": {
            LANG_VI: "Văn bản (.txt)",
            LANG_EN: "Text (.txt)",
            LANG_JA: "テキスト (.txt)"
        },
        "md_radio_label": {
            LANG_VI: "Markdown (.md)",
            LANG_EN: "Markdown (.md)",
            LANG_JA: "マークダウン (.md)"
        },
        "verbose_checkbox_label": {
            LANG_VI: "Chi tiết (verbose)",
            LANG_EN: "Verbose",
            LANG_JA: "詳細表示"
        },
        "run_button_text": {
            LANG_VI: "Tạo Tài Liệu",
            LANG_EN: "Generate Docs",
            LANG_JA: "ドキュメント生成"
        },
        # Advanced Tab
        "advanced_tab_title": {
            LANG_VI: "Nâng cao",
            LANG_EN: "Advanced",
            LANG_JA: "高度な設定"
        },
        "excluded_dirs_group_title": {
            LANG_VI: "Thư mục con loại trừ (cách nhau bởi dấu phẩy)",
            LANG_EN: "Excluded Subdirectories (comma-separated)",
            LANG_JA: "除外サブディレクトリ（カンマ区切り）"
        },
        "excluded_files_group_title": {
            LANG_VI: "Tệp loại trừ (đuôi tệp hoặc tên tệp, cách nhau bởi dấu phẩy)",
            LANG_EN: "Excluded Files (extensions or names, comma-separated)",
            LANG_JA: "除外ファイル（拡張子または名前、カンマ区切り）"
        },
        # History Tab
        "history_tab_title": {
            LANG_VI: "Lịch sử",
            LANG_EN: "History",
            LANG_JA: "履歴"
        },
        "history_group_title": {
            LANG_VI: "Lịch sử cấu hình đã chạy",
            LANG_EN: "Run History",
            LANG_JA: "実行履歴"
        },
        "load_history_button": {
            LANG_VI: "Tải Cấu Hình",
            LANG_EN: "Load Config",
            LANG_JA: "設定読込"
        },
        "delete_history_button": {
            LANG_VI: "Xóa Mục",
            LANG_EN: "Delete Entry",
            LANG_JA: "項目削除"
        },
        "delete_all_history_button": {
            LANG_VI: "Xóa Tất Cả",
            LANG_EN: "Delete All",
            LANG_JA: "すべて削除"
        },
        # Output Tab
        "output_tab_title": {
            LANG_VI: "Kết quả",
            LANG_EN: "Output",
            LANG_JA: "出力"
        },
        "copy_output_button": {
            LANG_VI: "Sao chép Kết quả",
            LANG_EN: "Copy Output",
            LANG_JA: "出力コピー"
        },
        "clear_output_button": {
            LANG_VI: "Xóa Kết quả",
            LANG_EN: "Clear Output",
            LANG_JA: "出力クリア"
        },
        "ai_studio_button": {
            LANG_VI: "🚀 Mở AI Studio (và sao chép đường dẫn tệp)",
            LANG_EN: "🚀 Open AI Studio (and copy file path)",
            LANG_JA: "🚀 AI Studioを開く (ファイルパスをコピー)"
        },
        "open_output_folder_button": {
            LANG_VI: "Mở Thư mục Đầu ra",
            LANG_EN: "Open Output Folder",
            LANG_JA: "出力フォルダを開く"
        },
        # Status Bar
        "status_ready": {
            LANG_VI: "Sẵn sàng",
            LANG_EN: "Ready",
            LANG_JA: "準備完了"
        },
        "status_processing": {
            LANG_VI: "Đang xử lý...",
            LANG_EN: "Processing...",
            LANG_JA: "処理中..."
        },
        "status_docs_generated_at": { # path
            LANG_VI: "Hoàn tất! Tài liệu tại: {path}",
            LANG_EN: "Done! Docs at: {path}",
            LANG_JA: "完了! ドキュメント場所: {path}"
        },
        "status_error": {
            LANG_VI: "Lỗi",
            LANG_EN: "Error",
            LANG_JA: "エラー"
        },
        "status_finishing_before_exit": {
             LANG_VI: "Đang hoàn tất tác vụ trước khi thoát...",
             LANG_EN: "Finishing task before exiting...",
             LANG_JA: "終了前にタスクを完了しています..."
        },
        # Messages / Dialogs
        "dialog_notice_title": { # Tieu de thong bao chung
            LANG_VI: "Thông báo",
            LANG_EN: "Notice",
            LANG_JA: "通知"
        },
        "dialog_error_title": { # Tieu de loi chung
            LANG_VI: "Lỗi",
            LANG_EN: "Error",
            LANG_JA: "エラー"
        },
        "dialog_confirm_delete_title": { # Tieu de xac nhan xoa
            LANG_VI: "Xác Nhận Xóa",
            LANG_EN: "Confirm Delete",
            LANG_JA: "削除の確認"
        },
        "dialog_deleted_title": { # Tieu de da xoa
            LANG_VI: "Đã Xóa",
            LANG_EN: "Deleted",
            LANG_JA: "削除済み"
        },
        "msg_dir_already_in_list_text": {
            LANG_VI: "Thư mục bạn chọn đã có trong danh sách.",
            LANG_EN: "The selected directory is already in the list.",
            LANG_JA: "選択されたディレクトリは既にリストにあります。"
        },
        "msg_select_dir_to_remove_text": {
            LANG_VI: "Vui lòng chọn ít nhất một thư mục để xóa.",
            LANG_EN: "Please select at least one directory to remove.",
            LANG_JA: "削除するディレクトリを少なくとも1つ選択してください。"
        },
        "msg_select_project_dir_text": {
            LANG_VI: "Vui lòng chọn ít nhất một thư mục dự án.",
            LANG_EN: "Please select at least one project directory.",
            LANG_JA: "少なくとも1つのプロジェクトディレクトリを選択してください。"
        },
        "msg_select_output_dir_text": {
            LANG_VI: "Vui lòng chọn thư mục đầu ra.",
            LANG_EN: "Please select an output directory.",
            LANG_JA: "出力ディレクトリを選択してください。"
        },
        "msg_enter_base_filename_text": {
            LANG_VI: "Vui lòng nhập tên tệp cơ sở.",
            LANG_EN: "Please enter a base filename.",
            LANG_JA: "ベースファイル名を入力してください。"
        },
        "worker_starting_generation": {
             LANG_VI: "Bắt đầu tạo tài liệu...",
             LANG_EN: "Starting document generation...",
             LANG_JA: "ドキュメント生成を開始しています..."
        },
        "worker_error_generic": { # error
             LANG_VI: "Lỗi trong worker: {error}",
             LANG_EN: "Error in worker: {error}",
             LANG_JA: "ワーカーエラー: {error}"
        },
        "critical_error_occurred": { # error_message
            LANG_VI: "Đã xảy ra lỗi nghiêm trọng:\n{error_message}",
            LANG_EN: "A critical error occurred:\n{error_message}",
            LANG_JA: "重大なエラーが発生しました:\n{error_message}"
        },
        "history_no_tm": { 
            LANG_VI: "Không TM",
            LANG_EN: "No Dir",
            LANG_JA: "ディレクトリなし"
        },
        "history_timestamp_na": {
            LANG_VI: "N/A",
            LANG_EN: "N/A",
            LANG_JA: "N/A"
        },
        "history_file_corrupted_title": { # Su dung dialog_error_title
            LANG_VI: "Lỗi Lịch sử", # Giu lai de phan biet
            LANG_EN: "History Error",
            LANG_JA: "履歴エラー"
        },
        "history_file_corrupted_text": {
            LANG_VI: "Tệp lịch sử bị lỗi và không thể đọc.",
            LANG_EN: "History file is corrupted and cannot be read.",
            LANG_JA: "履歴ファイルが破損しており、読み取れません。"
        },
        "history_load_error_text": { # error
            LANG_VI: "Không thể tải lịch sử: {error}",
            LANG_EN: "Could not load history: {error}",
            LANG_JA: "履歴を読み込めませんでした: {error}"
        },
        "history_save_error_text": { # error
            LANG_VI: "Không thể lưu lịch sử: {error}",
            LANG_EN: "Could not save history: {error}",
            LANG_JA: "履歴を保存できませんでした: {error}"
        },
        "msg_select_history_item_text": {
            LANG_VI: "Vui lòng chọn một mục từ lịch sử.",
            LANG_EN: "Please select an item from history.",
            LANG_JA: "履歴から項目を選択してください。"
        },
        "history_item_load_error_text": {
            LANG_VI: "Không thể lấy dữ liệu từ mục lịch sử đã chọn.",
            LANG_EN: "Could not retrieve data from selected history item.",
            LANG_JA: "選択された履歴項目からデータを取得できませんでした。"
        },
        "confirm_delete_history_item_text": {
            LANG_VI: "Bạn có chắc chắn muốn xóa mục lịch sử này?",
            LANG_EN: "Are you sure you want to delete this history item?",
            LANG_JA: "この履歴項目を削除してもよろしいですか？"
        },
        "history_item_deleted_text": {
            LANG_VI: "Mục lịch sử đã được xóa.",
            LANG_EN: "History item has been deleted.",
            LANG_JA: "履歴項目が削除されました。"
        },
        "history_delete_error_text": { # error
            LANG_VI: "Không thể xóa mục lịch sử: {error}",
            LANG_EN: "Could not delete history item: {error}",
            LANG_JA: "履歴項目を削除できませんでした: {error}"
        },
        "history_empty_text": {
            LANG_VI: "Lịch sử trống.",
            LANG_EN: "History is empty.",
            LANG_JA: "履歴は空です。"
        },
        "confirm_delete_all_history_text": {
            LANG_VI: "Bạn có chắc chắn muốn xóa TOÀN BỘ lịch sử chạy?",
            LANG_EN: "Are you sure you want to delete THE ENTIRE run history?",
            LANG_JA: "実行履歴全体を削除してもよろしいですか？"
        },
        "all_history_deleted_text": {
            LANG_VI: "Toàn bộ lịch sử đã được xóa.",
            LANG_EN: "Entire history has been deleted.",
            LANG_JA: "すべての履歴が削除されました。"
        },
        "output_copied_text": {
            LANG_VI: "Nội dung kết quả đã được sao chép.",
            LANG_EN: "Output content has been copied.",
            LANG_JA: "出力内容がコピーされました。"
        },
        "cannot_open_folder_text": { # error
            LANG_VI: "Không thể mở thư mục: {error}",
            LANG_EN: "Cannot open folder: {error}",
            LANG_JA: "フォルダを開けません: {error}"
        },
        "invalid_output_folder_path_text": {
            LANG_VI: "Đường dẫn thư mục đầu ra không hợp lệ hoặc không tồn tại.",
            LANG_EN: "Output folder path is invalid or does not exist.",
            LANG_JA: "出力フォルダパスが無効か、存在しません。"
        },
        "ai_studio_opened_path_copied_text": { # path
            LANG_VI: "Đã mở AI Studio và sao chép đường dẫn tệp:\n{path}\nvào clipboard.",
            LANG_EN: "Opened AI Studio and copied file path:\n{path}\nto clipboard.",
            LANG_JA: "AI Studioを開き、ファイルパスをコピーしました:\n{path}\nクリップボードへ。"
        },
        "cannot_open_ai_studio_text": { # error
            LANG_VI: "Không thể mở AI Studio hoặc sao chép đường dẫn: {error}",
            LANG_EN: "Cannot open AI Studio or copy path: {error}",
            LANG_JA: "AI Studioを開くかパスをコピーできません: {error}"
        },
        "no_doc_file_to_copy_path_text": {
            LANG_VI: "Không tìm thấy tệp tài liệu để sao chép đường dẫn.\nHãy chạy tạo tài liệu trước.",
            LANG_EN: "No document file found to copy path.\nPlease generate document first.",
            LANG_JA: "パスをコピーするドキュメントファイルが見つかりません。\nまずドキュメントを生成してください。"
        },
        "confirm_exit_text": {
            LANG_VI: "Một tác vụ đang chạy. Bạn có chắc muốn thoát?\nỨng dụng sẽ đợi tác vụ hoàn thành trước khi đóng.",
            LANG_EN: "A task is running. Are you sure you want to exit?\nThe application will wait for the task to complete before closing.",
            LANG_JA: "タスク実行中です。終了しますか？\nアプリケーションはタスク完了後に終了します。"
        },
        # gui_utils.format_output_for_tkinter
        "output_complete_status": { # time
            LANG_VI: "✨ Hoàn tất ({time:.2f}s) ✨",
            LANG_EN: "✨ Complete ({time:.2f}s) ✨",
            LANG_JA: "✨ 完了 ({time:.2f}秒) ✨"
        },
        "output_message_prefix": { # message
            LANG_VI: "✅ {message}",
            LANG_EN: "✅ {message}",
            LANG_JA: "✅ {message}"
        },
        "output_folders_scanned": { # num_folders
            LANG_VI: "📁 Thư mục đã quét: {num_folders}",
            LANG_EN: "📁 Folders scanned: {num_folders}",
            LANG_JA: "📁 スキャン済みフォルダ: {num_folders}"
        },
        "output_files_scanned": { # num_files
            LANG_VI: "📄 Tệp đã quét: {num_files}",
            LANG_EN: "📄 Files scanned: {num_files}",
            LANG_JA: "📄 スキャン済みファイル: {num_files}"
        },
        "output_skipped_folders_header": {
            LANG_VI: "📂 Thư mục bỏ qua:",
            LANG_EN: "📂 Skipped Folders:",
            LANG_JA: "📂 スキップされたフォルダ:"
        },
        "output_skipped_files_header": {
            LANG_VI: "📄 Tệp bỏ qua:",
            LANG_EN: "📄 Skipped Files:",
            LANG_JA: "📄 スキップされたファイル:"
        },
        "output_errors_header": {
            LANG_VI: "❌ Lỗi:",
            LANG_EN: "❌ Errors:",
            LANG_JA: "❌ エラー:"
        },
        "output_error_not_found": { # item
            LANG_VI: "{item}: Không tìm thấy tệp/TM",
            LANG_EN: "{item}: File/Folder not found",
            LANG_JA: "{item}: ファイル/フォルダが見つかりません"
        },
        "output_error_permission": { # item
            LANG_VI: "{item}: Lỗi truy cập",
            LANG_EN: "{item}: Permission error",
            LANG_JA: "{item}: アクセスエラー"
        },
        "output_error_generic_item": { # item, msg
            LANG_VI: "{item}: {msg}",
            LANG_EN: "{item}: {msg}",
            LANG_JA: "{item}: {msg}"
        },
        # app_logic.tao_tai_lieu_du_an (errors from this module)
        "applogic_err_path_type": {
            LANG_VI: "duong_dan_thu_muc phai la list/tuple",
            LANG_EN: "project_paths must be a list/tuple",
            LANG_JA: "project_paths は list/tuple である必要があります"
        },
        "applogic_err_path_empty": {
            LANG_VI: "duong_dan_thu_muc khong rong",
            LANG_EN: "project_paths cannot be empty",
            LANG_JA: "project_paths は空にできません"
        },
        "applogic_err_output_format": {
            LANG_VI: "output_format phai la 'txt'/'markdown'",
            LANG_EN: "output_format must be 'txt' or 'markdown'",
            LANG_JA: "output_format は 'txt' または 'markdown' である必要があります"
        },
        "applogic_folder_not_exist_val": { # Gia tri cho dict loi
            LANG_VI: "Thu muc khong ton tai",
            LANG_EN: "Folder does not exist",
            LANG_JA: "フォルダが存在しません"
        },
        "applogic_file_not_found_note": { # path. Hien thi trong file output
            LANG_VI: "Khong tim thay tep {path}...",
            LANG_EN: "File {path} not found...",
            LANG_JA: "ファイル {path} が見つかりません..."
        },
        "applogic_file_not_found_val": { # Gia tri cho dict loi
            LANG_VI: "Khong tim thay tep",
            LANG_EN: "File not found",
            LANG_JA: "ファイルが見つかりません"
        },
        "applogic_permission_denied_note": { # path. Hien thi trong file output
            LANG_VI: "Khong co quyen truy cap tep {path}...",
            LANG_EN: "Permission denied for file {path}...",
            LANG_JA: "ファイル {path} へのアクセス権がありません..."
        },
        "applogic_permission_denied_val": { # Gia tri cho dict loi
            LANG_VI: "Khong co quyen truy cap",
            LANG_EN: "Permission denied",
            LANG_JA: "アクセス権がありません"
        },
        "applogic_os_error_reading_file_note": { # path, error. Hien thi trong file output
            LANG_VI: "Loi doc tep {path}: {error}",
            LANG_EN: "OS error reading file {path}: {error}",
            LANG_JA: "ファイル {path} の読み取り中にOSエラー: {error}"
        },
        "applogic_os_error_val": { # error. Gia tri cho dict loi
            LANG_VI: "Loi he thong: {error}",
            LANG_EN: "System error: {error}",
            LANG_JA: "システムエラー: {error}"
        },
        "applogic_project_title_md": { # project_name
            LANG_VI: "# Du an: {project_name} - ...",
            LANG_EN: "# Project: {project_name} - ...",
            LANG_JA: "# プロジェクト: {project_name} - ..."
        },
        "applogic_project_title_txt": { # project_name
            LANG_VI: "Du an: {project_name} - ...",
            LANG_EN: "Project: {project_name} - ...",
            LANG_JA: "プロジェクト: {project_name} - ..."
        },
        "applogic_excluded_suffix": {
            LANG_VI: "/ (Ko liet ke)",
            LANG_EN: "/ (Not listed)",
            LANG_JA: "/ (リストされていません)"
        },
        "applogic_dir_not_found_suffix": {
             LANG_VI: "/ (Khong tim thay)",
             LANG_EN: "/ (Not found)",
             LANG_JA: "/ (見つかりません)"
        },
        "applogic_dir_permission_suffix": {
             LANG_VI: "/ (Khong co quyen)",
             LANG_EN: "/ (No permission)",
             LANG_JA: "/ (権限なし)"
        },
        "applogic_dir_os_error_suffix": { # error
             LANG_VI: "/ (Loi HDH: {error})",
             LANG_EN: "/ (OS Error: {error})",
             LANG_JA: "/ (OSエラー: {error})"
        },
        "applogic_cannot_read_file_note_generic": { # path, error. Hien thi trong file output
            LANG_VI: "Khong the doc tep {path}: {error}",
            LANG_EN: "Cannot read file {path}: {error}",
            LANG_JA: "ファイル {path} を読み取れません: {error}"
        },
        "applogic_encoding_warning_note": {
            LANG_VI: "\n\n_(Luu y: Tep co the ko ma hoa UTF-8, ND doc bang latin-1)_\n",
            LANG_EN: "\n\n_(Note: File might not be UTF-8 encoded, content read as latin-1)_\n",
            LANG_JA: "\n\n_(注意: ファイルがUTF-8エンコードでない可能性があります。内容はlatin-1として読み込まれました)_\n"
        },
         "applogic_dir_not_found_content_val": { # Gia tri cho dict loi
            LANG_VI: "Khong tim thay thu muc (khi doc ND)",
            LANG_EN: "Directory not found (when reading content)",
            LANG_JA: "ディレクトリが見つかりません (内容読み取り時)"
        },
        "applogic_dir_permission_content_val": { # Gia tri cho dict loi
            LANG_VI: "Khong co quyen truy cap (khi doc ND)",
            LANG_EN: "Permission denied (when reading content)",
            LANG_JA: "アクセス権がありません (内容読み取り時)"
        },
        "applogic_os_error_content_val": { # error. Gia tri cho dict loi
            LANG_VI: "Loi he thong (khi doc ND): {error}",
            LANG_EN: "System error (when reading content): {error}",
            LANG_JA: "システムエラー (内容読み取り時): {error}"
        },
        "applogic_docs_created_in_msg": { # output_dir
            LANG_VI: "Tai lieu du an da tao trong {output_dir}",
            LANG_EN: "Project documents created in {output_dir}",
            LANG_JA: "プロジェクトドキュメントが {output_dir} に作成されました"
        },
        "applogic_verbose_processed_msg": { # files, folders
            LANG_VI: "\nDa xu ly {files} tep va {folders} thu muc.",
            LANG_EN: "\nProcessed {files} files and {folders} folders.",
            LANG_JA: "\n{files} ファイルと {folders} フォルダを処理しました。"
        },
        # run_app.py
        "run_app_icon_not_found_console": { # path
            LANG_VI: "Khong tim thay icon ung dung: {path}",
            LANG_EN: "Application icon not found: {path}",
            LANG_JA: "アプリアイコンが見つかりません: {path}"
        },
        # Config file messages
        "config_file_default_path": { # path
            LANG_VI: "INFO: Đang sử dụng tệp cấu hình mặc định: {path}",
            LANG_EN: "INFO: Using default configuration file: {path}",
            LANG_JA: "INFO: デフォルト設定ファイルを使用中: {path}"
        },
        "config_file_loaded_path": { # path
            LANG_VI: "INFO: Đã tải cấu hình từ: {path}",
            LANG_EN: "INFO: Configuration loaded from: {path}",
            LANG_JA: "INFO: 設定ファイルを読み込みました: {path}"
        },
        "config_file_load_error": { # path, error
            LANG_VI: "LƯU Ý: Không thể tải tệp cấu hình '{path}': {error}. Sử dụng cài đặt mặc định.",
            LANG_EN: "WARNING: Could not load config file '{path}': {error}. Using default settings.",
            LANG_JA: "警告: 設定ファイル '{path}' を読み込めませんでした: {error}。デフォルト設定を使用します。"
        },
        "config_file_save_error": { # path, error
            LANG_VI: "LỖI: Không thể lưu tệp cấu hình '{path}': {error}",
            LANG_EN: "ERROR: Could not save config file '{path}': {error}",
            LANG_JA: "エラー: 設定ファイル '{path}' を保存できませんでした: {error}"
        }
    }
    current_lang = LANG_EN # Mac dinh tieng Anh

    @classmethod
    def set_language(cls, lang_code): # Dat ngon ngu
        if lang_code in cls.lang_map:
            cls.current_lang = lang_code
        else: 
            print(f"Unsupported language: {lang_code}. Defaulting to {cls.LANG_EN}")
            cls.current_lang = cls.LANG_EN # Mac dinh Anh neu ko ho tro

    @classmethod
    def get(cls, key, **kwargs): 
        try:
            translation_dict = cls.translations[key]
            raw_translation = translation_dict.get(cls.current_lang, translation_dict.get(cls.LANG_EN, key))
            return raw_translation.format(**kwargs) if kwargs else raw_translation
        except KeyError:
            if cls.current_lang != cls.LANG_EN and key in cls.translations and cls.LANG_EN in cls.translations[key]:
                raw_translation_en = cls.translations[key].get(cls.LANG_EN)
                return raw_translation_en.format(**kwargs) if kwargs and raw_translation_en else raw_translation_en if raw_translation_en else key.upper()
            return key.upper() 

    @classmethod
    def get_current_lang_display_name(cls):
        return cls.lang_map.get(cls.current_lang, "Unknown Language")