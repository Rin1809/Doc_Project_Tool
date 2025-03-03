# Doc_Project_Tool - Công cụ Tạo Tài liệu Dự án Tự động

---

## 1. Giới thiệu

**Doc_Project_Tool** là một công cụ Python mạnh mẽ được thiết kế để tự động tạo ra tài liệu dự án một cách nhanh chóng và hiệu quả. Công cụ này quét qua cấu trúc thư mục của dự án, liệt kê các thư mục và tệp, đồng thời trích xuất nội dung của các tệp mã nguồn phổ biến (như Python, JavaScript, Java, HTML, CSS, Shell scripts, v.v.) để đưa vào tài liệu.

**Mục tiêu chính của Doc_Project_Tool là:**

- **Tiết kiệm thời gian:** Tự động hóa quá trình tạo tài liệu, loại bỏ công việc thủ công tốn thời gian.
- **Dễ sử dụng:** Giao diện người dùng đồ họa trực quan (GUI) giúp người dùng không cần có kiến thức lập trình sâu vẫn có thể sử dụng.
- **Linh hoạt:** Hỗ trợ cấu hình các thư mục và tệp loại trừ, định dạng đầu ra (TXT hoặc Markdown), giúp tùy chỉnh tài liệu theo nhu cầu.
- **Tài liệu chi tiết:** Tạo ra tài liệu rõ ràng, dễ đọc, giúp người khác nhanh chóng nắm bắt cấu trúc và nội dung dự án.

**Ai nên sử dụng Doc_Project_Tool?**

- **Lập trình viên:** Muốn nhanh chóng tạo tài liệu cho dự án cá nhân hoặc dự án nhóm để chia sẻ, lưu trữ, hoặc bàn giao.
- **Người quản lý dự án:** Cần tài liệu tổng quan về cấu trúc và các thành phần của dự án để theo dõi và quản lý dự án hiệu quả.
- **Sinh viên/Người học:**  Muốn tạo tài liệu cho các bài tập, đồ án, hoặc dự án học tập một cách chuyên nghiệp.

## 2. Tính năng

**Doc_Project_Tool** cung cấp các tính năng nổi bật sau:

- **Quét nhiều thư mục dự án:**  Hỗ trợ chọn nhiều thư mục dự án cùng lúc, cho phép tạo tài liệu cho các dự án lớn hoặc tổ hợp dự án.
- **Loại trừ thư mục con và tệp:** Cho phép người dùng chỉ định các thư mục con và tệp/phần mở rộng tệp cần loại trừ khỏi quá trình tạo tài liệu, giúp tập trung vào các thành phần quan trọng của dự án.
- **Hỗ trợ định dạng đầu ra TXT và Markdown:**
    - **TXT:** Định dạng văn bản thuần túy, dễ đọc trong mọi trình soạn thảo văn bản.
    - **Markdown (.md):** Định dạng phổ biến cho tài liệu, hỗ trợ định dạng văn bản (tiêu đề, danh sách, code block...), dễ dàng chuyển đổi sang HTML và các định dạng khác. Markdown rất thích hợp để đăng tải tài liệu lên các nền tảng như GitHub, GitLab, v.v.
