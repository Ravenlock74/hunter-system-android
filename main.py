"""
HUNTER SYSTEM - Android (KivyMD) version
Logic ported 1:1 from the original customtkinter desktop script.
Layout redesigned as a single scrollable column (mobile-friendly),
instead of the desktop's left/right split panels.
"""
 
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
from kivy.uix.screenmanager import ScreenManager
from kivymd.uix.fitimage import FitImage
 
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.card import MDCard
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
 
import os
import json
from datetime import datetime
 
# ---------------------------------------------------------------------------
# FILE CONFIGURATION (Android-safe storage path)
# ---------------------------------------------------------------------------
if platform == "android":
    from android.storage import app_storage_path
    SAVE_FILE = os.path.join(app_storage_path(), "hunter_data.json")
else:
    SAVE_FILE = "hunter_data.json"
 
# ---------------------------------------------------------------------------
# BACKGROUND IMAGE
# ---------------------------------------------------------------------------
# Ganti "bg.jpg" dengan nama file foto kamu (taruh di folder yang sama dengan main.py)
BG_IMAGE_FILE = "bg.jpg"
 
_bg_candidate = os.path.join(os.path.dirname(os.path.abspath(__file__)), BG_IMAGE_FILE)
BG_IMAGE_PATH = _bg_candidate if os.path.exists(_bg_candidate) else ""
 
# ---------------------------------------------------------------------------
# COLOR PALETTE
# ---------------------------------------------------------------------------
COL_BG = (0.05, 0.06, 0.08, 1)
COL_CARD = (0.11, 0.12, 0.16, 1)
COL_CARD_ALT = (0.13, 0.15, 0.20, 1)
COL_CYAN = (0, 0.9, 1, 1)
COL_AMBER = (1, 0.7, 0, 1)
COL_RED = (0.86, 0.21, 0.27, 1)
COL_GREY = (0.55, 0.55, 0.55, 1)
COL_DARKGREY = (0.18, 0.19, 0.24, 1)
 
