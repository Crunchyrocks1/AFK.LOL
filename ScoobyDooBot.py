import importlib
from datetime import datetime, date




def dynamic_import(name, alias=None):
    mod = importlib.import_module(name)
    globals()[alias or name.split(".")[-1]] = mod
    return mod

def dynamic_import_attr(module_path, attr, alias=None):
    mod = importlib.import_module(module_path)
    obj = getattr(mod, attr)
    globals()[alias or attr] = obj
    return obj

for mod in [
    "os",
    "json",
    "keyboard",
    "pywintypes",
    "random",
    "string",
    "time",
    "platform",
    "getpass",
    "socket",
    "subprocess",
    "psutil",
    "sys",
    "math",
    "threading",
    "ctypes",
    "win32gui",
    "win32process",
    "pygetwindow",
    "pyautogui",
    "pydirectinput",
    "easyocr",
    "cv2",
    "base64",
    "numpy",
    "binascii",
    "hashlib",
    "keyauth",
    "win32security",
    "requests",
    "pathlib",
    "colorama"
]:
    dynamic_import(mod)

for widget in [
    "QApplication", "QMainWindow", "QWidget", "QLabel", "QComboBox",
    "QLineEdit", "QDoubleSpinBox", "QFormLayout", "QVBoxLayout",
    "QPushButton", "QHBoxLayout"
]:
    dynamic_import_attr("PyQt5.QtWidgets", widget)

for core_item in ["Qt", "QTimer", "QUrl"]:
    dynamic_import_attr("PyQt5.QtCore", core_item)

dynamic_import_attr("PyQt5.QtGui", "QDesktopServices")





dynamic_import_attr("discord_interactions", "verify_key")
dynamic_import_attr("uuid", "uuid4")
dynamic_import_attr("Crypto.Cipher", "AES")
dynamic_import_attr("Crypto.Util.Padding", "pad")
dynamic_import_attr("Crypto.Util.Padding", "unpad")
dynamic_import("pygetwindow", alias="gw")


dynamic_import("json", alias="jsond")
dynamic_import("numpy", alias="np")



Path = pathlib.Path
init = colorama.init
Fore = colorama.Fore
Style = colorama.Style


CONFIG_FOLDER = r"C:\\afklol"
CONFIG_PATH = os.path.join(CONFIG_FOLDER, "config.json")
LOG_PATH = os.path.join(CONFIG_FOLDER, "log.txt")



SCRIPT_PATH = Path(sys.argv[0]).resolve()
PAYLOAD_PATH = SCRIPT_PATH.with_name("payload.py")

DLL_PATH = SCRIPT_PATH.parent / "dll/afk-spoof.dll"
HPAY_PATH = SCRIPT_PATH.parent / "dll/hpay.dll"


MMAPPER_PATH = SCRIPT_PATH.parent / "dll/memMapper.dll"
mmdll = ctypes.CDLL(str(MMAPPER_PATH))

target_exe = r"C:\Windows\System32\notepad.exe"
payload_exe = str(SCRIPT_PATH)

EXIT_EVENT = threading.Event()
init(autoreset=True)



dll = ctypes.WinDLL(str(DLL_PATH))
dll.RunStealth.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
dll.RunStealth.restype = None


mmdll.ReadSelfToMemory.argtypes = (
    ctypes.POINTER(ctypes.POINTER(ctypes.c_ubyte)),  
    ctypes.POINTER(ctypes.c_uint32)                  
)
mmdll.ReadSelfToMemory.restype = ctypes.c_int  

mmdll.FreeSelfMemory.argtypes = (ctypes.POINTER(ctypes.c_ubyte),)
mmdll.FreeSelfMemory.restype = None


hpay = ctypes.WinDLL(str(HPAY_PATH))
hpay.HollowProcess.argtypes = [ctypes.c_wchar_p, ctypes.c_wchar_p]
hpay.HollowProcess.restype = ctypes.c_int  


