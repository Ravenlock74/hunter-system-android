import flet as ft
import os
import json
from datetime import datetime

SAVE_FILE = "hunter_data.json"
all_hunters = {}
active_hunter = None

def load_all_hunters():
    global all_hunters
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r', encoding='utf-8') as f:
                loaded = json.load(f)
                if isinstance(loaded, dict): all_hunters = loaded
        except: all_hunters = {}

def save_all_hunters():
    global all_hunters
    try:
        with open(SAVE_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_hunters, f, indent=4)
    except: pass

def dapatkan_rank_dari_level(level):
    if level >= 80: return "S-Rank"
    elif level >= 51: return "A-Rank"
    elif level >= 31: return "B-Rank"
    elif level >= 16: return "C-Rank"
    elif level >= 6: return "D-Rank"
    else: return "E-Rank"

def get_quests_by_rank_and_day(rank_str):
    day = datetime.now().weekday()
    is_weekday = day < 5
    clean_rank = rank_str.replace("-Rank", "").strip()
    
    rank_database = {
        "E": {
            "weekday_str": "10 Push-up, 1 Menit Plank, 10 Squat", "weekend_str": "Lari Minimal 1 KM",
            "weekday_int": "Review materi / Video Learning (10 Menit)", "weekend_int": "Pelajari bahasa asing / skill baru (10 Menit)",
            "weekday_agi": "Speed Typing Test: Capai Minimal 45 WPM", "weekend_agi": "Blind Balance: Berdiri satu kaki, mata tertutup 2 Menit",
            "xp_weekday": 20, "xp_weekend": 30
        },
        "D": {
            "weekday_str": "15 Push-up, 1.5 Menit Plank, 15 Squat", "weekend_str": "Lari Minimal 1.5 KM",
            "weekday_int": "Review materi + catat poin penting (20 Menit)", "weekend_int": "Belajar menyusun kalimat dasar skill baru (15 Menit)",
            "weekday_agi": "Speed Typing Test: Capai Minimal 55 WPM", "weekend_agi": "Blind Balance: Berdiri satu kaki, mata tertutup 3 Menit",
            "xp_weekday": 30, "xp_weekend": 40
        }
    }
    current_pool = rank_database.get(clean_rank, rank_database["E"])
    xp_reward = current_pool["xp_weekday"] if is_weekday else current_pool["xp_weekend"]
    
    return [
        {"id": "q1", "text": current_pool["weekday_str"] if is_weekday else current_pool["weekend_str"], "xp": xp_reward, "stat": "strength"},
        {"id": "q2", "text": current_pool["weekday_int"] if is_weekday else current_pool["weekend_int"], "xp": xp_reward, "stat": "intelligence"},
        {"id": "q3", "text": current_pool["weekday_agi"] if is_weekday else current_pool["weekend_agi"], "xp": xp_reward, "stat": "agility"}
    ]

def main(page: ft.Page):
    page.title = "Hunter System Android"
    page.theme_mode = ft.ThemeMode.DARK
    page.scroll = "adaptive"
    
    load_all_hunters()
    
    def rute_pilih_karakter():
        page.clean()
        page.add(
            ft.Text("⚠️ SYSTEM NOTIFICATION", size=24, weight="bold", color="amber"),
            ft.Text("Silakan pilih Karakter Slot untuk sinkronisasi:", size=14)
        )
        
        lv = ft.ListView(expand=1, spacing=10, padding=20)
        for name, data in all_hunters.items():
            if isinstance(data, dict) and "level" in data:
                def masuk_game(e, n=name):
                    global active_hunter
                    active_hunter = n
                    rute_game_utama()
                lv.controls.append(
                    ft.ElevatedButton(
                        text=f"Slot: {name} | Lv.{data['level']} [{data['rank']}]",
                        on_click=masuk_game,
                        width=400,
                        style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=8))
                    )
                )
        page.add(lv)
        
        def buka_input_nama(e):
            def simpan_nama(ev):
                nama = txt_nama.value.strip().upper()
                if nama and nama not in all_hunters:
                    all_hunters[nama] = {
                        "rank": "E-Rank", "level": 1, "xp": 0, "xp_needed": 100,
                        "strength": 10, "intelligence": 10, "agility": 10,
                        "last_reset_date": datetime.now().strftime("%Y-%m-%d"), 
                        "daily_completed": [], "in_penalty_zone": False
                    }
                    save_all_hunters()
                    dlg.open = False
                    page.update()
                    rute_pilih_karakter()
                    
            txt_nama = ft.TextField(label="Nama Hunter")
            dlg = ft.AlertDialog(
                title=ft.Text("Awaken New Character"),
                content=txt_nama,
                actions=[ft.TextButton("Awaken", on_click=simpan_nama)]
            )
            page.dialog = dlg
            dlg.open = True
            page.update()
            
        page.add(ft.FloatingActionButton(icon=ft.icons.ADD, text="New Character", on_click=buka_input_nama))
        page.update()

    def rute_game_utama():
        page.clean()
        p_data = all_hunters[active_hunter]
        
        # Cek Pergantian Hari 00:00
        sekarang_str = datetime.now().strftime("%Y-%m-%d")
        if p_data.get("last_secret_date") != sekarang_str:
            p_data["last_reset_date"] = sekarang_str
            p_data["daily_completed"] = []
            save_all_hunters()
            
        # UI Header Status
        page.add(
            ft.Text(f"HUNTER: {active_hunter} [{p_data['rank']}]", size=20, weight="bold", color="cyan"),
            ft.Text(f"LEVEL: {p_data['level']} | XP: {p_data['xp']}/{p_data['xp_needed']}", size=14),
            ft.ProgressBar(value=p_data['xp']/p_data['xp_needed'], width=400, color="cyan"),
            ft.Divider(),
            ft.Text("[ DAILY QUESTS ]", size=16, color="amber")
        )
        
        # Render Quest List
        quests = get_quests_by_rank_and_day(p_data["rank"])
        for q in quests:
            is_done = q["id"] in p_data.get("daily_completed", [])
            
            def klaim_reward(e, q_id=q["id"], xp_gain=q["xp"], stat=q["stat"]):
                p_data["daily_completed"].append(q_id)
                p_data["xp"] += xp_gain
                p_data[stat] += 1
                
                # Level Up Logic
                while p_data["xp"] >= p_data["xp_needed"]:
                    p_data["xp"] -= p_data["xp_needed"]
                    p_data["level"] += 1
                    p_data["xp_needed"] = 100 + ((p_data["level"] - 1) * 20)
                    p_data["rank"] = dapatkan_rank_dari_level(p_data["level"])
                    
                save_all_hunters()
                rute_game_utama()

            row = ft.Row(
                controls=[
                    ft.Text(f"[{q['stat'].upper()}] {q['text']} (+{q['xp']} XP)", expand=True),
                    ft.Text("✅ CLAIMED", color="green") if is_done else ft.ElevatedButton("CLAIM", on_click=klaim_reward)
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            page.add(row)
            
        def logout(e):
            rute_pilih_karakter()
            
        page.add(ft.Divider(), ft.ElevatedButton("Switch Character", on_click=logout, color="red"))
        page.update()

    rute_pilih_karakter()

ft.app(target=main)