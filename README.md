# Doc_Project_Tool - Effortlessly Generate Project Documentation 📄✨

## Demo

A brief demonstration of the Doc_Project_Tool in action:
![image](https://github.com/user-attachments/assets/de5d748c-654f-4800-8297-b50f49db1a1a)


**Output:**
![image](https://github.com/user-attachments/assets/e4ddafc9-b3de-4c4f-acca-fe7f386eac73)

---
## DOCS:

<!-- English -->
<details>
<summary>🇬🇧 English (Detailed)</summary>

## Overview

**Doc_Project_Tool** is a desktop application designed to streamline the process of creating comprehensive documentation for software projects. It scans selected project directories, outlines the file structure, and concatenates the content of supported source code files into a single, organized document. This tool is particularly useful for preparing project overviews for Large Language Models (LLMs), code reviews, or archiving.

Built with Python and PySide6, it offers a modern, user-friendly, and customizable interface with support for multiple languages.

## Important Notes

*   📜 **Configuration File:** User-specific settings such as preferred language, window size, and position are saved in `Core/doc_tool_config.json`.
*   💾 **History File:** Past run configurations (project paths, output settings, exclusions) are stored in `Core/doc_tool_history.json`, allowing for quick reloading of previous settings.
*   🚀 **Automated Setup:** `run.bat` (for Windows) and `run.sh` (for Linux/macOS) scripts are provided to automate the creation of a virtual environment (named `moitruongao`) and the installation of necessary dependencies, ensuring a smooth startup.

## Key Features

*   **Comprehensive Documentation Generation:**
    *   Select one or multiple project directories to include in the documentation.
    *   Specify a custom output directory and a base filename for the generated document.
    *   Choose between Text (`.txt`) or Markdown (`.md`) output formats.
    *   Optional "Verbose" mode to include detailed processing statistics (file/folder counts) in the output summary.
*   **Advanced Exclusion Filters:**
    *   Exclude specific subdirectories by name (e.g., `__pycache__`, `.git`, `venv`, `node_modules`).
    *   Exclude files by their extension (e.g., `.pyc`, `.log`) or full name.
*   **Intuitive & User-Friendly Interface (PySide6):**
    *   Modern tabbed layout for easy navigation: Configuration, Advanced, History, and Output.
    *   Custom-styled title bar with standard window controls (minimize, maximize, close) and a language selection dropdown.
    *   Full support for window dragging, resizing, and smooth open/close animations.
    *   Persistent window state (size, position, maximized status) across sessions.
*   **Multilingual Support:**
    *   Interface available in English, Vietnamese (Tiếng Việt), and Japanese (日本語).
    *   Easily switch languages on-the-fly from the title bar.
*   **Run History Management:**
    *   Automatically saves the configuration of successful documentation generation runs.
    *   View a list of past runs with timestamps and project names.
    *   Load settings from a history entry with a single click or double-click.
    *   Delete individual history entries or clear the entire history.
*   **Output & Status Management:**
    *   The "Output" tab displays a summary of the generation process, including execution time, number of files/folders processed, skipped items, and any errors encountered.
    *   Buttons to copy the output summary to the clipboard or clear the display.
    *   Convenient "Open Output Folder" button to quickly access the directory containing the generated document.
    *   Special "🚀 Open AI Studio (and copy file path)" button:
        *   Opens the AI Studio website (or a similar LLM interface).
        *   Copies the full path of the *main generated document file* to the clipboard. This makes it easy to reference or upload the document for AI analysis.
*   **Efficient Background Processing:**
    *   The core documentation generation logic (`tao_tai_lieu_du_an`) runs in a separate worker thread (DocWorker) to keep the UI responsive during processing.
    *   A progress bar and status messages in the status bar provide real-time feedback.
*   **Cross-Platform Compatibility:**
    *   Designed to run on Windows, Linux, and macOS.
    *   Setup scripts (`run.bat`, `run.sh`) simplify installation on different operating systems.
*   **Clear Feedback Mechanisms:**
    *   A dedicated status bar shows the application's current state (Ready, Processing, Done, Error).
    *   Informative dialog boxes for confirmations, errors, and notices.

## Prerequisites (To run from source)

1.  **Python:** Python 3.x is recommended. The setup scripts will attempt to use the `python` or `python3` command available in your system's PATH.
2.  **Pip:** The Python package installer (usually comes with Python).

## Installation & Running (From source)

The easiest and recommended way to run the application is by using the provided automation scripts:

### Using Scripts (Recommended)

1.  **Download Source Code:**
    *   Clone this repository or download it as a ZIP file and extract it.

2.  **Run the setup and launch script:**
    *   **On Windows:**
        1.  Navigate to the `windows` directory within the project's root folder.
        2.  Double-click `run.bat`.
    *   **On Linux/macOS:**
        1.  Open a Terminal.
        2.  Navigate to the `linux-mac` directory within the project's root folder.
        3.  Make the script executable: `chmod +x run.sh`
        4.  Run the script: `./run.sh`

    These scripts will automatically:
    *   Check for and create a Python virtual environment named `moitruongao` in the project root (if it doesn't exist).
    *   Activate the virtual environment.
    *   Install all dependencies listed in `requirements.txt`.
    *   Launch the Doc_Project_Tool application.

### Manual Setup (Advanced Option)

1.  **Download Source Code** (as above).
2.  Open a Terminal or Command Prompt and navigate to the project's root directory.
3.  **(Recommended)** Create and activate a Python virtual environment:
    ```bash
    python -m venv moitruongao
    ```
    *   On Windows: `moitruongao\Scripts\activate`
    *   On Linux/macOS: `source moitruongao/bin/activate`
4.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
5.  Run the application:
    ```bash
    python run_app.py
    ```

## User Guide

Once the application is running:

### General Settings

*   **Language Selection:** Use the dropdown menu on the right side of the title bar to change the application's language.
*   **Window Operations:** The window can be moved by dragging the title bar, resized by dragging its edges/corners, and controlled using the minimize, maximize/restore, and close buttons on the title bar.

### Configuration Tab (`Config Tab`)

This is the main tab for setting up your documentation task.

*   **Project Directories:**
    *   **List Area:** Displays the project directories you've added.
    *   **"Add Directory" button:** Opens a dialog to select a project folder to be included.
    *   **"Remove Selected" button:** Removes the currently selected directory/directories from the list.
*   **Output Settings:**
    *   **"Output Directory:" field:** Shows the path where the generated document(s) will be saved.
    *   **"Browse..." button:** Opens a dialog to choose the output directory.
    *   **"Base Filename:" field:** Enter the desired base name for your output file (e.g., `project_docs`). The extension (`.txt` or `.md`) will be added automatically. If a file with the same name exists, a number will be appended (e.g., `project_docs 1.txt`).
    *   **"Format:" options:**
        *   **Text (.txt):** Generates a plain text document.
        *   **Markdown (.md):** Generates a Markdown document.
    *   **"Verbose" checkbox:** If checked, the summary in the "Output" tab will include counts of processed files and folders.
*   **"Generate Docs" button:** Click this button to start the documentation generation process. It's enabled only if at least one project directory is added.

### Advanced Tab

Customize exclusion rules here.

*   **"Excluded Subdirectories (comma-separated)" field:** Enter a comma-separated list of subdirectory names that should be skipped during scanning (e.g., `__pycache__, .venv, node_modules`).
*   **"Excluded Files (extensions or names, comma-separated)" field:** Enter a comma-separated list of file extensions (e.g., `.log, .tmp`) or full filenames (e.g., `config.backup.json`) to exclude.

### History Tab

Manage and reuse past configurations.

*   **History List:** Displays a list of previously successful documentation runs, identified by project name and timestamp.
*   **"Load Config" button:** Loads all settings (project paths, output settings, exclusions) from the selected history item back into the "Configuration" and "Advanced" tabs. You can also double-click an item to load it.
*   **"Delete Entry" button:** Deletes the selected history item(s). A confirmation will be required.
*   **"Delete All" button:** Deletes all entries from the history. A confirmation will be required.

### Output Tab

View results and access generated files.

*   **Text Area:** Displays a summary of the most recent documentation generation process. This includes:
    *   Execution time.
    *   Path to the generated document(s).
    *   Counts of processed files and folders (if "Verbose" was enabled).
    *   Lists of skipped folders and files.
    *   Any errors encountered during the process.
*   **"Copy Output" button:** Copies the entire content of the summary text area to the clipboard.
*   **"Clear Output" button:** Clears the summary text area.
*   **"🚀 Open AI Studio (and copy file path)" button:**
    1.  Opens the AI Studio website in your default web browser.
    2.  Copies the full path of the *primary generated document file* from the last run to your clipboard. You can then easily reference this path or use it to locate and upload the file to an LLM.
    *   *Note: This button is enabled only if a document was successfully generated in the last run and the file still exists.*
*   **"Open Output Folder" button:** Opens the configured output directory (from the "Configuration" tab) in your system's file explorer.

### Status Bar

Located at the bottom of the window:

*   **Status Label:** Displays messages about the application's current state (e.g., "Ready", "Processing...", "Done! Docs at: ...", "Error").
*   **Progress Bar:** Shows the progress of the documentation generation process. It will be indeterminate (animated) during processing and fill up upon completion.

## Project Structure

```
Doc_Project_Tool/
├── .git/                     # Git repository data (Not typically included in distribution)
├── assets/
│   └── icon.ico              # Application icon
├── Core/                     # Core application logic and UI components
│   ├── __pycache__/          # Python cache files (Not typically included)
│   ├── app_logic.py          # Main documentation generation logic
│   ├── base_main_window.py   # Base class for the main window (frameless, custom title bar)
│   ├── constants.py          # Application-wide constants
│   ├── custom_title_bar.py   # Custom title bar widget
│   ├── doc_tool_config.json  # Stores user preferences (language, window state)
│   ├── doc_tool_history.json # Stores run history
│   ├── gui_components.py     # Contains a CustomScrolledText widget using customtkinter (may be for auxiliary use or experimental)
│   ├── gui_utils.py          # Utility functions for the GUI
│   ├── main_app.py           # Main application class (PySide6 UI and logic)
│   └── translations.py       # Multilingual translation strings
├── linux-mac/
│   └── run.sh                # Setup and run script for Linux/macOS
├── moitruongao/              # Python virtual environment (created by run scripts, not in repo)
├── windows/
│   └── run.bat               # Setup and run script for Windows
├── .gitignore                # Specifies intentionally untracked files that Git should ignore
├── requirements.txt          # List of Python dependencies
└── run_app.py                # Main entry point script to launch the application
```

## Technologies Used

*   **Python:** The primary programming language.
*   **PySide6:** The official Python bindings for Qt, used for building the graphical user interface.
*   **customtkinter:** Listed as a dependency; a `CustomScrolledText` component using it exists in `Core/gui_components.py`. The main application GUI, however, is built with PySide6.
*   **markdown:** Listed as a dependency, potentially for Markdown processing if specific features are added in the future (the current Markdown output is direct text writing).

</details>

<!-- Vietnamese -->
<details>
<summary>🇻🇳 Tiếng Việt (Chi tiết)</summary>

## Tổng quan

**Doc_Project_Tool** là một ứng dụng máy tính để bàn được thiết kế để đơn giản hóa quy trình tạo tài liệu toàn diện cho các dự án phần mềm. Ứng dụng quét các thư mục dự án đã chọn, phác thảo cấu trúc tệp và ghép nối nội dung của các tệp mã nguồn được hỗ trợ thành một tài liệu duy nhất, có tổ chức. Công cụ này đặc biệt hữu ích để chuẩn bị tổng quan dự án cho các Mô hình Ngôn ngữ Lớn (LLM), đánh giá mã nguồn hoặc lưu trữ.

Được xây dựng bằng Python và PySide6, ứng dụng cung cấp giao diện hiện đại, thân thiện với người dùng, tùy biến được và hỗ trợ đa ngôn ngữ.

## Lưu ý quan trọng

*   📜 **Tệp Cấu hình:** Các cài đặt cụ thể của người dùng như ngôn ngữ ưu tiên, kích thước và vị trí cửa sổ được lưu trong `Core/doc_tool_config.json`.
*   💾 **Tệp Lịch sử:** Các cấu hình chạy trước đó (đường dẫn dự án, cài đặt đầu ra, loại trừ) được lưu trữ trong `Core/doc_tool_history.json`, cho phép tải lại nhanh chóng các cài đặt cũ.
*   🚀 **Thiết lập Tự động:** Các tệp `run.bat` (cho Windows) và `run.sh` (cho Linux/macOS) được cung cấp để tự động hóa việc tạo môi trường ảo (tên là `moitruongao`) và cài đặt các thư viện cần thiết, đảm bảo khởi động trơn tru.

## Tính năng nổi bật

*   **Tạo Tài liệu Toàn diện:**
    *   Chọn một hoặc nhiều thư mục dự án để bao gồm trong tài liệu.
    *   Chỉ định thư mục đầu ra tùy chỉnh và tên tệp cơ sở cho tài liệu được tạo.
    *   Chọn giữa định dạng đầu ra Văn bản (`.txt`) hoặc Markdown (`.md`).
    *   Chế độ "Chi tiết (verbose)" tùy chọn để bao gồm thông tin thống kê xử lý chi tiết (số lượng tệp/thư mục) trong bản tóm tắt đầu ra.
*   **Bộ lọc Loại trừ Nâng cao:**
    *   Loại trừ các thư mục con cụ thể theo tên (ví dụ: `__pycache__`, `.git`, `venv`, `node_modules`).
    *   Loại trừ tệp theo phần mở rộng (ví dụ: `.pyc`, `.log`) hoặc tên đầy đủ.
*   **Giao diện Trực quan & Thân thiện với Người dùng (PySide6):**
    *   Giao diện theo thẻ hiện đại để dễ dàng điều hướng: Cấu hình, Nâng cao, Lịch sử và Kết quả.
    *   Thanh tiêu đề tùy chỉnh với các nút điều khiển cửa sổ tiêu chuẩn (thu nhỏ, phóng to, đóng) và menu thả xuống chọn ngôn ngữ.
    *   Hỗ trợ đầy đủ kéo thả cửa sổ, thay đổi kích thước và hiệu ứng động mượt mà khi mở/đóng.
    *   Trạng thái cửa sổ (kích thước, vị trí, trạng thái phóng to) được lưu trữ qua các phiên làm việc.
*   **Hỗ trợ Đa ngôn ngữ:**
    *   Giao diện có sẵn bằng Tiếng Anh (English), Tiếng Việt (Vietnamese), và Tiếng Nhật (日本語).
    *   Dễ dàng chuyển đổi ngôn ngữ trực tiếp từ thanh tiêu đề.
*   **Quản lý Lịch sử Chạy:**
    *   Tự động lưu cấu hình của các lần tạo tài liệu thành công.
    *   Xem danh sách các lần chạy trước đó với dấu thời gian và tên dự án.
    *   Tải cài đặt từ một mục lịch sử bằng một cú nhấp chuột hoặc nhấp đúp.
    *   Xóa các mục lịch sử riêng lẻ hoặc xóa toàn bộ lịch sử.
*   **Quản lý Kết quả & Trạng thái:**
    *   Tab "Kết quả" hiển thị bản tóm tắt của quá trình tạo tài liệu, bao gồm thời gian thực thi, số lượng tệp/thư mục đã xử lý, các mục bị bỏ qua và bất kỳ lỗi nào gặp phải.
    *   Các nút để sao chép bản tóm tắt đầu ra vào clipboard hoặc xóa hiển thị.
    *   Nút "Mở Thư mục Đầu ra" tiện lợi để truy cập nhanh vào thư mục chứa tài liệu đã tạo.
    *   Nút đặc biệt "🚀 Mở AI Studio (và sao chép đường dẫn tệp)":
        *   Mở trang web AI Studio (hoặc một giao diện LLM tương tự).
        *   Sao chép đường dẫn đầy đủ của *tệp tài liệu chính được tạo* vào clipboard. Điều này giúp dễ dàng tham chiếu hoặc tải lên tài liệu để phân tích bằng AI.
*   **Xử lý Nền Hiệu quả:**
    *   Logic tạo tài liệu cốt lõi (`tao_tai_lieu_du_an`) chạy trong một luồng worker riêng (DocWorker) để giữ cho giao diện người dùng phản hồi nhanh trong quá trình xử lý.
    *   Thanh tiến trình và thông báo trạng thái trên thanh trạng thái cung cấp phản hồi theo thời gian thực.
*   **Tương thích Đa nền tảng:**
    *   Được thiết kế để chạy trên Windows, Linux và macOS.
    *   Các script thiết lập (`run.bat`, `run.sh`) đơn giản hóa việc cài đặt trên các hệ điều hành khác nhau.
*   **Cơ chế Phản hồi Rõ ràng:**
    *   Thanh trạng thái chuyên dụng hiển thị trạng thái hiện tại của ứng dụng (Sẵn sàng, Đang xử lý, Hoàn tất! Tài liệu tại: ..., Lỗi).
    *   Các hộp thoại thông tin để xác nhận, báo lỗi và thông báo.

## Điều kiện tiên quyết (Để chạy từ mã nguồn)

1.  **Python:** Khuyến nghị sử dụng Python 3.x. Các script thiết lập sẽ cố gắng sử dụng lệnh `python` hoặc `python3` có sẵn trong PATH hệ thống của bạn.
2.  **Pip:** Trình quản lý gói Python (thường được cài đặt sẵn cùng với Python).

## Cài đặt & Chạy ứng dụng (Từ mã nguồn)

Cách dễ nhất và được khuyến nghị để chạy ứng dụng là sử dụng các script tự động hóa được cung cấp:

### Sử dụng Script (Khuyến nghị)

1.  **Tải mã nguồn:**
    *   Sao chép (clone) repository này hoặc tải về dưới dạng tệp ZIP và giải nén.

2.  **Chạy script cài đặt và khởi động:**
    *   **Trên Windows:**
        1.  Điều hướng đến thư mục `windows` trong thư mục gốc của dự án.
        2.  Nhấp đúp vào `run.bat`.
    *   **Trên Linux/macOS:**
        1.  Mở Terminal.
        2.  Điều hướng đến thư mục `linux-mac` trong thư mục gốc của dự án.
        3.  Cấp quyền thực thi cho script: `chmod +x run.sh`
        4.  Chạy script: `./run.sh`

    Các script này sẽ tự động:
    *   Kiểm tra và tạo một môi trường ảo Python tên là `moitruongao` trong thư mục gốc của dự án (nếu nó chưa tồn tại).
    *   Kích hoạt môi trường ảo.
    *   Cài đặt tất cả các thư viện cần thiết từ `requirements.txt`.
    *   Khởi chạy ứng dụng Doc_Project_Tool.

### Cài đặt Thủ công (Tùy chọn nâng cao)

1.  **Tải mã nguồn** (như trên).
2.  Mở Terminal hoặc Command Prompt và điều hướng đến thư mục gốc của dự án.
3.  **(Khuyến nghị)** Tạo và kích hoạt một môi trường ảo Python:
    ```bash
    python -m venv moitruongao
    ```
    *   Trên Windows: `moitruongao\Scripts\activate`
    *   Trên Linux/macOS: `source moitruongao/bin/activate`
4.  Cài đặt các thư viện cần thiết:
    ```bash
    pip install -r requirements.txt
    ```
5.  Chạy ứng dụng:
    ```bash
    python run_app.py
    ```

## Hướng dẫn sử dụng

Sau khi ứng dụng đã khởi chạy:

### Thiết lập Chung

*   **Chọn Ngôn ngữ:** Sử dụng menu thả xuống ở phía bên phải của thanh tiêu đề để thay đổi ngôn ngữ của ứng dụng.
*   **Thao tác Cửa sổ:** Cửa sổ có thể được di chuyển bằng cách kéo thanh tiêu đề, thay đổi kích thước bằng cách kéo các cạnh/góc của nó, và điều khiển bằng các nút thu nhỏ, phóng to/khôi phục, và đóng trên thanh tiêu đề.

### Tab Cấu hình (`Config Tab`)

Đây là tab chính để thiết lập tác vụ tạo tài liệu của bạn.

*   **Thư mục dự án:**
    *   **Vùng danh sách:** Hiển thị các thư mục dự án bạn đã thêm.
    *   **Nút "Thêm thư mục":** Mở hộp thoại để chọn một thư mục dự án cần đưa vào.
    *   **Nút "Xóa thư mục đã chọn":** Xóa thư mục/các thư mục hiện đang được chọn khỏi danh sách.
*   **Thiết lập đầu ra:**
    *   **Trường "Thư mục đầu ra:":** Hiển thị đường dẫn nơi tài liệu được tạo sẽ được lưu.
    *   **Nút "Duyệt...":** Mở hộp thoại để chọn thư mục đầu ra.
    *   **Trường "Tên tệp cơ sở:":** Nhập tên cơ sở mong muốn cho tệp đầu ra của bạn (ví dụ: `project_docs`). Phần mở rộng (`.txt` hoặc `.md`) sẽ được thêm tự động. Nếu một tệp cùng tên đã tồn tại, một số sẽ được nối vào (ví dụ: `project_docs 1.txt`).
    *   **Tùy chọn "Định dạng:":**
        *   **Văn bản (.txt):** Tạo tài liệu văn bản thuần túy.
        *   **Markdown (.md):** Tạo tài liệu Markdown.
    *   **Hộp kiểm "Chi tiết (verbose)":** Nếu được chọn, bản tóm tắt trong tab "Kết quả" sẽ bao gồm số lượng tệp và thư mục đã xử lý.
*   **Nút "Tạo Tài Liệu":** Nhấp vào nút này để bắt đầu quá trình tạo tài liệu. Nút này chỉ được kích hoạt nếu có ít nhất một thư mục dự án được thêm vào.

### Tab Nâng cao

Tùy chỉnh các quy tắc loại trừ tại đây.

*   **Trường "Thư mục con loại trừ (cách nhau bởi dấu phẩy)":** Nhập danh sách các tên thư mục con được phân tách bằng dấu phẩy sẽ bị bỏ qua trong quá trình quét (ví dụ: `__pycache__, .venv, node_modules`).
*   **Trường "Tệp loại trừ (đuôi tệp hoặc tên tệp, cách nhau bởi dấu phẩy)":** Nhập danh sách các phần mở rộng tệp (ví dụ: `.log, .tmp`) hoặc tên tệp đầy đủ (ví dụ: `config.backup.json`) được phân tách bằng dấu phẩy để loại trừ.

### Tab Lịch sử

Quản lý và tái sử dụng các cấu hình trước đây.

*   **Danh sách Lịch sử:** Hiển thị danh sách các lần tạo tài liệu thành công trước đó, được xác định bằng tên dự án và dấu thời gian.
*   **Nút "Tải Cấu Hình":** Tải tất cả cài đặt (đường dẫn dự án, cài đặt đầu ra, loại trừ) từ mục lịch sử đã chọn trở lại các tab "Cấu hình" và "Nâng cao". Bạn cũng có thể nhấp đúp vào một mục để tải.
*   **Nút "Xóa Mục":** Xóa (các) mục lịch sử đã chọn. Sẽ có yêu cầu xác nhận.
*   **Nút "Xóa Tất Cả":** Xóa tất cả các mục khỏi lịch sử. Sẽ có yêu cầu xác nhận.

### Tab Kết quả

Xem kết quả và truy cập các tệp đã tạo.

*   **Vùng Văn bản:** Hiển thị bản tóm tắt của quá trình tạo tài liệu gần đây nhất. Bao gồm:
    *   Thời gian thực thi.
    *   Đường dẫn đến (các) tài liệu được tạo.
    *   Số lượng tệp và thư mục đã xử lý (nếu "Chi tiết (verbose)" được bật).
    *   Danh sách các thư mục và tệp bị bỏ qua.
    *   Bất kỳ lỗi nào gặp phải trong quá trình.
*   **Nút "Sao chép Kết quả":** Sao chép toàn bộ nội dung của vùng văn bản tóm tắt vào clipboard.
*   **Nút "Xóa Kết quả":** Xóa vùng văn bản tóm tắt.
*   **Nút "🚀 Mở AI Studio (và sao chép đường dẫn tệp)":**
    1.  Mở trang web AI Studio trong trình duyệt web mặc định của bạn.
    2.  Sao chép đường dẫn đầy đủ của *tệp tài liệu chính được tạo* từ lần chạy cuối cùng vào clipboard của bạn. Sau đó, bạn có thể dễ dàng tham chiếu đường dẫn này hoặc sử dụng nó để định vị và tải tệp lên LLM.
    *   *Lưu ý: Nút này chỉ được kích hoạt nếu một tài liệu đã được tạo thành công trong lần chạy cuối cùng và tệp đó vẫn tồn tại.*
*   **Nút "Mở Thư mục Đầu ra":** Mở thư mục đầu ra đã cấu hình (từ tab "Cấu hình") trong trình εξερεύνηση tệp của hệ thống.

### Thanh Trạng thái

Nằm ở cuối cửa sổ:

*   **Nhãn Trạng thái:** Hiển thị các thông báo về trạng thái hiện tại của ứng dụng (ví dụ: "Sẵn sàng", "Đang xử lý...", "Hoàn tất! Tài liệu tại: ...", "Lỗi").
*   **Thanh Tiến trình:** Hiển thị tiến trình của quá trình tạo tài liệu. Nó sẽ không xác định (có hiệu ứng động) trong quá trình xử lý và sẽ đầy khi hoàn thành.

## Cấu trúc thư mục dự án

```
Doc_Project_Tool/
├── .git/                     # Dữ liệu kho Git (Thường không bao gồm trong bản phân phối)
├── assets/
│   └── icon.ico              # Biểu tượng ứng dụng
├── Core/                     # Logic cốt lõi và các thành phần UI của ứng dụng
│   ├── __pycache__/          # Tệp cache Python (Thường không bao gồm)
│   ├── app_logic.py          # Logic tạo tài liệu chính
│   ├── base_main_window.py   # Lớp cơ sở cho cửa sổ chính (không khung, thanh tiêu đề tùy chỉnh)
│   ├── constants.py          # Các hằng số toàn ứng dụng
│   ├── custom_title_bar.py   # Widget thanh tiêu đề tùy chỉnh
│   ├── doc_tool_config.json  # Lưu trữ tùy chọn người dùng (ngôn ngữ, trạng thái cửa sổ)
│   ├── doc_tool_history.json # Lưu trữ lịch sử chạy
│   ├── gui_components.py     # Chứa một widget CustomScrolledText sử dụng customtkinter (có thể dùng cho mục đích phụ hoặc thử nghiệm)
│   ├── gui_utils.py          # Các hàm tiện ích cho GUI
│   ├── main_app.py           # Lớp ứng dụng chính (UI và logic PySide6)
│   └── translations.py       # Chuỗi dịch đa ngôn ngữ
├── linux-mac/
│   └── run.sh                # Script cài đặt và chạy cho Linux/macOS
├── moitruongao/              # Môi trường ảo Python (được tạo bởi script chạy, không có trong repo)
├── windows/
│   └── run.bat               # Script cài đặt và chạy cho Windows
├── .gitignore                # Chỉ định các tệp không được theo dõi mà Git nên bỏ qua
├── requirements.txt          # Danh sách các thư viện Python phụ thuộc
└── run_app.py                # Script điểm vào chính để khởi chạy ứng dụng
```

## Công nghệ sử dụng

*   **Python:** Ngôn ngữ lập trình chính.
*   **PySide6:** Gói Python chính thức cho Qt, được sử dụng để xây dựng giao diện người dùng đồ họa.
*   **customtkinter:** Được liệt kê là một thư viện phụ thuộc; một thành phần `CustomScrolledText` sử dụng nó tồn tại trong `Core/gui_components.py`. Tuy nhiên, giao diện người dùng đồ họa chính của ứng dụng được xây dựng bằng PySide6.
*   **markdown:** Được liệt kê là một thư viện phụ thuộc, có khả năng dùng để xử lý Markdown nếu các tính năng cụ thể được thêm vào trong tương lai (đầu ra Markdown hiện tại là ghi văn bản trực tiếp).

</details>

<!-- Japanese -->
<details>
<summary>🇯🇵 日本語 (詳細)</summary>

## 概要

**Doc_Project_Tool**は、ソフトウェアプロジェクトの包括的なドキュメント作成プロセスを効率化するために設計されたデスクトップアプリケーションです。選択されたプロジェクトディレクトリをスキャンし、ファイル構造を概説し、サポートされているソースコードファイルの内容を単一の整理されたドキュメントに連結します。このツールは、大規模言語モデル（LLM）用のプロジェクト概要の準備、コードレビュー、またはアーカイブに特に役立ちます。

PythonとPySide6で構築されており、モダンでユーザーフレンドリー、カスタマイズ可能なインターフェースと多言語サポートを提供します。

## 重要な注意点

*   📜 **設定ファイル:** 優先言語、ウィンドウのサイズや位置などのユーザー固有の設定は、`Core/doc_tool_config.json`に保存されます。
*   💾 **履歴ファイル:** 過去の実行設定（プロジェクトパス、出力設定、除外設定）は`Core/doc_tool_history.json`に保存され、以前の設定を迅速に再読み込みできます。
*   🚀 **自動セットアップ:** `run.bat`（Windows用）および`run.sh`（Linux/macOS用）スクリプトが提供されており、仮想環境（`moitruongao`という名前）の作成と必要な依存関係のインストールを自動化し、スムーズな起動を保証します。

## 主な機能

*   **包括的なドキュメント生成:**
    *   ドキュメントに含める1つまたは複数のプロジェクトディレクトリを選択します。
    *   生成されるドキュメントのカスタム出力ディレクトリとベースファイル名を指定します。
    *   テキスト（`.txt`）またはマークダウン（`.md`）の出力形式を選択します。
    *   オプションの「詳細表示（verbose）」モードで、出力サマリーに詳細な処理統計（ファイル/フォルダ数）を含めます。
*   **高度な除外フィルター:**
    *   特定のサブディレクトリを名前で除外します（例: `__pycache__`, `.git`, `venv`, `node_modules`）。
    *   拡張子（例: `.pyc`, `.log`）またはフルネームでファイルを除外します。
*   **直感的でユーザーフレンドリーなインターフェース（PySide6）:**
    *   簡単なナビゲーションのためのモダンなタブ付きレイアウト: 設定、高度な設定、履歴、出力。
    *   標準のウィンドウコントロール（最小化、最大化、閉じる）と言語選択ドロップダウンを備えたカスタムスタイルのタイトルバー。
    *   ウィンドウのドラッグ、サイズ変更、スムーズな開閉アニメーションを完全にサポート。
    *   セッション間でウィンドウの状態（サイズ、位置、最大化状態）を永続化。
*   **多言語サポート:**
    *   インターフェースは英語、ベトナム語（Tiếng Việt）、日本語（日本語）で利用可能です。
    *   タイトルバーからオンザフライで簡単に言語を切り替えられます。
*   **実行履歴管理:**
    *   成功したドキュメント生成実行の設定を自動的に保存します。
    *   タイムスタンプとプロジェクト名で過去の実行リストを表示します。
    *   シングルクリックまたはダブルクリックで履歴エントリから設定を読み込みます。
    *   個々の履歴エントリを削除するか、履歴全体をクリアします。
*   **出力とステータス管理:**
    *   「出力」タブには、実行時間、処理されたファイル/フォルダの数、スキップされたアイテム、遭遇したエラーなど、ドキュメント生成プロセスの概要が表示されます。
    *   出力サマリーをクリップボードにコピーしたり、表示をクリアしたりするためのボタン。
    *   生成されたドキュメントが含まれるディレクトリにすばやくアクセスするための便利な「出力フォルダを開く」ボタン。
    *   特別な「🚀 AI Studioを開く（ファイルパスをコピー）」ボタン:
        *   AI Studioのウェブサイト（または同様のLLMインターフェース）を開きます。
        *   *主に生成されたドキュメントファイル*のフルパスをクリップボードにコピーします。これにより、AI分析のためにドキュメントを簡単に参照またはアップロードできます。
*   **効率的なバックグラウンド処理:**
    *   コアとなるドキュメント生成ロジック（`tao_tai_lieu_du_an`）は、処理中にUIの応答性を維持するために別のワーカースレッド（DocWorker）で実行されます。
    *   ステータスバーのプログレスバーとステータスメッセージがリアルタイムでフィードバックを提供します。
*   **クロスプラットフォーム互換性:**
    *   Windows、Linux、macOSで実行するように設計されています。
    *   セットアップスクリプト（`run.bat`、`run.sh`）が異なるオペレーティングシステムでのインストールを簡素化します。
*   **明確なフィードバックメカニズム:**
    *   専用のステータスバーがアプリケーションの現在の状態（準備完了、処理中、完了！ドキュメント場所: ...、エラー）を表示します。
    *   確認、エラー、通知のための情報ダイアログボックス。

## 前提条件（ソースから実行する場合）

1.  **Python:** Python 3.xを推奨します。セットアップスクリプトは、システムのPATHで利用可能な`python`または`python3`コマンドを使用しようとします。
2.  **Pip:** Pythonパッケージインストーラー（通常Pythonに付属）。

## インストールと実行（ソースから）

アプリケーションを実行する最も簡単で推奨される方法は、提供されている自動化スクリプトを使用することです。

### スクリプトの使用（推奨）

1.  **ソースコードのダウンロード:**
    *   このリポジトリをクローンするか、ZIPファイルとしてダウンロードして展開します。

2.  **セットアップおよび起動スクリプトの実行:**
    *   **Windowsの場合:**
        1.  プロジェクトのルートフォルダ内の`windows`ディレクトリに移動します。
        2.  `run.bat`をダブルクリックします。
    *   **Linux/macOSの場合:**
        1.  ターミナルを開きます。
        2.  プロジェクトのルートフォルダ内の`linux-mac`ディレクトリに移動します。
        3.  スクリプトに実行権限を付与します: `chmod +x run.sh`
        4.  スクリプトを実行します: `./run.sh`

    これらのスクリプトは自動的に次の処理を行います:
    *   プロジェクトルートに`moitruongao`という名前のPython仮想環境を確認し、存在しない場合は作成します。
    *   仮想環境をアクティブ化します。
    *   `requirements.txt`にリストされているすべての依存関係をインストールします。
    *   Doc_Project_Toolアプリケーションを起動します。

### 手動セットアップ（高度なオプション）

1.  **ソースコードをダウンロードします**（上記参照）。
2.  ターミナルまたはコマンドプロンプトを開き、プロジェクトのルートディレクトリに移動します。
3.  **(推奨)** Python仮想環境を作成してアクティブ化します:
    ```bash
    python -m venv moitruongao
    ```
    *   Windowsの場合: `moitruongao\Scripts\activate`
    *   Linux/macOSの場合: `source moitruongao/bin/activate`
4.  必要な依存関係をインストールします:
    ```bash
    pip install -r requirements.txt
    ```
5.  アプリケーションを実行します:
    ```bash
    python run_app.py
    ```

## ユーザーガイド

アプリケーションの起動後:

### 一般設定

*   **言語選択:** タイトルバーの右側にあるドロップダウンメニューを使用して、アプリケーションの言語を変更します。
*   **ウィンドウ操作:** ウィンドウはタイトルバーをドラッグして移動したり、端や角をドラッグしてサイズ変更したり、タイトルバーの最小化、最大化/元に戻す、閉じるボタンを使用して制御できます。

### 「設定」タブ (`Config Tab`)

これは、ドキュメント作成タスクを設定するためのメインタブです。

*   **プロジェクトディレクトリ:**
    *   **リストエリア:** 追加したプロジェクトディレクトリを表示します。
    *   **「ディレクトリ追加」ボタン:** 含めるプロジェクトフォルダを選択するためのダイアログを開きます。
    *   **「選択項目削除」ボタン:** 現在選択されているディレクトリをリストから削除します。
*   **出力設定:**
    *   **「出力ディレクトリ:」フィールド:** 生成されたドキュメントが保存されるパスを表示します。
    *   **「参照...」ボタン:** 出力ディレクトリを選択するためのダイアログを開きます。
    *   **「ベースファイル名:」フィールド:** 出力ファイルの希望するベース名を入力します（例: `project_docs`）。拡張子（`.txt`または`.md`）は自動的に追加されます。同じ名前のファイルが存在する場合、番号が追加されます（例: `project_docs 1.txt`）。
    *   **「フォーマット:」オプション:**
        *   **テキスト (.txt):** プレーンテキストドキュメントを生成します。
        *   **マークダウン (.md):** マークダウン ドキュメントを生成します。
    *   **「詳細表示（verbose）」チェックボックス:** オンにすると、「出力」タブのサマリーに処理されたファイルとフォルダの数が含まれます。
*   **「ドキュメント生成」ボタン:** このボタンをクリックしてドキュメント生成プロセスを開始します。少なくとも1つのプロジェクトディレクトリが追加されている場合にのみ有効になります。

### 「高度な設定」タブ

ここで除外ルールをカスタマイズします。

*   **「除外サブディレクトリ（カンマ区切り）」フィールド:** スキャン中にスキップするサブディレクトリ名のカンマ区切りリストを入力します（例: `__pycache__, .venv, node_modules`）。
*   **「除外ファイル（拡張子または名前、カンマ区切り）」フィールド:** 除外するファイル拡張子（例: `.log, .tmp`）またはフルファイル名（例: `config.backup.json`）のカンマ区切りリストを入力します。

### 「履歴」タブ

過去の設定を管理および再利用します。

*   **履歴リスト:** プロジェクト名とタイムスタンプで識別される、以前に成功したドキュメント実行のリストを表示します。
*   **「設定読込」ボタン:** 選択した履歴項目からすべての設定（プロジェクトパス、出力設定、除外設定）を「設定」タブと「高度な設定」タブに読み込みます。項目をダブルクリックして読み込むこともできます。
*   **「項目削除」ボタン:** 選択した履歴項目を削除します。確認が必要です。
*   **「すべて削除」ボタン:** 履歴からすべての項目を削除します。確認が必要です。

### 「出力」タブ

結果を表示し、生成されたファイルにアクセスします。

*   **テキストエリア:** 最新のドキュメント生成プロセスの概要を表示します。これには以下が含まれます:
    *   実行時間。
    *   生成されたドキュメントへのパス。
    *   処理されたファイルとフォルダの数（「詳細表示（verbose）」が有効な場合）。
    *   スキップされたフォルダとファイルのリスト。
    *   プロセス中に発生したエラー。
*   **「出力コピー」ボタン:** 概要テキストエリアの全内容をクリップボードにコピーします。
*   **「出力クリア」ボタン:** 概要テキストエリアをクリアします。
*   **「🚀 AI Studioを開く（ファイルパスをコピー）」ボタン:**
    1.  デフォルトのウェブブラウザでAI Studioのウェブサイトを開きます。
    2.  最後の実行で*主に生成されたドキュメントファイル*のフルパスをクリップボードにコピーします。その後、このパスを簡単に参照したり、LLMにファイルをアップロードしたりするために使用できます。
    *   *注意: このボタンは、最後の実行でドキュメントが正常に生成され、そのファイルがまだ存在する場合にのみ有効になります。*
*   **「出力フォルダを開く」ボタン:** （「設定」タブからの）設定された出力ディレクトリをシステムのファイルエクスプローラで開きます。

### ステータスバー

ウィンドウの下部にあります:

*   **ステータスラベル:** アプリケーションの現在の状態に関するメッセージを表示します（例: 「準備完了」、「処理中...」、「完了！ドキュメント場所: ...」、「エラー」）。
*   **プログレスバー:** ドキュメント生成プロセスの進行状況を表示します。処理中は不確定（アニメーション）になり、完了するといっぱいになります。

## プロジェクト構成

```
Doc_Project_Tool/
├── .git/                     # Gitリポジトリデータ（通常、配布物には含まれません）
├── assets/
│   └── icon.ico              # アプリケーションアイコン
├── Core/                     # コアアプリケーションロジックとUIコンポーネント
│   ├── __pycache__/          # Pythonキャッシュファイル（通常、含まれません）
│   ├── app_logic.py          # 主要なドキュメント生成ロジック
│   ├── base_main_window.py   # メインウィンドウの基本クラス（フレームレス、カスタムタイトルバー）
│   ├── constants.py          # アプリケーション全体の定数
│   ├── custom_title_bar.py   # カスタムタイトルバーウィジェット
│   ├── doc_tool_config.json  # ユーザー設定（言語、ウィンドウ状態）を保存
│   ├── doc_tool_history.json # 実行履歴を保存
│   ├── gui_components.py     # customtkinterを使用したCustomScrolledTextウィジェットが含まれています（補助的な使用または実験用である可能性があります）
│   ├── gui_utils.py          # GUI用のユーティリティ関数
│   ├── main_app.py           # メインアプリケーションクラス（PySide6 UIとロジック）
│   └── translations.py       # 多言語翻訳文字列
├── linux-mac/
│   └── run.sh                # Linux/macOS用のセットアップおよび実行スクリプト
├── moitruongao/              # Python仮想環境（実行スクリプトによって作成され、リポジトリにはありません）
├── windows/
│   └── run.bat               # Windows用のセットアップおよび実行スクリプト
├── .gitignore                # Gitが無視する意図的に追跡されていないファイルを指定
├── requirements.txt          # Pythonの依存関係のリスト
└── run_app.py                # アプリケーションを起動するためのメインエントリスクリプト
```

## 使用技術

*   **Python:** 主要なプログラミング言語。
*   **PySide6:** グラフィカルユーザーインターフェースを構築するために使用される、Qtの公式Pythonバインディング。
*   **customtkinter:** 依存関係としてリストされています。`Core/gui_components.py`にそれを使用した`CustomScrolledText`コンポーネントが存在します。ただし、メインアプリケーションのGUIはPySide6で構築されています。
*   **markdown:** 依存関係としてリストされており、将来特定の機能が追加された場合にマークダウン処理に使用される可能性があります（現在のマークダウン出力は直接的なテキスト書き込みです）。

</details>

---
