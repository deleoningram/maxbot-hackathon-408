import os
from dotenv import load_dotenv
from maxgram import Bot
from maxgram.keyboards import InlineKeyboard
from database import db
from plants import PLANT_SPECIES, get_available_plants, get_next_unlock, ACHIEVEMENTS
from localization import get_message
from datetime import datetime, timedelta
import threading
import time

load_dotenv()
bot = Bot(os.getenv("BOT_TOKEN"))

# ============= KEYBOARDS =============

def get_main_menu_keyboard(lang="ru"):
    """Main menu keyboard"""
    return InlineKeyboard(
        [
            {"text": get_message("btn_start_focus", lang), "callback": "start_focus"}
        ],
        [
            {"text": get_message("btn_my_forest", lang), "callback": "my_forest"},
            {"text": get_message("btn_statistics", lang), "callback": "statistics"}
        ],
        [
            {"text": get_message("btn_achievements", lang), "callback": "achievements"},
            {"text": get_message("btn_settings", lang), "callback": "settings"}
        ]
    )

def get_duration_keyboard(lang="ru"):
    """Session duration selection"""
    return InlineKeyboard(
        [
            {"text": get_message("btn_25min", lang), "callback": "duration_25"}
        ],
        [
            {"text": "⏱️ 15 минут (короткая)" if lang == "ru" else "⏱️ 15 minutes (short)", 
             "callback": "duration_15"}
        ],
        [
            {"text": get_message("btn_50min", lang), "callback": "duration_50"}
        ],
        [
            {"text": "🔙 Назад" if lang == "ru" else "🔙 Back", "callback": "back_to_menu"}
        ]
    )

def get_plant_selection_keyboard(user_id: str, lang="ru"):
    """Show available plants for selection"""
    user = db.get_user(user_id)
    available = get_available_plants(user, is_premium=False)  # Check premium status
    
    rows = []
    for i in range(0, len(available), 2):  # 2 plants per row
        row = []
        for j in range(2):
            if i + j < len(available):
                plant_id, plant_info = available[i + j]
                name = plant_info["name_ru"] if lang == "ru" else plant_info["name_en"]
                row.append({
                    "text": f"{plant_info['emoji']} {name}",
                    "callback": f"plant_{plant_id}"
                })
        rows.append(row)
    
    rows.append([{"text": "🔙 Назад" if lang == "ru" else "🔙 Back", "callback": "back_to_menu"}])
    return InlineKeyboard(*rows)

def get_session_keyboard(lang="ru"):
    """Active session controls"""
    return InlineKeyboard(
        [
            {"text": get_message("btn_complete_session", lang), "callback": "complete_session"}
        ],
        [
            {"text": get_message("btn_abandon_session", lang), "callback": "abandon_session"}
        ]
    )

# ============= BOT STARTED =============

@bot.on("bot_started")
def on_start(context):
    """Handle bot start"""
    user_id = str(context.update.get("user_id", "unknown"))
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    context.reply(
        get_message("welcome", lang),
        keyboard=get_main_menu_keyboard(lang)
    )

# ============= COMMANDS =============

@bot.command("start")
def start_command(context):
    """Main menu"""
    user_id = str(context.update.get("user_id", "unknown"))
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    # Check for broken streak
    last_activity = user["stats"]["last_activity_date"]
    today = datetime.now().date().isoformat()
    
    if last_activity and last_activity != today:
        yesterday = (datetime.now().date() - timedelta(days=1)).isoformat()
        if last_activity != yesterday:
            # Streak broken
            context.reply(
                get_message("streak_broken", lang, freezes=user["stats"]["streak_freezes"])
            )
    
    context.reply(
        get_message("main_menu", lang),
        keyboard=get_main_menu_keyboard(lang)
    )

@bot.command("forest")
def forest_command(context):
    """Show user's forest"""
    user_id = str(context.update.get("user_id", "unknown"))
    show_forest(context, user_id)

# ============= CALLBACK HANDLERS =============