- **Liệt kê cấu trúc thư mục rõ ràng:** Tài liệu được tạo ra thể hiện cấu trúc thư mục dự án một cách trực quan bằng cách sử dụng ký tự đồ họa ASCII (cho TXT) hoặc định dạng danh sách (cho Markdown), giúp dễ dàng hình dung cấu trúc dự án.
- **Trích xuất và hiển thị nội dung tệp mã nguồn:**  Đối với các tệp có phần mở rộng phổ biến như `.py`, `.js`, `.java`, `.cpp`, `.html`, `.css`, `.bat`, `.sh`, `.txt`, `.env`, công cụ sẽ trích xuất và hiển thị nội dung của chúng trong tài liệu (có syntax highlighting đơn giản bằng cách bao quanh code block bằng ```).
- **Xử lý lỗi và bỏ qua tệp/thư mục:**  Công cụ xử lý các lỗi như "Không tìm thấy tệp/thư mục" hoặc "Lỗi truy cập" một cách mềm dẻo và ghi lại thông tin về các lỗi và các tệp/thư mục bị bỏ qua trong tài liệu đầu ra, giúp người dùng biết được những vấn đề có thể xảy ra.
- **Chế độ Verbose (tùy chọn):** Khi bật chế độ Verbose, tài liệu sẽ hiển thị thêm thông tin chi tiết như số lượng tệp và thư mục đã xử lý.
- **Giao diện người dùng đồ họa (GUI) thân thiện:** Sử dụng thư viện `customtkinter` và `tkinter`, cung cấp giao diện trực quan, dễ sử dụng cho người dùng không chuyên về kỹ thuật.
- **Thông báo hoàn thành và Mở thư mục đầu ra:**  Sau khi tạo tài liệu thành công, công cụ hiển thị thông báo hoàn thành và cung cấp nút để mở nhanh chóng thư mục chứa tài liệu vừa tạo.

## 3. Cấu trúc Dự án

```
Doc_Project_Tool/
├── .git/             (Thư mục Git - không liệt kê khi tạo tài liệu)
├── .gitignore        (File chỉ định các tệp/thư mục Git bỏ qua)
├── Core/             (Thư mục chứa mã nguồn chính của công cụ)
│   ├── Tool.py       (File mã nguồn Python chính của công cụ)
├── moitruongao/     (Thư mục môi trường ảo Python - có thể liệt kê hoặc loại trừ)
├── run.bat           (File batch để chạy ứng dụng trên Windows)
```

- **`.git/`**: Thư mục Git chứa thông tin về lịch sử phiên bản của dự án. (Thường được loại trừ khỏi tài liệu).
- **`.gitignore`**: File văn bản liệt kê các file và thư mục mà Git sẽ bỏ qua, không theo dõi và không commit.
- **`Core/`**: Thư mục chứa mã nguồn Python chính của công cụ.
    - **`Tool.py`**: File Python chứa toàn bộ logic của công cụ, giao diện người dùng, và các chức năng tạo tài liệu.
- **`moitruongao/`**: Thư mục môi trường ảo Python. Thư mục này chứa các thư viện Python riêng biệt cho dự án này, giúp tránh xung đột phiên bản thư viện với các dự án khác. (Có thể được đưa vào tài liệu nếu bạn không loại trừ).
- **`run.bat`**: File batch script (trên Windows) giúp kích hoạt môi trường ảo và chạy file `Tool.py` một cách dễ dàng.

## 4. Cài đặt

### Điều kiện tiên quyết

Trước khi cài đặt và sử dụng **Doc_Project_Tool**, bạn cần đảm bảo rằng hệ thống của bạn đã cài đặt:

1. **Python:** Phiên bản Python 3.8 trở lên. Bạn có thể tải Python từ trang web chính thức: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **pip:** (Thường được cài đặt cùng với Python) Pip là trình quản lý gói cho Python, dùng để cài đặt các thư viện cần thiết cho dự án.

### Các bước cài đặt

1. **Tải Dự án:** Clone hoặc tải xuống mã nguồn của dự án **Doc_Project_Tool** từ GitHub (hoặc nguồn cung cấp khác).

   ```bash
   git clone [URL_repository_GitHub_của_bạn]
   cd Doc_Project_Tool
   ```

2. **Tạo Môi trường Ảo (khuyến khích):**  Sử dụng môi trường ảo giúp quản lý các thư viện Python cho từng dự án một cách độc lập. Trong thư mục dự án **Doc_Project_Tool**, chạy lệnh sau để tạo môi trường ảo có tên `moitruongao`:

   ```bash
   python -m venv moitruongao
   ```

3. **Kích hoạt Môi trường Ảo:**

   - **Trên Windows:** Chạy file `run.bat` trong thư mục dự án. File `run.bat` sẽ tự động kích hoạt môi trường ảo và chạy ứng dụng.

     Hoặc, bạn có thể kích hoạt thủ công bằng lệnh sau trong Command Prompt hoặc PowerShell:
     ```bash
     moitruongao\Scripts\activate.bat
     ```

   - **Trên macOS/Linux:** Chạy lệnh sau trong Terminal:
     ```bash
     source moitruongao/bin/activate
     ```

4. **Cài đặt Thư viện (nếu cần):** **Doc_Project_Tool** sử dụng các thư viện sau: `customtkinter`, `tkinter`, và `ttk`.  Các thư viện này đã được import trong file `Tool.py`, nhưng nếu bạn gặp lỗi thiếu thư viện khi chạy, hãy đảm bảo chúng đã được cài đặt trong môi trường ảo.

   Mở file `run.bat` bạn sẽ thấy dòng: `pip install -r requirements.txt`.  File `requirements.txt` (nếu có trong repository) sẽ liệt kê các thư viện cần thiết.

   Nếu file `requirements.txt` không có, bạn có thể tự cài đặt các thư viện (trong khi môi trường ảo đang được kích hoạt) bằng lệnh `pip install`:
   ```bash
   pip install customtkinter tkinter ttkbootstrap
   ```
   (Lưu ý: `ttkbootstrap` là một theme cho `tkinter`, không bắt buộc. `customtkinter` đã bao gồm nhiều theme đẹp, `ttkbootstrap` có thể không cần thiết.)

5. **Chạy Ứng dụng:**

   - **Trên Windows (khuyến khích):** Chạy file `run.bat`. File này sẽ kích hoạt môi trường ảo (nếu chưa) và sau đó chạy file `Core\Tool.py` để khởi động ứng dụng GUI.

   - **Chạy trực tiếp (mọi hệ điều hành sau khi kích hoạt môi trường ảo):**
     Di chuyển đến thư mục `Core/` và chạy lệnh:
     ```bash
     cd Core
     python Tool.py
     ```

     Hoặc, từ thư mục gốc dự án, chạy:
     ```bash
     python Core/Tool.py
     ```

     Giao diện đồ họa của **Doc_Project_Tool** sẽ hiện lên.

## 5. Cách Sử dụng

### Giao diện Người dùng Đồ họa (GUI)

Khi chạy file `Tool.py` hoặc `run.bat`, bạn sẽ thấy giao diện chính của **Doc_Project_Tool**:

![Giao diện chính Doc_Project_Tool](link_ảnh_giao_dien_chinh.png)

Giao diện được chia thành các phần chính:

1. **Chọn Thư mục Dự án:**  Khu vực này cho phép bạn thêm và quản lý các thư mục dự án mà bạn muốn tạo tài liệu.
    - **Danh sách Thư mục Dự án:** Hiển thị danh sách các thư mục đã được chọn.
    - **Nút "Thêm":**  Mở hộp thoại chọn thư mục để thêm thư mục dự án vào danh sách.
    - **Nút "Xóa":** Xóa thư mục đang được chọn khỏi danh sách.

2. **Cài đặt Loại trừ:** Khu vực này dùng để cấu hình các loại trừ.
    - **Thư mục con loại trừ:** Một text box lớn để bạn nhập danh sách các tên thư mục con cần loại trừ (ví dụ: `__pycache__`, `venv`, `.git`). Mỗi tên thư mục con trên một dòng.
    - **Tệp loại trừ:**  Một text box lớn để nhập danh sách các phần mở rộng tệp hoặc tên tệp cần loại trừ (ví dụ: `.pyc`, `desktop.ini`, `.json`, `*.log`). Mỗi phần mở rộng hoặc tên tệp trên một dòng.
    - **Nút "Thêm mặc định":** Điền sẵn danh sách các thư mục con và tệp loại trừ mặc định (thường dùng).

3. **Cài đặt Đầu ra:**  Khu vực cấu hình thư mục đầu ra và tên file tài liệu.
    - **Thư mục Đầu ra:**
        - **Label "Thư mục đầu ra":** Nhãn cho trường thư mục đầu ra.
        - **Trường nhập đường dẫn:** Hiển thị đường dẫn thư mục đầu ra hiện tại (mặc định là thư mục hiện tại "."). Bạn có thể nhập trực tiếp đường dẫn hoặc sử dụng nút "Chọn...".
        - **Nút "Chọn...":** Mở hộp thoại chọn thư mục để chọn thư mục đầu ra.
    - **Tên tệp:**
        - **Label "Tên tệp":** Nhãn cho trường tên tệp.
        - **Trường nhập tên tệp cơ sở:**  Nhập tên tệp cơ sở (ví dụ: `tai_lieu_du_an`). Tên file cuối cùng sẽ có dạng `[tên_tệp_cơ_sở].txt` hoặc `[tên_tệp_cơ_sở].md`, có thể có thêm số thứ tự nếu file đã tồn tại.

4. **Định dạng Đầu ra:** Lựa chọn định dạng tài liệu đầu ra:
    - **Radio button "txt":**  Chọn định dạng văn bản thuần túy `.txt`.
    - **Radio button "Markdown":** Chọn định dạng Markdown `.md`.

5. **Tùy chọn & Thực thi:**
    - **Checkbox "Verbose":**  Bật chế độ verbose để hiển thị thêm thông tin chi tiết trong tài liệu đầu ra (số tệp, thư mục đã xử lý).
    - **Nút "Tạo Tài Liệu":** Nút chính để bắt đầu quá trình tạo tài liệu dự án. Nhấn nút này sau khi đã cấu hình xong các cài đặt.

6. **Hiển thị Đầu ra:**  Text box lớn ở cuối giao diện để hiển thị các thông báo trong quá trình tạo tài liệu, cũng như các thông báo lỗi, cảnh báo, và thông báo hoàn thành.

### Giải thích các Trường Nhập

- **Thư mục Dự án:** Chọn một hoặc nhiều thư mục gốc của dự án mà bạn muốn tạo tài liệu cấu trúc và nội dung.
- **Thư mục con loại trừ:** Liệt kê các thư mục con (nằm trong các thư mục dự án đã chọn) mà bạn muốn bỏ qua, không đưa vào tài liệu. Ví dụ: `__pycache__`, `node_modules`, `venv`, `.git`. Mỗi thư mục con trên một dòng.
- **Tệp loại trừ:**  Liệt kê các phần mở rộng tệp (ví dụ: `.pyc`, `.log`, `.tmp`) hoặc tên tệp cụ thể mà bạn muốn bỏ qua. Ví dụ: `.log`, `temp.txt`, `*.bak`.  Mỗi loại trừ trên một dòng.
- **Thư mục Đầu ra:**  Chọn thư mục mà bạn muốn lưu file tài liệu được tạo ra. Nếu bạn không chọn, file sẽ được lưu trong thư mục hiện tại của ứng dụng.
- **Tên tệp:**  Đặt tên cho file tài liệu đầu ra (ví dụ: `project_docs`). Tên file thực tế sẽ được thêm phần mở rộng `.txt` hoặc `.md` tùy theo định dạng bạn chọn, và có thể thêm số nếu file trùng tên đã tồn tại.
- **Định dạng:** Chọn giữa `.txt` (văn bản thuần túy) hoặc `.md` (Markdown) cho tài liệu đầu ra.
- **Verbose:**  Nếu đánh dấu vào checkbox "Verbose", tài liệu sẽ bao gồm thêm thông tin về số lượng file và thư mục đã được xử lý.

**Quy trình sử dụng:**

1. **Thêm Thư mục Dự án:** Nhấn nút "Thêm" để chọn một hoặc nhiều thư mục dự án. Các thư mục đã chọn sẽ hiển thị trong danh sách.
2. **Cấu hình Loại trừ (tùy chọn):**  Nhập các thư mục con và tệp cần loại trừ vào các text box tương ứng. Hoặc nhấn "Thêm mặc định" để sử dụng danh sách loại trừ phổ biến.
3. **Chọn Thư mục Đầu ra:** Chọn thư mục bạn muốn lưu tài liệu. Nếu bạn không thay đổi, file sẽ được lưu trong thư mục hiện tại của ứng dụng.
4. **Nhập Tên tệp:** Nhập tên cơ sở cho file tài liệu.
5. **Chọn Định dạng Đầu ra:** Chọn "txt" hoặc "Markdown".
6. **Chọn Verbose (tùy chọn):** Đánh dấu vào checkbox "Verbose" nếu muốn.
7. **Nhấn "Tạo Tài Liệu":**  Nhấn nút này để bắt đầu quá trình tạo tài liệu.
8. **Theo dõi Đầu ra:** Xem text box "Hiển thị Đầu ra" để theo dõi tiến trình, thông báo lỗi, và thông báo hoàn thành.
9. **Kiểm tra Tài liệu:** Sau khi hoàn thành, kiểm tra file tài liệu được tạo ra trong thư mục đầu ra bạn đã chọn. Nhấn nút "Đi tới thư mục" trong hộp thoại hoàn thành để mở thư mục chứa tài liệu.

## 6. Ví dụ Sử dụng

Để giúp bạn dễ dàng hình dung cách sử dụng **Doc_Project_Tool**, chúng ta sẽ xem xét một số ví dụ minh họa cụ thể:

### Ví dụ 1: Tạo tài liệu TXT cơ bản cho một dự án Python nhỏ

**Tình huống:** Bạn có một dự án Python đơn giản tên là `my_python_project` có cấu trúc như sau:

```
my_python_project/
├── main.py
├── utils/
│   ├── helper.py
└── requirements.txt
```

Bạn muốn tạo một tài liệu TXT đơn giản để xem cấu trúc dự án và nội dung các file code Python.

**Các bước thực hiện:**

1. **Khởi động Doc_Project_Tool:** Chạy file `run.bat` (Windows) hoặc `python Core/Tool.py` (macOS/Linux) để mở giao diện ứng dụng.

2. **Thêm Thư mục Dự án:**
   - Nhấn nút **"Thêm"** trong khu vực **"Chọn Thư mục Dự án"**.
   - Chọn thư mục `my_python_project` từ hộp thoại chọn thư mục và nhấn **"Chọn Thư mục"**.
   - Thư mục `my_python_project` sẽ xuất hiện trong danh sách **Thư mục Dự án**.

3. **Cài đặt Loại trừ:**  Để ví dụ đơn giản, chúng ta sẽ **không** loại trừ thư mục con hoặc tệp nào. Để trống các text box **"Thư mục con loại trừ"** và **"Tệp loại trừ"**.

4. **Cài đặt Đầu ra:**
   - **Thư mục Đầu ra:** Để mặc định (thường là thư mục hiện tại của ứng dụng).
   - **Tên tệp:** Nhập `tai_lieu_python_project` vào trường **"Tên tệp"**.

5. **Định dạng Đầu ra:** Chọn radio button **"txt"** để tạo tài liệu định dạng TXT.

6. **Tùy chọn Verbose:** Để ví dụ này đơn giản, **không đánh dấu** vào checkbox **"Verbose"**.

7. **Thực thi:** Nhấn nút **"Tạo Tài Liệu"**.

8. **Xem kết quả:** Sau khi quá trình tạo tài liệu hoàn tất (thông báo "Hoàn thành" hiện ra), mở thư mục đầu ra bạn đã chọn. Bạn sẽ thấy file `tai_lieu_python_project.txt`.

**Nội dung file `tai_lieu_python_project.txt` (ví dụ):**

```txt
Dự án: my_python_project - ...

my_python_project/
├── main.py
└── utils/
    └── helper.py


my_python_project/
**main.py**
```python
def main():
    print("Xin chào từ my_python_project!")
    # Gọi hàm helper từ module utils
    from utils import helper
    helper.say_hello("Người dùng")

if __name__ == "__main__":
    main()
```

```
**utils\helper.py**
```python
def say_hello(name):
    print(f"Xin chào, {name} từ module helper!")
```
```

**Giải thích:**

- Tài liệu TXT đã được tạo thành công trong thư mục đầu ra.
- Cấu trúc thư mục `my_python_project` được liệt kê rõ ràng.
- Nội dung của các file Python (`main.py`, `utils\helper.py`) đã được trích xuất và hiển thị bên dưới, được bao quanh bởi ``` để đánh dấu code block.

---

### Ví dụ 2: Tạo tài liệu Markdown cho dự án Web và loại trừ thư mục môi trường ảo

**Tình huống:** Bạn có một dự án web front-end sử dụng HTML, CSS, JavaScript và có thư mục môi trường ảo `venv` mà bạn muốn loại trừ khỏi tài liệu. Cấu trúc dự án có thể như sau:

```
my_web_project/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
│   └── logo.png   (Chúng ta sẽ loại trừ file ảnh này)
└── venv/          (Thư mục môi trường ảo cần loại trừ)
```

Bạn muốn tạo tài liệu Markdown, loại trừ thư mục `venv` và file ảnh `logo.png`.

**Các bước thực hiện:**

1. **Khởi động Doc_Project_Tool.**

2. **Thêm Thư mục Dự án:** Thêm thư mục `my_web_project` vào danh sách dự án như trong Ví dụ 1.

3. **Cài đặt Loại trừ:**
   - **Thư mục con loại trừ:** Trong text box **"Thư mục con loại trừ"**, nhập `venv`.
   - **Tệp loại trừ:** Trong text box **"Tệp loại trừ"**, nhập `logo.png`.

4. **Cài đặt Đầu ra:**
   - **Thư mục Đầu ra:** Chọn thư mục mong muốn, ví dụ: thư mục Desktop.
   - **Tên tệp:** Nhập `tai_lieu_web_project` vào trường **"Tên tệp"**.

5. **Định dạng Đầu ra:** Chọn radio button **"Markdown"** để tạo tài liệu định dạng Markdown.

6. **Tùy chọn Verbose:** **Có thể đánh dấu** vào checkbox **"Verbose"** nếu bạn muốn xem thông tin chi tiết về quá trình xử lý.

7. **Thực thi:** Nhấn nút **"Tạo Tài Liệu"**.

8. **Xem kết quả:** Sau khi hoàn tất, mở thư mục Desktop (hoặc thư mục đầu ra đã chọn). Bạn sẽ thấy file `tai_lieu_web_project.md`.

**Một phần nội dung file `tai_lieu_web_project.md` (ví dụ):**

```markdown
# Dự án: my_web_project - ...

my_web_project/
- css/
    - styles.css
- img/
    - logo.png (Không liệt kê)
- js/
    - script.js
- venv/ (Không liệt kê)
- index.html


### [Xử lý file]
✅ my_web_project/index.html

- 📁 Thư mục đã quét: 2
- 📄 Tệp đã quét: 3
- 📂 Thư mục bỏ qua:
    - venv
- 📄 Tệp bỏ qua:
    - img\logo.png

**index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Trang Web của Tôi</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>Chào mừng đến với Trang Web của Tôi!</h1>
    <img src="img/logo.png" alt="Logo">
    <script src="js/script.js"></script>
</body>
</html>
```

**css\styles.css**

```css
body {
    font-family: sans-serif;
}
h1 {
    color: blue;
}
```

**js\script.js**

```javascript
console.log("Trang web đã được tải!");
```

**Giải thích:**

- Tài liệu Markdown đã được tạo thành công.
- Cấu trúc thư mục hiển thị dưới dạng danh sách Markdown.
- Thư mục `venv/` và file `img/logo.png` đã được loại trừ và được ghi rõ trong phần "Thư mục bỏ qua" và "Tệp bỏ qua" ở cuối tài liệu.
- Nội dung của các file HTML, CSS, JavaScript đã được trích xuất và hiển thị trong Markdown code blocks (```markdown).