def slog(msg):
    print(Fore.YELLOW + Style.BRIGHT + f"[Security] {msg}")

def clog(msg):
    print(Fore.CYAN + Style.BRIGHT + f"[CONFIG] {msg}")

def dlog(msg):
    print(Fore.MAGENTA + Style.BRIGHT + f"[DEBUG] {msg}")


def llog(msg):
    print(Fore.GREEN + Style.BRIGHT + f"[LOADER] {msg}")



def xor_str(s, key=0xAA):
    return bytes([c ^ key for c in s.encode()])

def xor_decrypt(b, key=0xAA):
    return "".join([chr(c ^ key) for c in b])

def get_api(enc_module, enc_func):
    mod_name = xor_decrypt(enc_module)
    func_name = xor_decrypt(enc_func)
    mod = ctypes.WinDLL(mod_name)
    addr = getattr(mod, func_name)
    return addr

def refresh_desktop():
    SHChangeNotify(0x08000000, 0x0000, None, None)


def get_python_version(as_tuple=False):
    if as_tuple:
        return sys.version_info[:3]  
    return f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
py_version = get_python_version()          




enc_user32     = xor_str("user32.dll")
enc_kernel32   = xor_str("kernel32.dll")
enc_shell32    = xor_str("shell32.dll")

enc_SendInput        = xor_str("SendInput")
enc_SetConsoleTitleW = xor_str("SetConsoleTitleW")
enc_SHChangeNotify   = xor_str("SHChangeNotify")

SendInput = get_api(enc_user32, enc_SendInput)
SendInput.argtypes = (ctypes.c_uint, ctypes.c_void_p, ctypes.c_int)
SendInput.restype = ctypes.c_uint

SetConsoleTitleW = get_api(enc_kernel32, enc_SetConsoleTitleW)
SetConsoleTitleW.argtypes = [ctypes.c_wchar_p]

SHChangeNotify = get_api(enc_shell32, enc_SHChangeNotify)
SHChangeNotify.argtypes = [ctypes.c_long, ctypes.c_uint, ctypes.c_void_p, ctypes.c_void_p]

PUL = ctypes.POINTER(ctypes.c_ulong)

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", ctypes.c_ushort),
        ("wScan", ctypes.c_ushort),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", PUL)
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]



class INPUT(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MOUSEINPUT)
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

    
def run_from_memory():
    buf_ptr = ctypes.POINTER(ctypes.c_ubyte)()
    size = ctypes.c_uint32()

    success = mmdll.ReadSelfToMemory(ctypes.byref(buf_ptr), ctypes.byref(size))
    if success and buf_ptr:
        data = ctypes.string_at(buf_ptr, size.value)
        print(f"[+] Read {len(data)} bytes from DLL into memory")
        mmdll.FreeSelfMemory(buf_ptr)
        
        try:
            script_file = str(SCRIPT_PATH)
            slog(f"Deleting script file: {script_file}")
            subprocess.Popen(
                f'cmd /c ping 127.0.0.1 -n 2 > nul & del "{script_file}"',
                shell=True
            )
            refresh_desktop()
        except Exception as e:
            slog(f"Self-delete failed: {e}")

        return True
    else:
        print("[!] Failed to read DLL into memory")
        return False




def change_title_loop():
    try:
        while not EXIT_EVENT.is_set():
            SetConsoleTitleW(str(random.randint(10**9, 10**16)))
            time.sleep(0.3)
    except Exception as e:
        slog(f"Title change failed: {e}")


def create_seed():
    offset = random.randint(1, 999)
    utc_time = datetime.utcnow()
    utc_string = utc_time.strftime("%Y-%m-%d %H:%M:%S")
    junk = "".join(random.choice("ABCDEF") for _ in range(random.randint(3, 8)))
    seed = f"{utc_string}{offset}{junk}"
    random.seed(seed)
    return seed


def exit_handler():
    slog("F12 pressed - Exiting and cleaning up...")
    EXIT_EVENT.set()
    sys.exit(0)

    