# ---------------------------------------------------------------------------
# KV LAYOUT
# ---------------------------------------------------------------------------
KV = """
ScreenManager:
    SelectionScreen:
    GameScreen:
 
 
<SelectionScreen>:
    name: "selection"
 
    FloatLayout:
 
        FitImage:
            source: app.BG_IMAGE if app.BG_IMAGE else ""
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}
            allow_stretch: True
            keep_ratio: False
            opacity: 1 if app.BG_IMAGE else 0
 
        MDBoxLayout:
            size_hint: 1, 1
            md_bg_color: 0, 0, 0, 0.62 if app.BG_IMAGE else 1
 
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: 0, 0, 0, 0
            padding: dp(20)
            spacing: dp(10)
 
        MDLabel:
            text: "[ THE SYSTEM: HUNTER REGISTRY ]"
            font_style: "H6"
            bold: True
            theme_text_color: "Custom"
            text_color: app.COL_AMBER
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
 
        MDLabel:
            text: "Pilih karakter untuk memulai sinkronisasi"
            theme_text_color: "Custom"
            text_color: app.COL_GREY
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]
 
        ScrollView:
            MDBoxLayout:
                id: hunter_list
                orientation: "vertical"
                adaptive_height: True
                spacing: dp(8)
                padding: dp(2)
 
        MDRaisedButton:
            text: "+ AWAKEN NEW CHARACTER"
            md_bg_color: app.COL_CYAN
            text_color: 0.05, 0.05, 0.05, 1
            size_hint_x: 1
            height: dp(46)
            on_release: app.open_new_character_dialog()
 
 
<GameScreen>:
    name: "game"
 
    FloatLayout:
 
        FitImage:
            source: app.BG_IMAGE if app.BG_IMAGE else ""
            size_hint: 1, 1
            pos_hint: {"x": 0, "y": 0}
            allow_stretch: True
            keep_ratio: False
            opacity: 1 if app.BG_IMAGE else 0
 
        MDBoxLayout:
            size_hint: 1, 1
            md_bg_color: 0, 0, 0, 0.62 if app.BG_IMAGE else 1
 
        MDBoxLayout:
            orientation: "vertical"
            md_bg_color: 0, 0, 0, 0
 
            MDTopAppBar:
            id: topbar
            title: "HUNTER SYSTEM"
            md_bg_color: app.COL_CARD
            specific_text_color: app.COL_CYAN
            left_action_items: [["arrow-left", lambda x: app.kembali_ke_menu_seleksi()]]
            right_action_items: [["delete", lambda x: app.handler_hapus_akun()]]
 
        ScrollView:
            MDBoxLayout:
                id: game_body
                orientation: "vertical"
                adaptive_height: True
                padding: dp(16)
                spacing: dp(18)
 
                # ---------- STATUS CARD ----------
                MDCard:
                    orientation: "vertical"
                    md_bg_color: 0.11, 0.12, 0.16, 0.82
                    radius: [12]
                    padding: dp(16)
                    spacing: dp(6)
                    adaptive_height: True
 
                    MDLabel:
                        id: lbl_clock
                        text: "00:00:00"
                        font_style: "H5"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.COL_CYAN
                        halign: "center"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_date
                        text: "Date Loading..."
                        theme_text_color: "Custom"
                        text_color: app.COL_GREY
                        halign: "center"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_profile
                        text: "HUNTER: --"
                        bold: True
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_level
                        text: "LEVEL: 1"
                        bold: True
                        theme_text_color: "Custom"
                        text_color: app.COL_AMBER
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_xp_text
                        text: "XP: 0 / 100"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDProgressBar:
                        id: xp_bar
                        value: 0
                        max: 100
                        size_hint_y: None
                        height: dp(8)
 
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(1)
                        md_bg_color: 0.25, 0.25, 0.25, 1
 
                    MDLabel:
                        id: lbl_str
                        text: "STR (Strength): --"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_int
                        text: "INT (Intelligence): --"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDLabel:
                        id: lbl_agi
                        text: "AGI (Agility): --"
                        font_style: "Caption"
                        size_hint_y: None
                        height: self.texture_size[1]
 
                # ---------- DAILY QUESTS ----------
                MDLabel:
                    text: "[ DAILY QUESTS ]"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app.COL_AMBER
                    size_hint_y: None
                    height: self.texture_size[1]
 
                MDLabel:
                    id: reset_info
                    text: "Quest baru otomatis diperbarui pukul 00:00 tengah malam."
                    font_style: "Caption"
                    theme_text_color: "Custom"
                    text_color: app.COL_GREY
                    text_size: self.width, None
                    size_hint_y: None
                    height: self.texture_size[1]
 
                MDBoxLayout:
                    id: daily_list
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(8)
 
                # ---------- SIDE QUESTS ----------
                MDLabel:
                    text: "[ SIDE QUESTS ] - Tugas Kustom Hari Ini"
                    bold: True
                    theme_text_color: "Custom"
                    text_color: app.COL_CYAN
                    size_hint_y: None
                    height: self.texture_size[1]
 
                MDCard:
                    orientation: "vertical"
                    md_bg_color: 0.13, 0.15, 0.20, 0.82
                    radius: [10]
                    padding: dp(12)
                    spacing: dp(10)
                    adaptive_height: True
 
                    MDTextField:
                        id: quest_input
                        hint_text: "Nama Tugas (Fixed: +20 EXP)..."
                        mode: "rectangle"
 
                    MDLabel:
                        text: "Pilih kategori stat:"
                        font_style: "Caption"
                        theme_text_color: "Custom"
                        text_color: app.COL_GREY
                        size_hint_y: None
                        height: self.texture_size[1]
 
                    MDBoxLayout:
                        size_hint_y: None
                        height: dp(40)
                        spacing: dp(8)
 
                        MDRaisedButton:
                            id: btn_stat_str
                            text: "STR"
                            md_bg_color: app.COL_DARKGREY
                            on_release: app.select_stat("strength")
 
                        MDRaisedButton:
                            id: btn_stat_int
                            text: "INT"
                            md_bg_color: app.COL_CYAN
                            text_color: 0.05, 0.05, 0.05, 1
                            on_release: app.select_stat("intelligence")
 
                        MDRaisedButton:
                            id: btn_stat_agi
                            text: "AGI"
                            md_bg_color: app.COL_DARKGREY
                            on_release: app.select_stat("agility")
 
                    MDRaisedButton:
                        text: "+ ADD QUEST"
                        md_bg_color: app.COL_CYAN
                        text_color: 0.05, 0.05, 0.05, 1
                        size_hint_x: 1
                        height: dp(44)
                        on_release: app.add_custom_quest()
 
                MDBoxLayout:
                    id: custom_list
                    orientation: "vertical"
                    adaptive_height: True
                    spacing: dp(8)
 
                MDBoxLayout:
                    size_hint_y: None
                    height: dp(20)
"""
 
 
class SelectionScreen(MDScreen):
    pass
 
 
