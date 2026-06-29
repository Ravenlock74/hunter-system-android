from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.progressbar import MDProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.utils import platform
import os
import json
from datetime import datetime

# Ambil lokasi penyimpanan aman untuk Android
if platform == 'android':
    from android.storage import app_storage_details
    SAVE_FILE = os.path.join(app_storage_details().files_dir, "hunter_data.json")
else:
    SAVE_FILE = "hunter_data.json"

KV = '''
MDBoxLayout:
    orientation: 'vertical'
    md_bg_color: 0.1, 0.11, 0.14, 1
    padding: dp(20)
    spacing: dp(15)

    MDLabel:
        text: "⚠️ SYSTEM NOTIFICATION"
        font_style: "H5"
        theme_text_color: "Custom"
        text_color: 1, 0.7, 0, 1
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        id: lbl_status
        text: "HUNTER STATUS LOADING..."
        font_style: "Subtitle1"
        theme_text_color: "Custom"
        text_color: 0, 0.9, 1, 1
        halign: "center"
        size_hint_y: None
        height: self.texture_size[1]

    MDProgressBar:
        id: progress_xp
        value: 0
        max: 1
        size_hint_y: None
        height: dp(8)

    MDLabel:
        text: "[ DAILY QUESTS ]"
        font_style: "Button"
        theme_text_color: "Custom"
        text_color: 1, 0.7, 0, 1

    ScrollView:
        MDBoxLayout:
            id: container_quests
            orientation: 'vertical'
            adaptive_height: True
            spacing: dp(10)
'''

class HunterApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Cyan"
        self.load_data()
        
        # Contoh data default jika baru pertama buka
        if "PLAYER" not in self.all_hunters:
            self.all_hunters["PLAYER"] = {
                "rank": "E-Rank", "level": 1, "xp": 0, "xp_needed": 100,
                "strength": 10, "intelligence": 10, "agility": 10,
                "daily_completed": []
            }
        
        layout = Builder.load_string(KV)
        return layout

    def on_start(self):
        self.update_ui()

    def load_data(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    self.all_hunters = json.load(f)
            except:
                self.all_hunters = {}
        else:
            self.all_hunters = {}

    def save_data(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.all_hunters, f, indent=4)
        except:
            pass

    def update_ui(self):
        p_data = self.all_hunters["PLAYER"]
        
        # Update teks status utama
        self.root.ids.lbl_status.text = (
            f"HUNTER: PLAYER [{p_data['rank']}]\\n"
            f"LEVEL: {p_data['level']} | XP: {p_data['xp']}/{p_data['xp_needed']}\\n\\n"
            f"STR: {p_data['strength']} | INT: {p_data['intelligence']} | AGI: {p_data['agility']}"
        )
        
        # Update progress bar
        self.root.ids.progress_xp.value = p_data['xp'] / p_data['xp_needed']
        
        # Update list quest
        container = self.root.ids.container_quests
        container.clear_widgets()
        
        quests = [
            {"id": "q1", "text": "10 Push-up, 1 Menit Plank, 10 Squat", "xp": 20, "stat": "strength"},
            {"id": "q2", "text": "Review Materi / Video Learning (10 Menit)", "xp": 20, "stat": "intelligence"},
            {"id": "q3", "text": "Speed Typing Test: Capai 45 WPM", "xp": 20, "stat": "agility"}
        ]
        
        for q in quests:
            box = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=48, spacing=10)
            lbl = MDLabel(text=f"[{q['stat'].upper()}] {q['text']}", theme_text_color="Secondary")
            
            if q["id"] in p_data["daily_completed"]:
                btn = MDRaisedButton(text="CLAIMED", md_bg_color=(0, 0.5, 0, 1), disabled=True)
            else:
                btn = MDRaisedButton(text="CLAIM", on_release=lambda x, quest=q: self.claim_quest(quest))
                
            box.add_widget(lbl)
            box.add_widget(btn)
            container.add_widget(box)

    def claim_quest(self, quest):
        p_data = self.all_hunters["PLAYER"]
        p_data["daily_completed"].append(quest["id"])
        p_data["xp"] += quest["xp"]
        p_data[quest["stat"]] += 1
        
        # Logika Level Up
        while p_data["xp"] >= p_data["xp_needed"]:
            p_data["xp"] -= p_data["xp_needed"]
            p_data["level"] += 1
            p_data["xp_needed"] = 100 + ((p_data["level"] - 1) * 20)
            
            # Update Rank
            lv = p_data["level"]
            if lv >= 80: p_data["rank"] = "S-Rank"
            elif lv >= 51: p_data["rank"] = "A-Rank"
            elif lv >= 31: p_data["rank"] = "B-Rank"
            elif lv >= 16: p_data["rank"] = "C-Rank"
            elif lv >= 6: p_data["rank"] = "D-Rank"
            else: p_data["rank"] = "E-Rank"
            
        self.save_data()
        self.update_ui()

if __name__ == '__main__':
    HunterApp().run()
Langkah 2: Ganti Isi File build.yml dengan Docker Buildozer (Stabil & Anti-Gagal)
Masuk ke folder .github/workflows/build.yml di GitHub kamu.

Klik tombol Edit (ikon pensil).

Ganti seluruh isinya dengan skrip otomatis yang memanfaatkan Docker Container resmi dari Buildozer ini:

YAML
name: Build Android APK Stable

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v4

      - name: Build APK with Buildozer Docker
        uses: jasonmccallister/buildozer-action@v1
        with:
          command: 'buildozer android debug'
          repository_root: '.'

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: hunter-app-apk
          path: .id/bin/*.apk