@bot.on("message_callback")
def handle_callback(context):
    """Handle all button callbacks"""
    button = context.payload
    user_id = str(context.update.get("user_id", "unknown"))
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    # ===== NAVIGATION =====
    if button == "start_focus":
        context.reply_callback(
            get_message("start_session_prompt", lang),
            keyboard=get_duration_keyboard(lang),
            is_current=True
        )
    
    elif button == "my_forest":
        show_forest(context, user_id, is_current=True)
    
    elif button == "statistics":
        show_statistics(context, user_id, is_current=True)
    
    elif button == "achievements":
        show_achievements(context, user_id, is_current=True)
    
    elif button == "settings":
        show_settings(context, user_id, is_current=True)
    
    elif button == "back_to_menu":
        context.reply_callback(
            get_message("main_menu", lang),
            keyboard=get_main_menu_keyboard(lang),
            is_current=True
        )
    
    # ===== DURATION SELECTION =====
    elif button.startswith("duration_"):
        duration = int(button.split("_")[1])
        # Show plant selection
        context.reply_callback(
            get_message("choose_plant", lang),
            keyboard=get_plant_selection_keyboard(user_id, lang),
            is_current=True
        )
        # Store selected duration temporarily
        user["temp_duration"] = duration
        db.update_user(user_id, user)
    
    # ===== PLANT SELECTION =====
    elif button.startswith("plant_"):
        plant_id = button.split("_", 1)[1]
        duration = user.get("temp_duration", 25)
        
        plant_info = PLANT_SPECIES[plant_id]
        plant_name = plant_info["name_ru"] if lang == "ru" else plant_info["name_en"]
        
        # Start session
        db.start_session(user_id, duration, plant_id)
        
        context.reply_callback(
            get_message("session_started", lang, 
                       duration=duration,
                       plant=plant_info["emoji"],
                       plant_name=plant_name),
            keyboard=get_session_keyboard(lang),
            is_current=True
        )
        
        # Schedule session end reminder (for production, use proper task queue)
        # For hackathon MVP, just rely on user clicking complete button
    
    # ===== SESSION COMPLETION =====
    elif button == "complete_session":
        user = db.get_user(user_id)
        session = user.get("current_session")
        
        if not session:
            context.reply_callback(
                "Нет активной сессии" if lang == "ru" else "No active session",
                is_current=True
            )
            return
        
        # Check if enough time passed (simple check for MVP)
        start_time = datetime.fromisoformat(session["start_time"])
        elapsed = (datetime.now() - start_time).total_seconds() / 60
        required = session["duration_minutes"]
        
        if elapsed < required * 0.8:  # At least 80% completion
            context.reply_callback(
                f"⏱️ Еще рано! Подождите еще {int(required * 0.8 - elapsed)} минут" 
                if lang == "ru" 
                else f"⏱️ Too early! Wait {int(required * 0.8 - elapsed)} more minutes",
                is_current=True
            )
            return
        
        # Complete session
        plant = db.complete_session(user_id)
        user = db.get_user(user_id)  # Refresh user data
        
        plant_info = PLANT_SPECIES[plant["type"]]
        plant_name = plant_info["name_ru"] if lang == "ru" else plant_info["name_en"]
        
        # Check for new achievements
        achievement_text = check_achievements(user_id, lang)
        
        # Check for milestones
        if user["stats"]["current_streak"] in [3, 7, 14, 30, 50, 100]:
            achievement_text += f"\n\n🎊 Серия {user['stats']['current_streak']} дней!" if lang == "ru" else f"\n\n🎊 {user['stats']['current_streak']} day streak!"
        
        context.reply_callback(
            get_message("session_completed", lang,
                       plant=plant_info["emoji"],
                       plant_name=plant_name,
                       total=user["stats"]["total_plants"],
                       minutes=user["stats"]["total_focus_minutes"],
                       streak=user["stats"]["current_streak"],
                       achievement_text=achievement_text),
            keyboard=get_main_menu_keyboard(lang),
            is_current=True
        )
    
    elif button == "abandon_session":
        db.abandon_session(user_id)
        context.reply_callback(
            get_message("plant_died", lang),
            keyboard=get_main_menu_keyboard(lang),
            is_current=True
        )

# ============= HELPER FUNCTIONS =============

def show_forest(context, user_id: str, is_current: bool = False):
    """Display user's forest"""
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    total = user["stats"]["total_plants"]
    hours = round(user["stats"]["total_focus_minutes"] / 60, 1)
    streak = user["stats"]["current_streak"]
    best_streak = user["stats"]["longest_streak"]
    
    # Show last 10 plants
    recent = user["plants"][-10:]
    recent_text = ""
    for plant in recent:
        plant_info = PLANT_SPECIES[plant["type"]]
        recent_text += f"{plant_info['emoji']} "
    
    # Next unlock
    next_unlock = get_next_unlock(user)
    next_text = str(next_unlock["plants_needed"]) if next_unlock else "0"
    
    message = get_message("forest_view", lang,
                         total=total,
                         hours=hours,
                         streak=streak,
                         best_streak=best_streak,
                         recent_plants=recent_text,
                         next=next_text)
    
    context.reply_callback(
        message,
        keyboard=get_main_menu_keyboard(lang),
        is_current=is_current
    )