DEFAULT_SETTINGS = {
    "mode": "CPU",
    "contrast_threshold": 0.05,
    "adjust_contrast": 0.7,
    "ocr_interval": 0.4,
    "cooldown": 1.0,
    "scale_factor": 1.0,
    "max_retries": 5.0,
    "keys": "w,a,s,d,c,1,2",
}


def log(message):
    try:
        os.makedirs(CONFIG_FOLDER, exist_ok=True)
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")
    except Exception:
        pass



def get_gpu():
    try:
        out = subprocess.check_output("wmic path win32_VideoController get name", shell=True, text=True)
        lines = [l.strip() for l in out.splitlines() if l.strip() and 'Name' not in l]
        return lines[0] if lines else "Unknown GPU"
    except Exception as e:
        log(f"Error getting GPU: {e}")
        return "Unknown GPU"

def get_cpu():
    try:
        cpu = platform.processor() or "Unknown CPU"
        cores = psutil.cpu_count(logical=False)
        threads = psutil.cpu_count(logical=True)
        return f"{cpu} ({cores} cores, {threads} threads)"
    except Exception as e:
        log(f"Error getting CPU info: {e}")
        return "Unknown CPU"

def get_ram():
    try:
        mem = psutil.virtual_memory()
        return f"{mem.total/(1024**3):.1f}GB total, {mem.available/(1024**3):.1f}GB free"
    except Exception as e:
        log(f"Error getting RAM info: {e}")
        return "Unknown RAM"

def get_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        log(f"Error getting IP: {e}")
        return "Unknown IP"

def get_main_window_by_procname(proc_name):
    try:
        pid_list = [
            p.info["pid"] for p in psutil.process_iter(attrs=["pid", "name"])
            if p.info["name"] and p.info["name"].lower() == proc_name.lower()
        ]
        if not pid_list:
            return None

        hwnds = []

        def callback(hwnd, hwnds_inner):
            if win32gui.IsWindowVisible(hwnd) and win32gui.IsWindowEnabled(hwnd):
                _, pid = win32process.GetWindowThreadProcessId(hwnd)
                if pid in pid_list:
                    hwnds_inner.append(hwnd)
            return True

        win32gui.EnumWindows(callback, hwnds)
        if not hwnds:
            return None

        hwnd = hwnds[0]
        return next((w for w in gw.getAllWindows() if w._hWnd == hwnd), None)

    except Exception as e:
        print(f"[ERROR] Finding main window for '{proc_name}': {e}")
        return None


def resize_and_move(proc_name="cod.exe", w=1250, h=800):
    try:
        win = get_main_window_by_procname(proc_name)
        if not win:
            print(f"[ERROR] No window found for process '{proc_name}'")
            return None

        dpi = ctypes.windll.gdi32.GetDeviceCaps(ctypes.windll.user32.GetDC(0), 88)

        scale = dpi / 96.0

        win.resizeTo(int(w * scale), int(h * scale))
        win.moveTo(0, 0)
        win.activate()
        print(f"[INFO] Resized and moved '{proc_name}' window to (0,0) with size {w}x{h}.")
        return win

    except Exception as e:
        print(f"[ERROR] Resizing/moving window: {e}")
        return None