class GameScreen(MDScreen):
    pass
 
 
class HunterApp(MDApp):
 
    # background image path (exposed to KV via app.BG_IMAGE)
    BG_IMAGE = BG_IMAGE_PATH
 
    # expose colors to KV via `app.COL_xxx`
    COL_BG = COL_BG
    COL_CARD = COL_CARD
    COL_CARD_ALT = COL_CARD_ALT
    COL_CYAN = COL_CYAN
    COL_AMBER = COL_AMBER
    COL_RED = COL_RED
    COL_GREY = COL_GREY
    COL_DARKGREY = COL_DARKGREY
 
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
 
        self.all_hunters = {}
        self.active_hunter = None
        self.selected_stat = "intelligence"
        self._clock_event = None
        self._new_char_dialog = None
        self._generic_dialog = None
 
        self.load_all_hunters()
        self.sm = Builder.load_string(KV)
        return self.sm
 
    def on_start(self):
        self.refresh_selection_screen()
 
    # -----------------------------------------------------------------
    # PERSISTENCE
    # -----------------------------------------------------------------
    def load_all_hunters(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self.all_hunters = loaded if isinstance(loaded, dict) else {}
            except Exception:
                self.all_hunters = {}
        else:
            self.all_hunters = {}
 
    def save_all_hunters(self):
        try:
            with open(SAVE_FILE, "w", encoding="utf-8") as f:
                json.dump(self.all_hunters, f, indent=4)
        except Exception as e:
            print(f"Gagal menyimpan database: {e}")
 
    # -----------------------------------------------------------------
    # RANK / QUEST RULES (identical to the desktop version)
    # -----------------------------------------------------------------
    @staticmethod
    def dapatkan_rank_dari_level(level):
        if level >= 80:
            return "S-Rank"
        elif level >= 51:
            return "A-Rank"
        elif level >= 31:
            return "B-Rank"
        elif level >= 16:
            return "C-Rank"
        elif level >= 6:
            return "D-Rank"
        else:
            return "E-Rank"
 
    @staticmethod
    def get_quests_by_rank_and_day(rank_str):
        day = datetime.now().weekday()
        is_weekday = day < 5
        clean_rank = rank_str.replace("-Rank", "").strip()
 
        rank_database = {
            "E": {
                "weekday_str": "10 Push-up, 1 Menit Plank, 10 Squat", "weekend_str": "Lari Minimal 1 KM",
                "weekday_int": "Review materi / Video Learning (10 Menit)", "weekend_int": "Pelajari bahasa asing / skill baru (10 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 45 WPM", "weekend_agi": "Blind Balance: Berdiri satu kaki, mata tertutup 2 Menit",
                "xp_weekday": 20, "xp_weekend": 30,
            },
            "D": {
                "weekday_str": "15 Push-up, 1.5 Menit Plank, 15 Squat", "weekend_str": "Lari Minimal 1.5 KM",
                "weekday_int": "Review materi + catat poin penting (20 Menit)", "weekend_int": "Belajar menyusun kalimat dasar skill baru (15 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 55 WPM", "weekend_agi": "Blind Balance: Berdiri satu kaki, mata tertutup 3 Menit",
                "xp_weekday": 30, "xp_weekend": 40,
            },
            "C": {
                "weekday_str": "20 Push-up, 2 Menit Plank, 20 Squat", "weekend_str": "Lari Minimal 2 KM",
                "weekday_int": "Latihan soal kuliah / studi kasus software (30 Menit)", "weekend_int": "Mendengarkan audio-listening asing (20 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 65 WPM", "weekend_agi": "Blind Balance: Berdiri satu kaki, mata tertutup 4 Menit",
                "xp_weekday": 40, "xp_weekend": 50,
            },
            "B": {
                "weekday_str": "30 Push-up, 2.5 Menit Plank, 30 Squat", "weekend_str": "Lari Minimal 3 KM",
                "weekday_int": "Belajar materi kuliah esok hari / simulasi software (45 Menit)", "weekend_int": "Membaca artikel bahasa asing (30 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 75 WPM", "weekend_agi": "Reflex Training: Tangkap bola tenis cepat 5 Menit",
                "xp_weekday": 50, "xp_weekend": 65,
            },
            "A": {
                "weekday_str": "40 Push-up, 3 Menit Plank, 40 Squat", "weekend_str": "Lari Minimal 4 KM",
                "weekday_int": "Persiapan ujian intensif / menyusun draf laporan (60 Menit)", "weekend_int": "Percakapan aktif bahasa asing (45 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 85 WPM", "weekend_agi": "Reflex Training: Tangkap bola tenis cepat 10 Menit",
                "xp_weekday": 65, "xp_weekend": 80,
            },
            "S": {
                "weekday_str": "50 Push-up, 3.5 Menit Plank, 50 Squat", "weekend_str": "Lari Minimal 5 KM",
                "weekday_int": "Penguasaan materi & penyelesaian proyek rumit (90 Menit)", "weekend_int": "Fasih menganalisis dokumen asing (60 Menit)",
                "weekday_agi": "Speed Typing Test: Capai Minimal 95+ WPM", "weekend_agi": "God-like Reflexes: Kombinasi fisik tingkat lanjut (15 Menit)",
                "xp_weekday": 80, "xp_weekend": 100,
            },
        }
 
        pool = rank_database.get(clean_rank, rank_database["E"])
        xp_reward = pool["xp_weekday"] if is_weekday else pool["xp_weekend"]
 
        return [
            {"id": "q1", "text": pool["weekday_str"] if is_weekday else pool["weekend_str"], "xp": xp_reward, "stat": "strength"},
            {"id": "q2", "text": pool["weekday_int"] if is_weekday else pool["weekend_int"], "xp": xp_reward, "stat": "intelligence"},
            {"id": "q3", "text": pool["weekday_agi"] if is_weekday else pool["weekend_agi"], "xp": xp_reward, "stat": "agility"},
        ]
 
    # -----------------------------------------------------------------
    # GENERIC DIALOG HELPER
    # -----------------------------------------------------------------
    def show_dialog(self, title, text):
        dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDFlatButton(text="OK", theme_text_color="Custom",
                             text_color=COL_CYAN,
                             on_release=lambda x: dialog.dismiss())
            ],
        )
        dialog.open()
 
    # -----------------------------------------------------------------
    # SELECTION SCREEN
    # -----------------------------------------------------------------
    def refresh_selection_screen(self):
        self.load_all_hunters()
        screen = self.sm.get_screen("selection")
        container = screen.ids.hunter_list
        container.clear_widgets()
 
        if not self.all_hunters:
            container.add_widget(
                MDLabel(
                    text="[ Tidak ada data Hunter terdaftar ]",
                    theme_text_color="Custom",
                    text_color=COL_GREY,
                    halign="center",
                    size_hint_y=None,
                    height="60dp",
                )
            )
            return
 
        for name, data in self.all_hunters.items():
            if isinstance(data, dict) and "level" in data:
                btn = MDRaisedButton(
                    text=f"Slot: {name}  |  Lv.{data['level']} [{data['rank']}]",
                    md_bg_color=COL_CARD_ALT,
                    size_hint_x=1,
                    height="48dp",
                )
                btn.bind(on_release=lambda inst, n=name: self.pilih_karakter_dan_masuk(n))
                container.add_widget(btn)
 
    def open_new_character_dialog(self):
        text_field = MDTextField(hint_text="Ketik nama hunter baru...")
        self._new_char_dialog = MDDialog(
            title="NEW AWAKENING",
            type="custom",
            content_cls=text_field,
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: self._new_char_dialog.dismiss()),
                MDFlatButton(
                    text="AWAKEN NOW",
                    theme_text_color="Custom",
                    text_color=COL_CYAN,
                    on_release=lambda x: self.buat_karakter_baru(text_field.text),
                ),
            ],
        )
        self._new_char_dialog.open()
 
    def buat_karakter_baru(self, nama_input):
        nama_bersih = (nama_input or "").strip().upper()
        if not nama_bersih:
            self.show_dialog("SYSTEM", "Nama tidak boleh kosong!")
            return
        if nama_bersih in self.all_hunters:
            self.show_dialog("SYSTEM", "Nama Hunter ini sudah terdaftar!")
            return
 
        self.all_hunters[nama_bersih] = {
            "rank": "E-Rank", "level": 1, "xp": 0, "xp_needed": 100,
            "strength": 10, "intelligence": 10, "agility": 10,
            "last_reset_date": datetime.now().strftime("%Y-%m-%d"),
            "daily_completed": [],
            "custom_quests": [],
            "in_penalty_zone": False,
        }
        self.save_all_hunters()
        if self._new_char_dialog:
            self._new_char_dialog.dismiss()
        self.refresh_selection_screen()
 
    def pilih_karakter_dan_masuk(self, nama):
        self.load_all_hunters()
        self.active_hunter = nama
        p_data = self.all_hunters[nama]
 
        self.eksekusi_pengecekan_hari(p_data, datetime.now())
 
        self.sm.get_screen("game").ids.topbar.title = f"SYSTEM: {nama}"
        self.sm.current = "game"
 
        self.muat_ulang_papan_daily_quest()
        self.muat_ulang_side_quests()
        self.update_ui_display()
 
        if not self._clock_event:
            self._clock_event = Clock.schedule_interval(self.update_clock, 1)
 
    def kembali_ke_menu_seleksi(self):
        self.active_hunter = None
        self.sm.current = "selection"
        self.refresh_selection_screen()
 
    def handler_hapus_akun(self):
        if not self.active_hunter:
            return
        nama = self.active_hunter
 
        def confirm_delete(*_):
            self.all_hunters.pop(nama, None)
            self.save_all_hunters()
            confirm_dialog.dismiss()
            self.show_dialog("SYSTEM", "Data akun berhasil dihapus.")
            self.kembali_ke_menu_seleksi()
 
        confirm_dialog = MDDialog(
            title="SYSTEM WARNING",
            text=f"Hapus karakter [{nama}] secara permanen?\nTindakan ini tidak bisa dibatalkan!",
            buttons=[
                MDFlatButton(text="BATAL", on_release=lambda x: confirm_dialog.dismiss()),
                MDFlatButton(text="HAPUS", theme_text_color="Custom",
                             text_color=COL_RED, on_release=confirm_delete),
            ],
        )
        confirm_dialog.open()
 
    # -----------------------------------------------------------------
    # XP / LEVEL LOGIC
    # -----------------------------------------------------------------
    def gain_xp(self, amount, stat_type):
        p_data = self.all_hunters[self.active_hunter]
        p_data["xp"] += amount
        if stat_type:
            p_data[stat_type] += 1
 
        leveled_up = False
        while p_data["xp"] >= p_data["xp_needed"]:
            p_data["xp"] -= p_data["xp_needed"]
            p_data["level"] += 1
            p_data["xp_needed"] = 100 + ((p_data["level"] - 1) * 20)
            p_data["rank"] = self.dapatkan_rank_dari_level(p_data["level"])
            leveled_up = True
 
        if leveled_up:
            self.show_dialog(
                "SYSTEM NOTIFICATION",
                f"\u2605 LEVEL UP! \u2605\nAnda naik ke Level {p_data['level']}!\nRank Anda: {p_data['rank']}",
            )
 
        self.update_ui_display()
        self.save_all_hunters()
 
    def kurangi_xp_dengan_penalti(self, p_data, total_penalti):
        p_data["xp"] -= total_penalti
        while p_data["xp"] < 0:
            if p_data["level"] <= 1:
                p_data["xp"] = 0
                break
            p_data["level"] -= 1
            p_data["xp_needed"] = 100 + ((p_data["level"] - 1) * 20)
            p_data["xp"] = p_data["xp_needed"] + p_data["xp"]
            p_data["rank"] = self.dapatkan_rank_dari_level(p_data["level"])
 
            self.show_dialog(
                "LEVEL DEGRADED",
                f"SYSTEM PENALTY CONSEQUENCE\n\n"
                f"XP Anda defisit! Level Anda TURUN ke Level {p_data['level']}!\n"
                f"Rank Anda saat ini: {p_data['rank']}",
            )
 
    def eksekusi_pengecekan_hari(self, p_data, sekarang):
        hari_sekarang_str = sekarang.strftime("%Y-%m-%d")
        active_pool = self.get_quests_by_rank_and_day(p_data["rank"])
 
        if p_data.get("last_reset_date") != hari_sekarang_str:
            quest_selesai = p_data.get("daily_completed", [])
            jumlah_gagal = len(active_pool) - len(quest_selesai)
 
            if jumlah_gagal > 0 and not p_data.get("in_penalty_zone", False):
                total_penalti = jumlah_gagal * 10
                p_data["in_penalty_zone"] = True
                self.show_dialog(
                    "SYSTEM ALARM: PERGANTIAN HARI (00:00)",
                    f"WAKTU HABIS! HARI TELAH BERGANTI!\n\n"
                    f"Anda menyisakan {jumlah_gagal} Daily Quest dari hari kemarin!\n"
                    f"Hukuman Tahap 1: -{total_penalti} EXP diterapkan.\n"
                    f"Hukuman Tahap 2: Anda dipindahkan ke Penalty Zone!",
                )
                self.kurangi_xp_dengan_penalti(p_data, total_penalti)
            else:
                if not p_data.get("in_penalty_zone", False):
                    self.show_dialog(
                        "SYSTEM NOTIFICATION",
                        "Hari telah berganti! Semua quest kemarin aman. Quest Board diperbarui!",
                    )
 
            p_data["last_reset_date"] = hari_sekarang_str
            if not p_data["in_penalty_zone"]:
                p_data["daily_completed"] = []
 
            self.save_all_hunters()
            return True
        return False
 
    # -----------------------------------------------------------------
    # UI REFRESH
    # -----------------------------------------------------------------
    def update_ui_display(self):
        if not self.active_hunter:
            return
        p_data = self.all_hunters[self.active_hunter]
        ids = self.sm.get_screen("game").ids
 
        ids.lbl_profile.text = f"HUNTER: {self.active_hunter} ({p_data['rank']})"
        ids.lbl_level.text = f"LEVEL: {p_data['level']}"
        ids.lbl_xp_text.text = f"XP: {p_data['xp']} / {p_data['xp_needed']}"
        ids.xp_bar.value = (p_data["xp"] / p_data["xp_needed"] * 100) if p_data["xp_needed"] > 0 else 0
        ids.lbl_str.text = f"STR (Strength): {p_data['strength']}"
        ids.lbl_int.text = f"INT (Intelligence): {p_data['intelligence']}"
        ids.lbl_agi.text = f"AGI (Agility): {p_data['agility']}"
 
    def update_clock(self, dt):
        if self.sm.current != "game" or not self.active_hunter:
            return
        ids = self.sm.get_screen("game").ids
        sekarang = datetime.now()
        ids.lbl_clock.text = sekarang.strftime("%H:%M:%S")
        ids.lbl_date.text = sekarang.strftime("%A, %d %B %Y")
 
        p_data = self.all_hunters[self.active_hunter]
        if self.eksekusi_pengecekan_hari(p_data, sekarang):
            self.muat_ulang_papan_daily_quest()
            self.update_ui_display()
 
    # -----------------------------------------------------------------
    # QUEST ROWS
    # -----------------------------------------------------------------
    def create_quest_row(self, parent, quest_data, is_daily=True, quest_id=None,
                          is_penalty=False, is_claimed=False):
        row = MDCard(
            orientation="horizontal",
            md_bg_color=COL_CARD_ALT if not is_penalty else (0.25, 0.08, 0.08, 1),
            radius=[8],
            padding="10dp",
            spacing="8dp",
            adaptive_height=True,
        )
 
        prefix = "[PENALTY]" if is_penalty else f"[{quest_data['stat'].upper()}]"
        info_teks = f"{prefix} {quest_data['text']} (+{quest_data['xp']} EXP)"
 
        lbl = MDLabel(
            text=info_teks,
            theme_text_color="Custom",
            text_color=COL_GREY if is_claimed else (COL_RED if is_penalty else (1, 1, 1, 1)),
            text_size=(None, None),
            size_hint_x=0.7,
        )
        lbl.bind(width=lambda inst, w: setattr(inst, "text_size", (w, None)))
        lbl.bind(texture_size=lambda inst, ts: setattr(row, "height", max(ts[1] + 24, 48)))
        row.add_widget(lbl)
 
        if is_claimed:
            row.add_widget(
                MDLabel(text="\u2705 CLAIMED", theme_text_color="Custom",
                        text_color=COL_CYAN, size_hint_x=0.3, halign="right")
            )
        else:
            def complete_action(*_):
                p_data = self.all_hunters[self.active_hunter]
                if is_penalty:
                    p_data["in_penalty_zone"] = False
                    p_data["daily_completed"] = []
                    self.save_all_hunters()
                    self.show_dialog("PENALTY CLEARED",
                                      "Hukuman selesai! Akses Daily Quest dipulihkan.")
                    self.gain_xp(quest_data["xp"], None)
                    self.muat_ulang_papan_daily_quest()
                else:
                    if is_daily:
                        p_data["daily_completed"].append(quest_id)
                        self.save_all_hunters()
                        self.gain_xp(quest_data["xp"], quest_data["stat"])
                        self.muat_ulang_papan_daily_quest()
                    else:
                        self.show_dialog("QUEST REWARD",
                                          f"Side Quest selesai!\nReward: +{quest_data['xp']} EXP!")
                        self.gain_xp(quest_data["xp"], quest_data["stat"])
                        if row.parent:
                            row.parent.remove_widget(row)
 
            btn = MDRaisedButton(
                text="CLAIM",
                size_hint_x=0.3,
                md_bg_color=COL_RED if is_penalty else COL_CYAN,
                text_color=(1, 1, 1, 1) if is_penalty else (0.05, 0.05, 0.05, 1),
            )
            btn.bind(on_release=complete_action)
            row.add_widget(btn)
 
        parent.add_widget(row)
 
    def muat_ulang_papan_daily_quest(self):
        if not self.active_hunter:
            return
        screen = self.sm.get_screen("game")
        container = screen.ids.daily_list
        container.clear_widgets()
 
        p_data = self.all_hunters[self.active_hunter]
 
        if p_data.get("in_penalty_zone", False):
            screen.ids.reset_info.text = "PENALTY ZONE AKTIF. Selesaikan hukuman Anda!"
            screen.ids.reset_info.text_color = COL_RED
            penalty_quest = {"text": "Belajar Bahasa Mandarin 20 Menit", "xp": 20, "stat": "intelligence"}
            self.create_quest_row(container, penalty_quest, is_daily=False, is_penalty=True)
        else:
            screen.ids.reset_info.text = "Quest baru otomatis diperbarui pukul 00:00 tengah malam."
            screen.ids.reset_info.text_color = COL_GREY
            active_pool = self.get_quests_by_rank_and_day(p_data["rank"])
            completed = p_data.get("daily_completed", [])
 
            if len(completed) >= len(active_pool):
                container.add_widget(
                    MDLabel(
                        text="[OK] SEMUA QUEST HARI INI TELAH DIKERJAKAN!",
                        bold=True,
                        theme_text_color="Custom",
                        text_color=COL_AMBER,
                        halign="center",
                        size_hint_y=None,
                        height="80dp",
                    )
                )
            else:
                for q in active_pool:
                    is_claimed = q["id"] in completed
                    self.create_quest_row(container, q, is_daily=True,
                                           quest_id=q["id"], is_claimed=is_claimed)
 
    # -----------------------------------------------------------------
    # SIDE / CUSTOM QUEST
    # -----------------------------------------------------------------
    def select_stat(self, stat_name):
        self.selected_stat = stat_name
        screen = self.sm.get_screen("game")
        buttons = {
            "strength": screen.ids.btn_stat_str,
            "intelligence": screen.ids.btn_stat_int,
            "agility": screen.ids.btn_stat_agi,
        }
        for name, btn in buttons.items():
            if name == stat_name:
                btn.md_bg_color = COL_CYAN
                btn.text_color = (0.05, 0.05, 0.05, 1)
            else:
                btn.md_bg_color = COL_DARKGREY
                btn.text_color = (1, 1, 1, 1)
 
    def add_custom_quest(self):
        screen = self.sm.get_screen("game")
        quest_text = screen.ids.quest_input.text.strip()
        if not quest_text:
            self.show_dialog("SYSTEM WARNING", "Nama Side Quest tidak boleh kosong!")
            return
 
        new_quest = {"text": quest_text, "xp": 20, "stat": self.selected_stat}
 
        # Simpan ke profil aktif
        p_data = self.all_hunters[self.active_hunter]
        if "custom_quests" not in p_data:
            p_data["custom_quests"] = []
        p_data["custom_quests"].append(new_quest)
        self.save_all_hunters()
 
        self.muat_ulang_side_quests()
        screen.ids.quest_input.text = ""
 
    def muat_ulang_side_quests(self):
        if not self.active_hunter:
            return
        screen = self.sm.get_screen("game")
        container = screen.ids.custom_list
        container.clear_widgets()
 
        p_data = self.all_hunters[self.active_hunter]
        for i, q in enumerate(p_data.get("custom_quests", [])):
            self.create_quest_row(container, q, is_daily=False, quest_id=i)
 
 
if __name__ == "__main__":
    HunterApp().run()
