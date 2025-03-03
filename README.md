# Doc_Project_Tool - Công cụ Tạo Tài liệu Dự án Tự động

## Interface
![image](https://github.com/user-attachments/assets/5ffbc36e-e9ed-4ed2-95c3-0aeaf7004421)

## Ouput
![image](https://github.com/user-attachments/assets/8d6b78e5-fdd1-4799-b298-067d09674266)

## Introduction
<details>
<summary>🇻🇳 Tiếng Việt</summary>

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
   git clone https://github.com/Rin1809/Doc_Project_Tool/
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
- **Tên tệp:**  Đặt tên cho file tài liệu đầu ra (ví dụ: `project_docs`). Tên file cuối cùng sẽ được thêm phần mở rộng `.txt` hoặc `.md` tùy theo định dạng bạn chọn, và có thể thêm số nếu file trùng tên đã tồn tại.
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
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
└── venv/          (Không liệt kê)


### [Xử lý file]
✅ my_web_project/index.html

- 📁 Thư mục đã quét: 2
- 📄 Tệp đã quét: 3
- 📂 Thư mục bỏ qua:
    └──venv
- 📄 Tệp bỏ qua:
    └── img\logo.png

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


**css\styles.css**

```css
body {
    font-family: sans-serif;
}
h1 {
    color: blue;
}


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

</details>

<details>
<summary>🇬🇧 English</summary>

## 1. Introduction

**Doc_Project_Tool** is a powerful Python tool designed to automatically generate project documentation quickly and efficiently. It scans through the project's directory structure, lists directories and files, and extracts the content of common source code files (such as Python, JavaScript, Java, HTML, CSS, Shell scripts, etc.) for inclusion in the documentation.

**The main goals of Doc_Project_Tool are:**

- **Save Time:** Automate the documentation process, eliminating time-consuming manual work.
- **Easy to Use:** An intuitive Graphical User Interface (GUI) makes it accessible to users without deep programming knowledge.
- **Flexible:** Supports configuration of excluded directories and files, and output formats (TXT or Markdown), allowing customization to meet specific needs.
- **Detailed Documentation:** Generates clear, easy-to-read documentation, helping others quickly understand project structure and content.

**Who should use Doc_Project_Tool?**

- **Programmers:** Who want to quickly create documentation for personal or team projects for sharing, archiving, or handover.
- **Project Managers:** Who need an overview of project structure and components for effective project tracking and management.
- **Students/Learners:** Who want to create professional-looking documentation for assignments, projects, or learning exercises.

## 2. Features

**Doc_Project_Tool** offers the following key features:

- **Scan Multiple Project Directories:** Supports selecting multiple project directories at once, allowing documentation generation for large or combined projects.
- **Exclude Subdirectories and Files:** Allows users to specify subdirectories and file extensions/names to exclude from documentation generation, focusing on essential project components.
- **TXT and Markdown Output Formats Supported:**
    - **TXT:** Plain text format, easily readable in any text editor.
    - **Markdown (.md):** Popular documentation format, supports text formatting (headings, lists, code blocks...), and easily convertible to HTML and other formats. Markdown is well-suited for online documentation platforms like GitHub, GitLab, etc.
- **Clear Directory Structure Listing:** Generated documentation visually represents the project's directory structure using ASCII art characters (for TXT) or list formatting (for Markdown), providing an easy-to-grasp project overview.
- **Source Code File Content Extraction and Display:** For files with common extensions like `.py`, `.js`, `.java`, `.cpp`, `.html`, `.css`, `.bat`, `.sh`, `.txt`, `.env`, the tool extracts and displays their content in the documentation (with basic syntax highlighting by enclosing code blocks in ```).
- **Error Handling and File/Directory Skipping:** The tool gracefully handles errors like "File/directory not found" or "Permission denied," and records information about errors and skipped files/directories in the output documentation, informing users of potential issues.
- **Verbose Mode (Optional):** When Verbose mode is enabled, the documentation includes detailed information such as the number of files and directories processed.
- **User-Friendly Graphical User Interface (GUI):** Uses `customtkinter` and `tkinter` libraries to provide an intuitive, easy-to-use interface for non-technical users.
- **Completion Notification and Output Directory Opening:** Upon successful documentation generation, the tool displays a completion message and provides a button to quickly open the directory containing the generated documentation.

## 3. Project Structure

```
Doc_Project_Tool/
├── .git/             (Git Directory - not listed in documentation)
├── .gitignore        (File specifying files/directories Git should ignore)
├── Core/             (Directory containing the core source code of the tool)
│   ├── Tool.py       (Main Python source code file of the tool)
├── moitruongao/     (Python virtual environment directory - can be listed or excluded)
├── run.bat           (Batch file to run the application on Windows)
```

- **`.git/`**: Git directory containing version history. (Usually excluded from documentation).
- **`.gitignore`**: Text file listing files and directories Git should ignore from tracking and committing.
- **`Core/`**: Directory containing the main Python source code of the tool.
    - **`Tool.py`**: Python file containing the tool's entire logic, user interface, and documentation generation functionalities.
- **`moitruongao/`**: Python virtual environment directory. This directory contains isolated Python libraries for this project, avoiding version conflicts with other projects. (Can be included in documentation if not excluded).
- **`run.bat`**: Batch script (on Windows) to easily activate the virtual environment and run `Tool.py`.

## 4. Installation

### Prerequisites

Before installing and using **Doc_Project_Tool**, ensure your system has the following installed:

1. **Python:** Python version 3.8 or later. You can download Python from the official website: [https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **pip:** (Usually installed with Python) Pip is a package manager for Python, used to install necessary libraries for the project.

### Installation Steps

1. **Download Project:** Clone or download the source code of the **Doc_Project_Tool** project from GitHub (or other source).

   ```bash
   git clone https://github.com/Rin1809/Doc_Project_Tool/
   cd Doc_Project_Tool
   ```

2. **Create Virtual Environment (Recommended):** Using a virtual environment helps manage Python libraries for each project independently. In the **Doc_Project_Tool** project directory, run the following command to create a virtual environment named `moitruongao`:

   ```bash
   python -m venv moitruongao
   ```

3. **Activate Virtual Environment:**

   - **On Windows:** Run the `run.bat` file in the project directory. `run.bat` will automatically activate the virtual environment and run the application.

     Alternatively, you can manually activate it using the following command in Command Prompt or PowerShell:
     ```bash
     moitruongao\Scripts\activate.bat
     ```

   - **On macOS/Linux:** Run the following command in the Terminal:
     ```bash
     source moitruongao/bin/activate
     ```

4. **Install Libraries (If Necessary):** **Doc_Project_Tool** uses the following libraries: `customtkinter`, `tkinter`, and `ttk`. These libraries are imported in `Tool.py`, but if you encounter library missing errors, ensure they are installed in the virtual environment.

   Open `run.bat`, and you'll find the line: `pip install -r requirements.txt`. The `requirements.txt` file (if available in the repository) lists the necessary libraries.

   If `requirements.txt` is not present, you can install the libraries manually (while the virtual environment is activated) using the `pip install` command:
   ```bash
   pip install customtkinter tkinter ttkbootstrap
   ```
   (Note: `ttkbootstrap` is a theme for `tkinter`, optional. `customtkinter` already includes beautiful themes; `ttkbootstrap` may not be necessary.)

5. **Run Application:**

   - **On Windows (Recommended):** Run the `run.bat` file. This file will activate the virtual environment (if not already active) and then run `Core\Tool.py` to start the GUI application.

   - **Run Directly (Any OS after activating virtual environment):**
     Navigate to the `Core/` directory and run the command:
     ```bash
     cd Core
     python Tool.py
     ```

     Or, from the project root directory, run:
     ```bash
     python Core/Tool.py
     ```

     The graphical interface of **Doc_Project_Tool** will appear.

## 5. How to Use

### Graphical User Interface (GUI)

When you run `Tool.py` or `run.bat`, you will see the main interface of **Doc_Project_Tool**:

The interface is divided into main sections:

1. **Select Project Directory:** This area allows you to add and manage the project directories for which you want to generate documentation.
    - **Project Directories List:** Displays the list of selected project directories.
    - **"Add" Button:** Opens a directory selection dialog to add a project directory to the list.
    - **"Remove" Button:** Removes the currently selected directory from the list.

2. **Exclusion Settings:** This area is used to configure exclusions.
    - **Excluded Subdirectories:** A large textbox where you can enter a list of subdirectory names to exclude (e.g., `__pycache__`, `venv`, `.git`). Each subdirectory name on a new line.
    - **Excluded Files:** A large textbox to enter a list of file extensions or filenames to exclude (e.g., `.pyc`, `desktop.ini`, `.json`, `*.log`). Each extension or filename on a new line.
    - **"Add Defaults" Button:** Fills in a pre-defined list of commonly used excluded subdirectories and files.

3. **Output Settings:** Area for configuring the output directory and documentation filename.
    - **Output Directory:**
        - **"Output Directory" Label:** Label for the output directory field.
        - **Path Entry Field:** Displays the current output directory path (default is the current directory "."). You can directly enter a path or use the "Browse..." button.
        - **"Browse..." Button:** Opens a directory selection dialog to choose the output directory.
    - **Filename:**
        - **"Filename" Label:** Label for the filename field.
        - **Base Filename Entry Field:** Enter the base filename (e.g., `project_documentation`). The final filename will be `[base_filename].txt` or `[base_filename].md`, potentially with a numeric suffix if a file with the same name already exists.

4. **Output Format:** Select the output documentation format:
    - **"txt" Radio Button:** Selects plain text `.txt` format.
    - **"Markdown" Radio Button:** Selects Markdown `.md` format.

5. **Options & Execution:**
    - **"Verbose" Checkbox:** Enables verbose mode to include more detailed information in the output documentation (number of files, directories processed).
    - **"Generate Documentation" Button:** The main button to start the project documentation generation process. Click this button after configuring all settings.

6. **Output Display:** A large textbox at the bottom of the interface to display messages during documentation generation, including error messages, warnings, and completion notifications.

### Input Field Explanations

- **Project Directories:** Select one or more root directories of the projects for which you want to document structure and content.
- **Excluded Subdirectories:** List subdirectory names (within the selected project directories) that you want to skip and not include in the documentation. Example: `__pycache__`, `node_modules`, `venv`, `.git`. Each subdirectory name on a new line.
- **Excluded Files:** List file extensions (e.g., `.pyc`, `.log`, `.tmp`) or specific filenames you want to skip. Example: `.log`, `temp.txt`, `*.bak`. Each exclusion on a new line.
- **Output Directory:** Choose the directory where you want to save the generated documentation file. If you don't choose, the file will be saved in the application's current directory.
- **Filename:** Set a name for the output documentation file (e.g., `project_docs`). The actual filename will have the extension `.txt` or `.md` depending on the format you choose, and may have a number appended if a filename already exists.
- **Format:** Choose between `.txt` (plain text) or `.md` (Markdown) for the output documentation.
- **Verbose:** If you check the "Verbose" checkbox, the documentation will include extra information about the number of files and directories processed.

**Usage Procedure:**

1. **Add Project Directories:** Click the "Add" button to select one or more project directories. Selected directories will appear in the list.
2. **Configure Exclusions (Optional):** Enter subdirectories and files to exclude in the corresponding text boxes. Or click "Add Defaults" to use the common exclusion list.
3. **Choose Output Directory:** Select the directory where you want to save the documentation. If you don't change it, the file will be saved in the application's current directory.
4. **Enter Filename:** Enter a base name for the documentation file.
5. **Choose Output Format:** Select "txt" or "Markdown".
6. **Select Verbose (Optional):** Check the "Verbose" checkbox if desired.
7. **Click "Generate Documentation":** Click this button to start the documentation generation process.
8. **Monitor Output:** Watch the "Output Display" textbox to monitor progress, error messages, and completion notifications.
9. **Check Documentation:** After completion, check the documentation file generated in the output directory you selected. Click "Go to Folder" in the completion dialog to open the directory containing the documentation.

## 6. Usage Examples

To help you visualize how to use **Doc_Project_Tool**, let's look at some specific usage examples:

### Example 1: Generate Basic TXT Documentation for a Small Python Project

**Scenario:** You have a simple Python project named `my_python_project` with the following structure:

```
my_python_project/
├── main.py
├── utils/
│   ├── helper.py
└── requirements.txt
```

You want to generate basic TXT documentation to view the project structure and the content of the Python code files.

**Steps to Follow:**

1. **Launch Doc_Project_Tool:** Run `run.bat` (Windows) or `python Core/Tool.py` (macOS/Linux) to open the application interface.

2. **Add Project Directory:**
   - Click the **"Add"** button in the **"Select Project Directory"** area.
   - Select the `my_python_project` directory from the directory selection dialog and click **"Select Folder"**.
   - The `my_python_project` directory will appear in the **Project Directories** list.

3. **Exclusion Settings:** For this simple example, we will **not** exclude any subdirectories or files. Leave the **"Excluded Subdirectories"** and **"Excluded Files"** textboxes empty.

4. **Output Settings:**
   - **Output Directory:** Leave it as default (usually the application's current directory).
   - **Filename:** Enter `python_project_docs` in the **"Filename"** field.

5. **Output Format:** Select the **"txt"** radio button to generate TXT format documentation.

6. **Verbose Option:** For this simple example, **do not check** the **"Verbose"** checkbox.

7. **Execute:** Click the **"Generate Documentation"** button.

8. **View Results:** After the documentation generation is complete (the "Completion" message appears), open the output directory you selected. You will see the file `python_project_docs.txt`.

**Content of `python_project_docs.txt` (Example):**

```txt
Project: my_python_project - ...

my_python_project/
├── main.py
└── utils/
    └── helper.py


my_python_project/
**main.py**
```python
def main():
    print("Hello from my_python_project!")
    # Call helper function from utils module
    from utils import helper
    helper.say_hello("User")

if __name__ == "__main__":
    main()
```

```
**utils\helper.py**
```python
def say_hello(name):
    print(f"Hello, {name} from helper module!")
```


**Explanation:**

- The TXT documentation file was successfully created in the output directory.
- The `my_python_project` directory structure is listed clearly.
- The content of Python files (`main.py`, `utils\helper.py`) has been extracted and displayed below, enclosed in ``` to mark code blocks.

---

### Example 2: Generate Markdown Documentation for a Web Project and Exclude a Virtual Environment Directory

**Scenario:** You have a front-end web project using HTML, CSS, JavaScript, and a virtual environment directory `venv` that you want to exclude from documentation. The project structure might be:

```
my_web_project/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
│   └── logo.png   (We will exclude this image file)
└── venv/          (Virtual environment directory to exclude)
```

You want to generate Markdown documentation, exclude the `venv` directory, and exclude the image file `logo.png`.

**Steps to Follow:**

1. **Launch Doc_Project_Tool.**

2. **Add Project Directory:** Add the `my_web_project` directory to the project list as in Example 1.

3. **Exclusion Settings:**
   - **Excluded Subdirectories:** In the **"Excluded Subdirectories"** textbox, enter `venv`.
   - **Excluded Files:** In the **"Excluded Files"** textbox, enter `logo.png`.

4. **Output Settings:**
   - **Output Directory:** Choose the desired directory, e.g., the Desktop.
   - **Filename:** Enter `web_project_docs` in the **"Filename"** field.

5. **Output Format:** Select the **"Markdown"** radio button to generate Markdown format documentation.

6. **Verbose Option:** **You can check** the **"Verbose"** checkbox if you want to see detailed processing information.

7. **Execute:** Click the **"Generate Documentation"** button.

8. **View Results:** After completion, open the Desktop (or the output directory you chose). You will see the file `web_project_docs.md`.

**Partial Content of `web_project_docs.md` (Example):**

```markdown
# Project: my_web_project - ...

my_web_project/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
└── venv/          (Not listed)


### [File processing]
✅ my_web_project/index.html

- 📁 Directories scanned: 2
- 📄 Files scanned: 3
- 📂 Directories skipped:
    └──venv
- 📄 Files skipped:
    └── img\logo.png

**index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>My Web Page</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>Welcome to My Web Page!</h1>
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
console.log("Web page loaded!");
```

**Explanation:**

- The Markdown documentation file was successfully created.
- The directory structure is shown as a Markdown list.
- The `venv/` directory and `img/logo.png` file have been excluded and are noted in the "Directories skipped" and "Files skipped" sections at the end of the documentation.
- The content of HTML, CSS, and JavaScript files has been extracted and displayed within Markdown code blocks (```markdown).

---

### Explore More

Experiment with different settings, such as enabling **"Verbose"** mode, adding multiple project directories, and customizing exclusion lists to explore the full capabilities of **Doc_Project_Tool**.

Happy project documenting!

## 7. Advanced Configuration

### Default Exclusion Files

**Doc_Project_Tool** comes pre-configured with some default excluded subdirectories and file extensions, considered common and often unnecessary in project documentation, for example:

**Default Excluded Subdirectories:**
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

**Default Excluded Files:**
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

You can customize this list by directly editing the "Excluded Subdirectories" and "Excluded Files" text boxes in the GUI. The "Add Defaults" button helps you quickly restore the default exclusion list if needed.

### Output Formats

**Doc_Project_Tool** supports two main output formats: **TXT** and **Markdown**.

- **TXT (.txt):** Creates a plain text file, easily readable in any text editor. Directory structure is represented with ASCII art characters. Code file content is enclosed in ``` to mark code blocks (but with no syntax highlighting). Suitable for quick reading or printing.

- **Markdown (.md):** Creates a Markdown file, a very popular format for technical documentation. Markdown allows for richer text formatting (headings, lists, code blocks, ...) and is easily convertible to HTML. Directory structure is represented with Markdown lists. Code file content is enclosed in ```markdown to create Markdown code blocks. The Markdown format is highly suitable for viewing online on platforms like GitHub, GitLab, or using with static site generators.

You can choose the output format that best suits your usage needs before generating the documentation.

</details>

<details>
<summary>🇯🇵 日本語</summary>

## 1. はじめに

**Doc_Project_Tool** は、プロジェクトのドキュメントを迅速かつ効率的に自動生成するために設計された強力なPythonツールです。プロジェクトのディレクトリ構造をスキャンし、ディレクトリとファイルをリストアップし、一般的なソースコードファイル（Python、JavaScript、Java、HTML、CSS、シェルスクリプトなど）のコンテンツをドキュメントに含めるために抽出します。

**Doc_Project_Toolの主な目的:**

- **時間の節約:** ドキュメント作成プロセスを自動化し、時間のかかる手作業を排除します。
- **使いやすさ:** 直感的なGUI（グラフィカルユーザーインターフェース）により、深いプログラミング知識を持たないユーザーでもアクセス可能。
- **柔軟性:** 除外するディレクトリとファイル、および出力形式（TXTまたはMarkdown）の構成をサポートし、特定のニーズに合わせてカスタマイズできます。
- **詳細なドキュメント:** 明確で読みやすいドキュメントを生成し、他の人がプロジェクトの構造とコンテンツを迅速に理解できるようにします。

**誰がDoc_Project_Toolを使用すべきか？**

- **プログラマー:** 個人またはチームプロジェクトのドキュメントを迅速に作成し、共有、アーカイブ、または引き継ぎたい場合。
- **プロジェクトマネージャー:** 効果的なプロジェクト追跡および管理のために、プロジェクト構造とコンポーネントの概要が必要な場合。
- **学生/学習者:** 課題、プロジェクト、または学習活動のためのプロフェッショナルなドキュメントを作成したい場合。

## 2. 機能

**Doc_Project_Tool** は、以下の主な機能を提供します。

- **複数のプロジェクトディレクトリのスキャン:** 複数のプロジェクトディレクトリの同時選択をサポートし、大規模または結合されたプロジェクトのドキュメント生成を可能にします。
- **サブディレクトリとファイルの除外:** ドキュメント生成から除外するサブディレクトリとファイル拡張子/名を指定でき、重要なプロジェクトコンポーネントに焦点を当てることができます。
- **TXTおよびMarkdown出力形式のサポート:**
    - **TXT:** プレーンテキスト形式で、どのテキストエディターでも簡単に読めます。
    - **Markdown（.md）:** 人気のあるドキュメント形式で、テキストフォーマット（見出し、リスト、コードブロックなど）をサポートし、HTMLおよびその他の形式に簡単に変換できます。Markdownは、GitHub、GitLabなどのオンラインドキュメントプラットフォームに最適です。
- **明確なディレクトリ構造リストの表示:** 生成されたドキュメントは、ASCIIアート文字（TXT用）またはリスト形式（Markdown用）を使用してプロジェクトのディレクトリ構造を視覚的に表し、プロジェクトの概要を把握しやすくします。
- **ソースコードファイルのコンテンツの抽出と表示:** `.py`、`.js`、`.java`、`.cpp`、`.html`、`.css`、`.bat`、`.sh`、`.txt`、`.env`などの一般的な拡張子のファイルの場合、ツールはドキュメント内でコンテンツを抽出して表示します（コードブロックを ``` で囲むことで基本的なシンタックスハイライト表示）。
- **エラー処理とファイル/ディレクトリのスキップ:** ツールは「ファイル/ディレクトリが見つかりません」や「アクセス拒否」などのエラーを適切に処理し、エラーとスキップされたファイル/ディレクトリに関する情報を出力ドキュメントに記録し、ユーザーに潜在的な問題を知らせます。
- **詳細モード（オプション）:** 詳細モードを有効にすると、ドキュメントには、処理されたファイルとディレクトリの数などの詳細情報が含まれます。
- **ユーザーフレンドリーなGUI（グラフィカルユーザーインターフェース）:** `customtkinter` および `tkinter` ライブラリを使用して、技術者でないユーザーにも直感的で使いやすいインターフェースを提供します。
- **完了通知と出力ディレクトリのオープン:** ドキュメント生成の成功時に、ツールは完了メッセージを表示し、生成されたドキュメントを含むディレクトリをすばやく開くためのボタンを提供します。

## 3. プロジェクト構造

```
Doc_Project_Tool/
├── .git/             (Gitディレクトリ - ドキュメントにリストされていません)
├── .gitignore        (Gitが無視するファイル/ディレクトリを指定するファイル)
├── Core/             (ツールのコアソースコードを含むディレクトリ)
│   ├── Tool.py       (ツールのメインPythonソースコードファイル)
├── moitruongao/     (Python仮想環境ディレクトリ - リストするか除外するかを選択可能)
├── run.bat           (Windowsでアプリケーションを実行するバッチファイル)
```

- **`.git/`**: バージョン履歴を含むGitディレクトリ。（通常、ドキュメントから除外されます）。
- **`.gitignore`**: Gitが追跡とコミットから無視するファイルとディレクトリをリストしたテキストファイル。
- **`Core/`**: ツールのメインPythonソースコードを含むディレクトリ。
    - **`Tool.py`**: ツールのロジック全体、ユーザーインターフェース、およびドキュメント生成機能を包含するPythonファイル。
- **`moitruongao/`**: Python仮想環境ディレクトリ。このディレクトリには、このプロジェクト用に隔離されたPythonライブラリが含まれており、他のプロジェクトとのバージョン競合を回避します。（除外されていない場合はドキュメントに含めることができます）。
- **`run.bat`**: 仮想環境をアクティブにして `Tool.py` を簡単に実行するためのバッチスクリプト（Windows）。

## 4. インストール

### 前提条件

**Doc_Project_Tool** をインストールして使用する前に、システムに以下がインストールされていることを確認してください。

1. **Python:** Pythonバージョン3.8以降。Python公式サイトからダウンロードできます。[https://www.python.org/downloads/](https://www.python.org/downloads/)

2. **pip:** （通常Pythonと一緒にインストールされます）PipはPythonのパッケージマネージャーであり、プロジェクトに必要なライブラリをインストールするために使用されます。

### インストール手順

1. **プロジェクトのダウンロード:** GitHub（または他のソース）から **Doc_Project_Tool** プロジェクトのソースコードをクローンまたはダウンロードします。

   ```bash
   git clone https://github.com/Rin1809/Doc_Project_Tool/
   cd Doc_Project_Tool
   ```

2. **仮想環境の作成（推奨）:** 仮想環境を使用すると、各プロジェクトのPythonライブラリを独立して管理できます。**Doc_Project_Tool** プロジェクトディレクトリで、次のコマンドを実行して `moitruongao` という名前の仮想環境を作成します。

   ```bash
   python -m venv moitruongao
   ```

3. **仮想環境のアクティブ化:**

   - **Windowsの場合:** プロジェクトディレクトリにある `run.bat` ファイルを実行します。 `run.bat` は仮想環境を自動的にアクティブ化し、アプリケーションを実行します。

     または、コマンドプロンプトまたはPowerShellで次のコマンドを使用して手動でアクティブ化することもできます。
     ```bash
     moitruongao\Scripts\activate.bat
     ```

   - **macOS/Linuxの場合:** ターミナルで次のコマンドを実行します。
     ```bash
     source moitruongao/bin/activate
     ```

4. **ライブラリのインストール（必要な場合）:** **Doc_Project_Tool** は、次のライブラリを使用します。`customtkinter`、`tkinter`、および `ttk`。これらのライブラリは `Tool.py` にインポートされていますが、ライブラリが見つからないエラーが発生した場合は、仮想環境にインストールされていることを確認してください。

   `run.bat` を開くと、`pip install -r requirements.txt` という行があります。 `requirements.txt` ファイル（リポジトリで利用可能な場合）には、必要なライブラリがリストされています。

   `requirements.txt` が存在しない場合は、仮想環境がアクティブになっている間に `pip install` コマンドを使用してライブラリを手動でインストールできます。
   ```bash
   pip install customtkinter tkinter ttkbootstrap
   ```
   （注：`ttkbootstrap` は `tkinter` のテーマであり、オプションです。`customtkinter` にはすでに美しいテーマが含まれており、`ttkbootstrap` は必要ない場合があります。）

5. **アプリケーションの実行:**

   - **Windowsの場合（推奨）:** `run.bat` ファイルを実行します。このファイルは仮想環境をアクティブ化し（まだアクティブ化されていない場合）、次に `Core\Tool.py` を実行してGUIアプリケーションを起動します。

   - **直接実行（仮想環境をアクティブ化した後、任意のOS）:**
     `Core/` ディレクトリに移動し、次のコマンドを実行します。
     ```bash
     cd Core
     python Tool.py
     ```

     または、プロジェクトのルートディレクトリから、次を実行します。
     ```bash
     python Core/Tool.py
     ```

     **Doc_Project_Tool** のグラフィカルインターフェースが表示されます。

## 5. 使用方法

### GUI（グラフィカルユーザーインターフェース）

`Tool.py` または `run.bat` を実行すると、**Doc_Project_Tool** のメインインターフェースが表示されます。

インターフェースは、主に次のセクションに分かれています。

1. **プロジェクトディレクトリの選択:** この領域では、ドキュメントを生成するプロジェクトディレクトリを追加および管理できます。
    - **プロジェクトディレクトリリスト:** 選択されたプロジェクトディレクトリのリストを表示します。
    - **[追加]ボタン:** プロジェクトディレクトリをリストに追加するためのディレクトリ選択ダイアログを開きます。
    - **[削除]ボタン:** 現在選択されているディレクトリをリストから削除します。

2. **除外設定:** この領域は、除外を構成するために使用されます。
    - **除外するサブディレクトリ:** 除外するサブディレクトリ名のリストを入力できる大きなテキストボックス（例：`__pycache__`、`venv`、`.git`）。各サブディレクトリ名を新しい行に入力します。
    - **除外するファイル:** 除外するファイル拡張子またはファイル名のリストを入力できる大きなテキストボックス（例：`.pyc`、`desktop.ini`、`.json`、`*.log`）。各拡張子またはファイル名を新しい行に入力します。
    - **[デフォルトを追加]ボタン:** 一般的に使用される除外するサブディレクトリとファイルの事前定義されたリストを挿入します。

3. **出力設定:** 出力ディレクトリとドキュメントファイル名を構成する領域。
    - **出力ディレクトリ:**
        - **[出力ディレクトリ]ラベル:** 出力ディレクトリフィールドのラベル。
        - **パス入力フィールド:** 現在の出力ディレクトリパス（デフォルトは現在のディレクトリ「。」）を表示します。パスを直接入力するか、[参照...]ボタンを使用できます。
        - **[参照...]ボタン:** 出力ディレクトリを選択するためのディレクトリ選択ダイアログを開きます。
    - **ファイル名:**
        - **[ファイル名]ラベル:** ファイル名フィールドのラベル。
        - **基本ファイル名入力フィールド:** 基本ファイル名（例：`project_documentation`）を入力します。最終的なファイル名は `[基本ファイル名].txt` または `[基本ファイル名].md` になり、同じ名前のファイルがすでに存在する場合は、数値サフィックスが付加される可能性があります。

4. **出力形式:** 出力ドキュメント形式を選択します。
    - **[txt]ラジオボタン:** プレーンテキストの`.txt`形式を選択します。
    - **[Markdown]ラジオボタン:** Markdown `.md` 形式を選択します。

5. **オプションと実行:**
    - **[詳細]チェックボックス:** 出力ドキュメントに詳細情報（処理されたファイル数、ディレクトリ数）を含めるために、詳細モードを有効にします。
    - **[ドキュメントを生成]ボタン:** プロジェクトドキュメントの生成プロセスを開始するためのメインボタン。すべての設定を構成したら、このボタンをクリックします。

6. **出力表示:** ドキュメント生成中のメッセージ（エラーメッセージ、警告、完了通知を含む）を表示するための、インターフェースの下部にある大きなテキストボックス。

### 入力フィールドの説明

- **プロジェクトディレクトリ:** 構造とコンテンツを文書化するプロジェクトのルートディレクトリを1つ以上選択します。
- **除外するサブディレクトリ:** ドキュメントに含めずにスキップするサブディレクトリ名（選択したプロジェクトディレクトリ内）をリストします。例：`__pycache__`、`node_modules`、`venv`、`.git`。各サブディレクトリ名を新しい行に入力します。
- **除外するファイル:** スキップするファイル拡張子（例：`.pyc`、`.log`、`.tmp`）または特定のファイル名をリストします。例：`.log`、`temp.txt`、`*.bak`。各除外を新しい行に入力します。
- **出力ディレクトリ:** 生成されたドキュメントファイルを保存するディレクトリを選択します。選択しない場合、ファイルはアプリケーションの現在のディレクトリに保存されます。
- **ファイル名:** 出力ドキュメントファイルの名前を設定します（例：`project_docs`）。実際のファイル名には、選択した形式に応じて拡張子 `.txt` または `.md` が付加され、ファイル名が既に存在する場合は、番号が付加される場合があります。
- **形式:** 出力ドキュメントの形式として `.txt` （プレーンテキスト）または `.md` （Markdown）を選択します。
- **詳細:** [詳細] チェックボックスをオンにすると、ドキュメントには、処理されたファイルとディレクトリの数に関する追加情報が含まれます。

**使用手順:**

1. **プロジェクトディレクトリを追加:** [追加]ボタンをクリックして、1つまたは複数のプロジェクトディレクトリを選択します。選択したディレクトリがリストに表示されます。
2. **除外を構成する（オプション）:** 対応するテキストボックスに除外するサブディレクトリとファイルを入力します。または、[デフォルトを追加] をクリックして、一般的な除外リストを使用します。
3. **出力ディレクトリを選択:** ドキュメントを保存するディレクトリを選択します。変更しない場合、ファイルはアプリケーションの現在のディレクトリに保存されます。
4. **ファイル名を入力:** ドキュメントファイルの基本名を入力します。
5. **出力形式を選択:** [txt] または [Markdown] を選択します。
6. **[詳細] を選択（オプション）:** 必要に応じて [詳細] チェックボックスをオンにします。
7. **[ドキュメントを生成] をクリック:** このボタンをクリックして、ドキュメント生成プロセスを開始します。
8. **出力を監視:** [出力表示] テキストボックスを見て、進行状況、エラーメッセージ、完了通知を監視します。
9. **ドキュメントを確認:** 完了後、選択した出力ディレクトリに生成されたドキュメントファイルを確認します。完了ダイアログの [フォルダーに移動] をクリックして、ドキュメントを含むディレクトリを開きます。

## 6. 使用例

**Doc_Project_Tool** の使用方法を視覚化するために、いくつかの特定の使用例を見てみましょう。

### 例 1：小規模なPythonプロジェクトの基本的なTXTドキュメントを生成する

**シナリオ:** 次のような構造の `my_python_project` という名前のシンプルなPythonプロジェクトがあります。

```
my_python_project/
├── main.py
├── utils/
│   ├── helper.py
└── requirements.txt
```

プロジェクト構造とPythonコードファイルの内容を表示するために、基本的なTXTドキュメントを生成します。

**実行する手順:**

1. **Doc_Project_Toolを起動:** `run.bat` (Windows) または `python Core/Tool.py` (macOS/Linux) を実行して、アプリケーションインターフェースを開きます。

2. **プロジェクトディレクトリを追加:**
   - **[プロジェクトディレクトリを選択]** 領域の **[追加]** ボタンをクリックします。
   - ディレクトリ選択ダイアログから `my_python_project` ディレクトリを選択し、**[フォルダーを選択]** をクリックします。
   - `my_python_project` ディレクトリが **プロジェクトディレクトリ** リストに表示されます。

3. **除外設定:** この簡単な例では、サブディレクトリまたはファイルを除外**しません**。**[除外するサブディレクトリ]** および **[除外するファイル]** テキストボックスを空のままにします。

4. **出力設定:**
   - **出力ディレクトリ:** デフォルトのままにします（通常はアプリケーションの現在のディレクトリ）。
   - **ファイル名:** **[ファイル名]** フィールドに `python_project_docs` と入力します。

5. **出力形式:** **[txt]** ラジオボタンを選択して、TXT形式のドキュメントを生成します。

6. **詳細オプション:** この簡単な例では、**[詳細]** チェックボックスを**オンにしません**。

7. **実行:** **[ドキュメントを生成]** ボタンをクリックします。

8. **結果を表示:** ドキュメントの生成が完了したら（「完了」メッセージが表示されたら）、選択した出力ディレクトリを開きます。`python_project_docs.txt` ファイルが表示されます。

**`python_project_docs.txt` の内容（例）:**

```txt
プロジェクト: my_python_project - ...

my_python_project/
├── main.py
└── utils/
    └── helper.py


my_python_project/
**main.py**
```python
def main():
    print("こんにちは、my_python_projectから！")
    # utilsモジュールからヘルパー関数を呼び出す
    from utils import helper
    helper.say_hello("ユーザー")

if __name__ == "__main__":
    main()
```

```
**utils\helper.py**
```python
def say_hello(name):
    print(f"こんにちは、{name}さん、ヘルパーモジュールから！")
```


**説明:**

- TXTドキュメントファイルが出力ディレクトリに正常に作成されました。
- `my_python_project` ディレクトリ構造が明確にリストされています。
- Pythonファイル（`main.py`、`utils\helper.py`）の内容が抽出され、下に表示され、コードブロックをマークするために ``` で囲まれています。

---

### 例 2：WebプロジェクトのMarkdownドキュメントを生成し、仮想環境ディレクトリを除外する

**シナリオ:** HTML、CSS、JavaScript、およびドキュメントから除外する仮想環境ディレクトリ `venv` を使用するフロントエンドWebプロジェクトがあります。プロジェクト構造は次のようになります。

```
my_web_project/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
│   └── logo.png   （この画像ファイルを除外します）
└── venv/          （除外する仮想環境ディレクトリ）
```

Markdownドキュメントを生成し、`venv` ディレクトリと画像ファイル `logo.png` を除外します。

**実行する手順:**

1. **Doc_Project_Toolを起動します。**

2. **プロジェクトディレクトリを追加:** 例1のように、`my_web_project` ディレクトリをプロジェクトリストに追加します。

3. **除外設定:**
   - **除外するサブディレクトリ:** **[除外するサブディレクトリ]** テキストボックスに `venv` と入力します。
   - **除外するファイル:** **[除外するファイル]** テキストボックスに `logo.png` と入力します。

4. **出力設定:**
   - **出力ディレクトリ:** 目的のディレクトリ（例：デスクトップ）を選択します。
   - **ファイル名:** **[ファイル名]** フィールドに `web_project_docs` と入力します。

5. **出力形式:** **[Markdown]** ラジオボタンを選択して、Markdown形式のドキュメントを生成します。

6. **詳細オプション:** 詳細な処理情報を確認したい場合は、**[詳細]** チェックボックスを**オンにできます**。

7. **実行:** **[ドキュメントを生成]** ボタンをクリックします。

8. **結果を表示:** 完了後、デスクトップ（または選択した出力ディレクトリ）を開きます。`web_project_docs.md` ファイルが表示されます。

**`web_project_docs.md` の内容の一部（例）:**

```markdown
# プロジェクト: my_web_project - ...

my_web_project/
├── index.html
├── css/
│   └── styles.css
├── js/
│   └── script.js
├── img/
└── venv/          (リストされていません)


### ［ファイル処理中]
✅ my_web_project/index.html

- 📁 スキャンしたディレクトリ: 2
- 📄 スキャンしたファイル: 3
- 📂 スキップしたディレクトリ:
    └──venv
- 📄 スキップしたファイル:
    └── img\logo.png

**index.html**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>私のウェブページ</title>
    <link rel="stylesheet" href="css/styles.css">
</head>
<body>
    <h1>私のウェブページへようこそ！</h1>
    <img src="img/logo.png" alt="ロゴ">
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
console.log("ウェブページがロードされました！");
```

**説明:**

- Markdownドキュメントファイルが正常に作成されました。
- ディレクトリ構造はMarkdownリストとして表示されます。
- `venv/` ディレクトリと `img/logo.png` ファイルは除外されており、ドキュメントの最後にある「スキップされたディレクトリ」および「スキップされたファイル」セクションに注意書きされています。
- HTML、CSS、JavaScriptファイルの内容が抽出され、Markdownコードブロック（```markdown）内に表示されています。

---

### さらに詳しく探る

**[詳細]** モードを有効にする、複数のプロジェクトディレクトリを追加する、除外リストをカスタマイズするなど、さまざまな設定を試して、**Doc_Project_Tool** の全機能を探索してください。

プロジェクトのドキュメント作成をお楽しみください！

## 7. 高度な構成

### デフォルトの除外ファイル

**Doc_Project_Tool** には、プロジェクトドキュメントでは一般的で、不要と見なされる、デフォルトの除外されたサブディレクトリとファイル拡張子が事前構成されています。例：

**デフォルトで除外されるサブディレクトリ:**
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

**デフォルトで除外されるファイル:**
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

GUIの [除外するサブディレクトリ] および [除外するファイル] テキストボックスを直接編集して、このリストをカスタマイズできます。[デフォルトを追加] ボタンを使用すると、必要に応じてデフォルトの除外リストをすばやく復元できます。

### 出力形式

**Doc_Project_Tool** は、**TXT** および **Markdown** の2つの主要な出力形式をサポートしています。

- **TXT (.txt):** プレーンテキストファイルを作成します。どのテキストエディターでも簡単に読めます。ディレクトリ構造はASCIIアート文字で表されます。コードファイルの内容は ``` で囲まれ、コードブロックとしてマークされます（ただし、シンタックスハイライト表示はありません）。簡単な読み取りや印刷に適しています。

- **Markdown (.md):** Markdownファイルを作成します。これは、技術ドキュメントで非常に人気のある形式です。Markdownでは、より豊富なテキストフォーマット（見出し、リスト、コードブロックなど）が可能になり、HTMLに簡単に変換できます。ディレクトリ構造はMarkdownリストで表されます。コードファイルの内容は ```markdown で囲まれ、Markdownコードブロックを作成します。Markdown形式は、GitHub、GitLabなどのプラットフォームでオンラインで表示したり、静的サイトジェネレーターで使用したりするのに非常に適しています。

ドキュメントを生成する前に、使用ニーズに最適な出力形式を選択できます。

</details>