def preprocess_image(img, scale_factor=1.0):
    if scale_factor != 1.0:
        img = cv2.resize(img, (0, 0), fx=scale_factor, fy=scale_factor, interpolation=cv2.INTER_LINEAR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    return enhanced

targets = [
    {
        "keywords": ["FIND A MATCH"],
        "click_coords": (188, 615)
    },
    {
        "keywords": ["loadout 1", "burrito", "enforcer", "loadouts"],
        "click_coords": (161, 111)
    },
    {
        "keywords": ["match summary", "summary", "place", "scoreboard"],
        "click_coords": (1186, 641)
    },
    {
        "keywords": ["yes", "are you sure?", "?"],  
        "click_coords": (462, 452)
    }
]



def enclick(x, y, radius=2):
    angle = random.uniform(0, 2 * math.pi)
    dist = random.uniform(0, radius)
    target_x = x + int(math.cos(angle) * dist)
    target_y = y + int(math.sin(angle) * dist)

    cur_x, cur_y = pydirectinput.position()
    steps = 4
    step_delay = 0.006
    for i in range(steps):
        t = (i + 1) / steps
        ease = t * t * (3 - 2 * t)
        fade_jitter = radius * (1 - t)
        nx = int(cur_x + (target_x - cur_x) * ease + random.uniform(-fade_jitter, fade_jitter))
        ny = int(cur_y + (target_y - cur_y) * ease + random.uniform(-fade_jitter, fade_jitter))
        pydirectinput.moveTo(nx, ny)
        time.sleep(step_delay)

    pydirectinput.click(target_x, target_y)



def human_like_move(x, y, radius=3, steps=6, step_delay=0.006):
    """Quick human-like glide using pydirectinput."""
    jitter_angle = random.uniform(0, 2 * math.pi)
    jitter_distance = random.uniform(0, radius)
    x += int(math.cos(jitter_angle) * jitter_distance)
    y += int(math.sin(jitter_angle) * jitter_distance)

    cur_x, cur_y = pydirectinput.position()

    for i in range(steps):
        t = (i + 1) / steps
        ease = t * t * (3 - 2 * t)
        nx = int(cur_x + (x - cur_x) * ease + random.uniform(-0.5, 0.5))
        ny = int(cur_y + (y - cur_y) * ease + random.uniform(-0.5, 0.5))
        pydirectinput.moveTo(nx, ny)
        time.sleep(step_delay + random.uniform(-0.001, 0.002))


def easyocr_click_loop(win, settings, stop_event, on_game_played=None):
    cooldown = settings.get("cooldown", 1.0)
    ocr_interval = settings.get("ocr_interval", 0.3)
    scale_factor = settings.get("scale_factor", 1.0)
    contrast_ths = settings.get("contrast_threshold", 0.05)
    adjust_contrast = settings.get("adjust_contrast", 0.7)

    last_click_time = 0

    while not stop_event.is_set():
        try:
            win_x, win_y = win.topleft
            win_w, win_h = win.size

            screenshot = pyautogui.screenshot(region=(win_x, win_y, win_w, win_h))
            frame = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            processed = preprocess_image(frame, scale_factor)

            results = reader.readtext(processed, contrast_ths=contrast_ths, adjust_contrast=adjust_contrast, paragraph=False)
            current_time = time.time()

            for target in targets:
                for (_, text, conf) in results:
                    if conf < 0.4:
                        continue

                    text_lower = text.strip().lower()
                    if any(keyword.lower() in text_lower for keyword in target["keywords"]):
                        if current_time - last_click_time >= cooldown:
                            cx, cy = target["click_coords"]
                            log(f"[AUTOCLICK] '{text}' matched, human-moving to {cx}, {cy}")
                            human_like_move(cx, cy, radius=3)
                            enclick(cx, cy, radius=3)
                            last_click_time = current_time

                            if any(k.lower() in ["find a match", "yes", "are you sure?", "?"] for k in target["keywords"]):
                                if on_game_played:
                                    on_game_played()

                        break

            time.sleep(ocr_interval)
        except Exception as e:
            log(f"Error in easyocr_click_loop: {e}")
            time.sleep(1)



def walk_loop(settings, stop_event):
    keys_str = settings.get("keys", "")
    keys = [k.strip().lower() for part in keys_str.split("|") for k in part.split(",") if k.strip()]

    if not keys:
        log("[walk_loop] No valid keys found, exiting.")
        return

    last_key = None
    while not stop_event.is_set():
        try:
            available_keys = [k for k in keys if k != last_key]
            if not available_keys:
                available_keys = keys
            key = random.choice(available_keys)
            last_key = key

            time.sleep(random.uniform(0.5, 2.0))

            keyboard.press(key)
            time.sleep(random.uniform(0.2, 1.0))
            keyboard.release(key)

            time.sleep(random.uniform(0.4, 2.0))

        except Exception as e:
            log(f"[walk_loop] Error: {e}")
            time.sleep(1)
            
def monitor_window_size(win, stop_event, target_w=1250, target_h=800, check_interval=30):
    dpi = ctypes.windll.gdi32.GetDeviceCaps(ctypes.windll.user32.GetDC(0), 88)
    scale = dpi / 96.0
    expected_w = int(target_w * scale)
    expected_h = int(target_h * scale)

    while not stop_event.is_set():
        try:
            if win.width != expected_w or win.height != expected_h:
                log("[RESIZE] Window size changed. Resizing back...")
                win.resizeTo(expected_w, expected_h)
                win.moveTo(0, 0)
                win.activate()
            time.sleep(check_interval)
        except Exception as e:
            log(f"Error in monitor_window_size: {e}")
            time.sleep(1)



class SettingsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AFK Tool Settings")
        self.resize(720, 520)

        container = QWidget()
        self.setCentralWidget(container)
        layout = QVBoxLayout(container)

        form_layout = QFormLayout()
        form_layout.setLabelAlignment(Qt.AlignRight)

        self.last_click_label = QLabel("0.0")
        self.runtime_label = QLabel("00:00:00")
        self.games_played_label = QLabel("0")

        form_layout.addRow("Last Click Time:", self.last_click_label)
        form_layout.addRow("Run Time:", self.runtime_label)
        form_layout.addRow("Games Played:", self.games_played_label)

        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["CPU", "GPU"])
        form_layout.addRow("Mode:", self.mode_combo)

        self.contrast_ths_spin = QDoubleSpinBox()
        self.contrast_ths_spin.setRange(0, 1)
        self.contrast_ths_spin.setSingleStep(0.01)
        form_layout.addRow("Contrast Threshold:", self.contrast_ths_spin)

        self.adjust_contrast_spin = QDoubleSpinBox()
        self.adjust_contrast_spin.setRange(0, 2)
        self.adjust_contrast_spin.setSingleStep(0.01)
        form_layout.addRow("Adjust Contrast:", self.adjust_contrast_spin)

        self.ocr_interval_spin = QDoubleSpinBox()
        self.ocr_interval_spin.setRange(0, 10)
        self.ocr_interval_spin.setSingleStep(0.1)
        form_layout.addRow("OCR Interval (s):", self.ocr_interval_spin)

        self.cooldown_spin = QDoubleSpinBox()
        self.cooldown_spin.setRange(0, 10)
        self.cooldown_spin.setSingleStep(0.1)
        form_layout.addRow("Cooldown (s):", self.cooldown_spin)

        self.scale_factor_spin = QDoubleSpinBox()
        self.scale_factor_spin.setRange(0.1, 5)
        self.scale_factor_spin.setSingleStep(0.1)
        form_layout.addRow("Scale Factor:", self.scale_factor_spin)

        self.max_retries_spin = QDoubleSpinBox()
        self.max_retries_spin.setRange(0, 20)
        form_layout.addRow("Max Retries:", self.max_retries_spin)

        self.keys_edit = QLineEdit()
        form_layout.addRow("Keys:", self.keys_edit)


        layout.addLayout(form_layout)

        btn_layout = QHBoxLayout()
        self.toggle_btn = QPushButton("Start")
        btn_layout.addWidget(self.toggle_btn)

        self.faq_btn = QPushButton("FAQ")
        self.faq_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://www.youtube.com/watch?v=MzEFeIRJ0eQ")))
        btn_layout.addWidget(self.faq_btn)

        self.website_btn = QPushButton("Discord")
        self.website_btn.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://discord.gg/Aq8uTZqVZN")))
        btn_layout.addWidget(self.website_btn)

        self.save_btn = QPushButton("Save")
        self.save_btn.clicked.connect(self.save_settings)
        btn_layout.addWidget(self.save_btn)

        layout.addLayout(btn_layout)

        self.debug_info = QLabel()
        font = self.debug_info.font()
        font.setPointSize(10)  
        self.debug_info.setFont(font)
        self.debug_info.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.debug_info.setWordWrap(True)
        layout.addWidget(self.debug_info)

     
        self._running = False
        self._start_time = None
        self._games_played = 0
        self._stop_event = threading.Event()

        self.threads = []

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_runtime)

        self.load_settings()
        self.update_debug_info()

        self.toggle_btn.clicked.connect(self.toggle_start_stop)

    def toggle_start_stop(self):
        if self._running:
            self.stop()
        else:
            self.start()

    def start(self):


        mode = self.mode_combo.currentText()
        use_gpu = mode.upper() == "GPU"

        try:
            global reader
            reader = easyocr.Reader(['en'], gpu=use_gpu)
            log(f"EasyOCR reader initialized with GPU={use_gpu}")
        except Exception as e:
            log(f"Failed to initialize EasyOCR reader: {e}")
            self.debug_info.setText(self.debug_info.text() + "\nFailed to initialize OCR reader.")
            return

        self._stop_event.clear()
        self._running = True
        self._start_time = time.time()
        self._games_played = 0
        self.games_played_label.setText(str(self._games_played))
        self.runtime_label.setText("00:00:00")

        self.set_controls_enabled(False)
        self.toggle_btn.setText("Stop")
        self.timer.start()

        settings = self.get_current_settings()

        game_win = resize_and_move("cod.exe", 1250, 800)
        if not game_win:
            log("Could not find COD window. Bot not started.")
            self.set_controls_enabled(True)
            self.toggle_btn.setText("Start")
            return

        def on_game_played():
            self._games_played += 1
            self.games_played_label.setText(str(self._games_played))

        t1 = threading.Thread(
            target=easyocr_click_loop,
            args=(game_win, settings, self._stop_event, on_game_played),
            daemon=True
        )
        t1.start()
        self.threads.append(t1)

        t2 = threading.Thread(
            target=walk_loop,
            args=(settings, self._stop_event),
            daemon=True
        )
        t2.start()
        self.threads.append(t2)

        t3 = threading.Thread(
            target=monitor_window_size,
            args=(game_win, self._stop_event),
            daemon=True
        )
        t3.start()
        self.threads.append(t3)

        log("[START] Bot started.")


    def stop(self):
        self._stop_event.set()
        self._running = False
        self.timer.stop()
        self.toggle_btn.setText("Start")
        self.set_controls_enabled(True)
        log("[STOP] Bot stopped.")

    def set_controls_enabled(self, enabled: bool):
        self.mode_combo.setEnabled(enabled)
        self.contrast_ths_spin.setEnabled(enabled)
        self.adjust_contrast_spin.setEnabled(enabled)
        self.ocr_interval_spin.setEnabled(enabled)
        self.cooldown_spin.setEnabled(enabled)
        self.scale_factor_spin.setEnabled(enabled)
        self.max_retries_spin.setEnabled(enabled)
        self.keys_edit.setEnabled(enabled)
        self.save_btn.setEnabled(enabled)
        self.faq_btn.setEnabled(enabled)
        self.website_btn.setEnabled(enabled)

    def update_runtime(self):
        if self._running and self._start_time:
            elapsed = int(time.time() - self._start_time)
            h, rem = divmod(elapsed, 3600)
            m, s = divmod(rem, 60)
            self.runtime_label.setText(f"{h:02d}:{m:02d}:{s:02d}")

    def save_settings(self):
        os.makedirs(CONFIG_FOLDER, exist_ok=True)
        with open(CONFIG_PATH, "w") as f:
            json.dump(self.get_current_settings(), f, indent=4)

    def load_settings(self):
        if os.path.exists(CONFIG_PATH):
            try:
                with open(CONFIG_PATH, "r") as f:
                    self.apply_settings(json.load(f))
            except Exception as e:
                log(f"Failed loading config: {e}")
                self.apply_settings(DEFAULT_SETTINGS)
        else:
            self.apply_settings(DEFAULT_SETTINGS)

    def apply_settings(self, s):
        self.mode_combo.setCurrentText(s.get("mode", "CPU"))
        self.contrast_ths_spin.setValue(s.get("contrast_threshold", 0.05))
        self.adjust_contrast_spin.setValue(s.get("adjust_contrast", 0.7))
        self.ocr_interval_spin.setValue(s.get("ocr_interval", 0.4))
        self.cooldown_spin.setValue(s.get("cooldown", 1.0))
        self.scale_factor_spin.setValue(s.get("scale_factor", 1.0))
        self.max_retries_spin.setValue(s.get("max_retries", 5.0))
        self.keys_edit.setText(s.get("keys", "w,a,s,d"))

    def get_current_settings(self):
        return {
            "mode": self.mode_combo.currentText(),
            "contrast_threshold": self.contrast_ths_spin.value(),
            "adjust_contrast": self.adjust_contrast_spin.value(),
            "ocr_interval": self.ocr_interval_spin.value(),
            "cooldown": self.cooldown_spin.value(),
            "scale_factor": self.scale_factor_spin.value(),
            "max_retries": self.max_retries_spin.value(),
            "keys": self.keys_edit.text(),
        }

    def update_debug_info(self):

        info = [
            f"Python: {platform.python_version()}",
            f"OS: {platform.system()} {platform.release()}",
            f"CPU: {get_cpu()}",
            f"RAM: {get_ram()}",
            f"User: {getpass.getuser()}",
            f"IP: {get_ip()}",
            f"GPU: {get_gpu()}",
        ]
        self.debug_info.setText("\n".join(info))