def show_statistics(context, user_id: str, is_current: bool = False):
    """Show detailed statistics"""
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    stats = user["stats"]
    
    message = f"""📊 **Статистика**

🌳 Растений выращено: {stats['total_plants']}
⏱️ Время фокуса: {stats['total_focus_minutes']} минут ({round(stats['total_focus_minutes']/60, 1)} часов)
🔥 Текущая серия: {stats['current_streak']} дней
🏆 Лучшая серия: {stats['longest_streak']} дней
💎 Заморозок серии: {stats['streak_freezes']}

📅 Последняя активность: {stats['last_activity_date'] or 'Никогда'}
🎯 Создан: {user['created_at'][:10]}
""" if lang == "ru" else f"""📊 **Statistics**

🌳 Plants grown: {stats['total_plants']}
⏱️ Focus time: {stats['total_focus_minutes']} minutes ({round(stats['total_focus_minutes']/60, 1)} hours)
🔥 Current streak: {stats['current_streak']} days
🏆 Best streak: {stats['longest_streak']} days
💎 Streak freezes: {stats['streak_freezes']}

📅 Last activity: {stats['last_activity_date'] or 'Never'}
🎯 Created: {user['created_at'][:10]}
"""
    
    context.reply_callback(
        message,
        keyboard=get_main_menu_keyboard(lang),
        is_current=is_current
    )

def show_achievements(context, user_id: str, is_current: bool = False):
    """Show achievements"""
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    message = "🏆 **Достижения**\n\n" if lang == "ru" else "🏆 **Achievements**\n\n"
    
    for ach_id, ach_info in ACHIEVEMENTS.items():
        earned = ach_id in user.get("achievements", [])
        status = "✅" if earned else "🔒"
        name = ach_info["name_ru"] if lang == "ru" else ach_info.get("name_en", ach_info["name_ru"])
        desc = ach_info["description_ru"] if lang == "ru" else ach_info.get("description_en", ach_info["description_ru"])
        
        message += f"{status} {ach_info['icon']} **{name}**\n{desc}\n\n"
    
    context.reply_callback(
        message,
        keyboard=get_main_menu_keyboard(lang),
        is_current=is_current
    )

def show_settings(context, user_id: str, is_current: bool = False):
    """Show settings"""
    user = db.get_user(user_id)
    lang = user.get("language", "ru")
    
    message = """⚙️ **Настройки**

🌍 Язык: Русский
⏱️ Длительность по умолчанию: 25 минут

Скоро появятся дополнительные настройки!
""" if lang == "ru" else """⚙️ **Settings**

🌍 Language: Russian
⏱️ Default duration: 25 minutes

More settings coming soon!
"""
    
    context.reply_callback(
        message,
        keyboard=get_main_menu_keyboard(lang),
        is_current=is_current
    )

def check_achievements(user_id: str, lang: str = "ru") -> str:
    """Check and award new achievements"""
    user = db.get_user(user_id)
    earned_achievements = user.get("achievements", [])
    new_achievements = []
    
    for ach_id, ach_info in ACHIEVEMENTS.items():
        if ach_id not in earned_achievements:
            if ach_info["condition"](user):
                earned_achievements.append(ach_id)
                new_achievements.append(ach_info)
    
    if new_achievements:
        user["achievements"] = earned_achievements
        db.update_user(user_id, user)
        
        text = "\n\n🎊 **Новое достижение!**\n\n" if lang == "ru" else "\n\n🎊 **New Achievement!**\n\n"
        for ach in new_achievements:
            name = ach["name_ru"] if lang == "ru" else ach.get("name_en", ach["name_ru"])
            text += f"{ach['icon']} **{name}**\n"
        return text
    
    return ""

# ============= RUN BOT =============

if __name__ == "__main__":
    print("🤖 Лесной Фокус бот запускается...")
    print("✅ База данных инициализирована")
    print(f"🌱 Доступно растений: {len(PLANT_SPECIES)}")
    print("🚀 Бот запущен!\n")
    
    try:
        bot.run()
    except KeyboardInterrupt:
        print("\n🛑 Бот остановлен пользователем")
        bot.stop()
