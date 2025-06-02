import sys
import os
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon

# Xu ly AppUserModelID cho Windows de icon hien thi dung tren taskbar
IS_WINDOWS = os.name == 'nt'
if IS_WINDOWS:
    try:
        import ctypes
        myappid = u'mycompany.docprojecttool.pyside6.1_0_0' 
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    except (ImportError, AttributeError, Exception):
        pass 


from .main_app import ProjectDocApp 
from .constants import ASSETS_DIR_NAME, DEFAULT_ICON_NAME

def main():
    app = QApplication(sys.argv)

 
    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    base_app_path = os.path.dirname(current_file_dir)
    
    # Set icon cho toan bo ung dung (hien thi tren taskbar)
    icon_path_app_level = os.path.join(base_app_path, ASSETS_DIR_NAME, DEFAULT_ICON_NAME)
    if os.path.exists(icon_path_app_level):
        app.setWindowIcon(QIcon(icon_path_app_level))
    else:
        print(f"Khong tim thay icon ung dung: {icon_path_app_level}")

    window = ProjectDocApp(base_app_path)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()