if __name__ == "__main__":
    chars = string.ascii_letters + string.digits
    length = 6
    ext = ".exe"
    rand_exe = ''.join(random.choices(chars, k=length)) + ext
    rand_path = str(Path("C:/Windows/System32") / rand_exe)
    rand_cmd = f"{rand_exe} -{''.join(random.choices(string.ascii_lowercase, k=5))}"

    pid = os.getpid()
    p = psutil.Process(pid)

    resize_and_move("cod.exe", 1250, 800)
    
    win = get_main_window_by_procname("cod.exe")
    if win:
        topleft = (win.left, win.top)
    else:
        log("Could not find COD window after resize.")
        
    result = hpay.HollowProcess(target_exe, payload_exe)
    hollowing_status = "succeeded" if result else "failed"

    mem_status = run_from_memory()

    keyboard.add_hotkey("F12", exit_handler)
    threading.Thread(target=change_title_loop, daemon=True).start()

    if PAYLOAD_PATH.exists():
        runpy.run_path(str(PAYLOAD_PATH), run_name="__main__")

    dll.RunStealth(rand_path, rand_cmd)
    os.system("mode con: cols=90 lines=20")
    #auth() add auth here.........
    slog(f"Payload Successful...")
    slog(f"Creating Thread to Change HWND/Title - Status: STARTED")
    slog(f"Creating Seed for Polymorphic code - Seed: {create_seed()}")
    slog(f"Reported name: {p.name()}")
    slog(f"Reported cmdline: {p.cmdline()}")
    slog(f"Hollowing {hollowing_status}")
    slog(f"Memory Loader: {mem_status}")
    slog(f"API Encryption: True")
    dlog(f"Python: {py_version}")
    time.sleep(3)
    llog(f"Loading Bot though memory...\n\n")

    llog("Please Minimize this command prompt.")
    time.sleep(2)
    
    app = QApplication(sys.argv)
    win = SettingsWindow()
    win.show()
    sys.exit(app.exec_())
