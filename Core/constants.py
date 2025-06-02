# Core/constants.py
# Hang so cho UD

# --- Ngon ngu ---
DEFAULT_LANGUAGE = "vi"
CONFIG_FILE_NAME = "doc_tool_config.json"

# Fonts
TITLE_FONT_SIZE = 18 # Giu nguyen, hoac chinh nhe neu can
HEADER_FONT_SIZE = 14
NORMAL_FONT_SIZE = 10
SMALL_FONT_SIZE = 9

# Mau sac - Stellar Poetic Theme
WINDOW_BG_COLOR = "rgb(10, 12, 28)" # Xanh den sau tham
CONTAINER_BG_COLOR = "rgba(20, 25, 50, 0.92)" # Xanh tim, trong suot hon chut
TITLE_BAR_BG_COLOR = "rgba(15, 18, 35, 0.95)" # Dam hon container, it trong suot hon

PRIMARY_COLOR = "rgb(65, 75, 115)" # Xanh xam tram
ACCENT_COLOR = "rgb(65, 75, 115)" 
HOVER_COLOR = "rgb(85, 100, 145)" # Dam hon primary
SELECTED_COLOR = "rgb(130, 170, 255)" # Sang hon accent
TEXT_HOVER_COLOR = "rgb(240, 245, 255)" # Mau chu khi hover, sang hon TEXT_COLOR mot chut
ACCENT_GLOW_COLOR = "rgba(110, 150, 255, 0.3)" # Mau glow nhe cho accent

TEXT_COLOR = "rgb(225, 230, 245)" # Trang nga (lunar white)
SUBTEXT_COLOR = "rgb(155, 160, 180)" # Xam nhat
INPUT_BG_COLOR = "rgba(12, 15, 32, 0.9)" # Nen input toi
INPUT_BORDER_COLOR = "rgba(140, 150, 190, 0.5)" # Vien input mo
INPUT_FOCUS_BORDER_COLOR = "rgb(160, 190, 255)" # Vien focus sang
INPUT_PLACEHOLDER_COLOR = "rgb(120, 125, 145)" # Mau cho placeholder text

SUCCESS_COLOR = "rgb(65, 75, 115)"  # Xanh la nhat
WARNING_COLOR = "rgb(230, 170, 80)" # Vang cam
ERROR_COLOR = "rgb(220, 90, 100)"   # Do hong

# Mau cho thanh cuon
SCROLLBAR_BG_COLOR = "rgba(18, 22, 40, 0.85)"
SCROLLBAR_HANDLE_COLOR = "rgb(85, 100, 145)" # Giong HOVER_COLOR
SCROLLBAR_HANDLE_HOVER_COLOR = "rgb(110, 150, 255)" # Giong ACCENT_COLOR
SCROLLBAR_HANDLE_PRESSED_COLOR = "rgb(130, 170, 255)" # Giong SELECTED_COLOR

# Loai tru MD
DEFAULT_EXCLUDED_SUBDIRS = ["__pycache__", "moitruongao", "venv", ".git", ".vscode", "bieutuong", "memory", "node_modules", "uploads", "chats", "package-lock.json", "dist", "build", "assets"]
DEFAULT_EXCLUDED_FILES = [".pyc", "desktop.ini", ".rar", "ex.json", ".jpg", ".mp3", ".png", ".ico", ".jpeg", ".gif"]

# Ten tep & TM MD
DEFAULT_OUTPUT_DIR = "."
DEFAULT_BASE_FILENAME = "tai_lieu_du_an"

# File ext ho tro
SUPPORTED_FILE_EXTENSIONS = ('.py', '.js', '.java', '.cpp', '.html', '.css', '.bat', '.sh', '.txt', '.env', '.tsx', '.mjs', '.json', '.ts', 'Dockerfile', '.qss', '.md')

# Lich su
HISTORY_FILE = "doc_tool_history.json"
MAX_HISTORY_ITEMS = 15

# UI PySide6
WINDOW_DEFAULT_WIDTH = 1000
WINDOW_DEFAULT_HEIGHT = 800
WINDOW_MIN_WIDTH = 800
WINDOW_MIN_HEIGHT = 700
RESIZE_MARGIN = 10
NO_EDGE, TOP_EDGE, BOTTOM_EDGE, LEFT_EDGE, RIGHT_EDGE = 0x0, 0x1, 0x2, 0x4, 0x8
TOP_LEFT_CORNER, TOP_RIGHT_CORNER = TOP_EDGE | LEFT_EDGE, TOP_EDGE | RIGHT_EDGE
BOTTOM_LEFT_CORNER, BOTTOM_RIGHT_CORNER = BOTTOM_EDGE | LEFT_EDGE, BOTTOM_EDGE | RIGHT_EDGE

# Paths
ASSETS_DIR_NAME = "assets"
DEFAULT_ICON_NAME = "icon.ico"
DEFAULT_BACKGROUND_NAME = "background.jpg"