---

### Khám phá thêm

Thử nghiệm với các cài đặt khác nhau như bật chế độ **"Verbose"**, thêm nhiều thư mục dự án, và tùy chỉnh danh sách loại trừ để khám phá toàn bộ khả năng của **Doc_Project_Tool**.

Chúc bạn tạo tài liệu dự án thành công!

## 7. Cấu hình Nâng cao

### File loại trừ mặc định

**Doc_Project_Tool** đã cài đặt sẵn một số thư mục con và phần mở rộng tệp loại trừ mặc định, được coi là phổ biến và thường không cần thiết trong tài liệu dự án, ví dụ:

**Thư mục con loại trừ mặc định:**
```
__pycache__
moitruongao
venv
.git
.vscode
bieutuong
memory
node_modules
uploads
chats
```

**Tệp loại trừ mặc định:**
```
.pyc
desktop.ini
.json
.txt
.rar
requirements.txt
ex.json
.jpg
.mp3
```

Bạn có thể tùy chỉnh danh sách này bằng cách chỉnh sửa trực tiếp trong các text box "Thư mục con loại trừ" và "Tệp loại trừ" trong giao diện GUI.  Nút "Thêm mặc định" sẽ giúp bạn nhanh chóng khôi phục lại danh sách loại trừ mặc định nếu bạn muốn.

### Định dạng Đầu ra

**Doc_Project_Tool** hỗ trợ hai định dạng đầu ra chính: **TXT** và **Markdown**.

- **TXT (.txt):** Tạo file văn bản thuần túy, dễ đọc bằng bất kỳ trình soạn thảo văn bản nào. Cấu trúc thư mục được biểu diễn bằng ký tự ASCII. Nội dung file code được bao quanh bởi ``` để đánh dấu code block (nhưng không có syntax highlighting). Phù hợp để đọc nhanh hoặc in ra.

- **Markdown (.md):** Tạo file Markdown, một định dạng rất phổ biến cho tài liệu kỹ thuật. Markdown cho phép định dạng văn bản phong phú hơn (tiêu đề, danh sách, code block, ...) và dễ dàng chuyển đổi sang HTML. Cấu trúc thư mục được biểu diễn bằng danh sách Markdown. Nội dung file code được bao quanh bởi ```markdown để tạo code block Markdown. Định dạng Markdown rất thích hợp để xem trực tuyến trên GitHub, GitLab, hoặc sử dụng với các công cụ tạo tài liệu tĩnh (static site generators).

Bạn có thể chọn định dạng đầu ra phù hợp với nhu cầu sử dụng của mình trước khi tạo tài liệu.
