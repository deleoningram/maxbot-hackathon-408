MESSAGES = {
    # Welcome & Start
    "welcome": {
        "ru": "🌱 Добро пожаловать в Лесной Фокус!\n\nЯ помогу вам сосредоточиться на работе и вырастить виртуальный лес. Каждая сессия концентрации выращивает новое растение.\n\nИспользуйте /start чтобы увидеть меню.",
        "en": "🌱 Welcome to Forest Focus!\n\nI'll help you stay focused and grow a virtual forest. Each focus session grows a new plant.\n\nUse /start to see the menu."
    },
    
    "main_menu": {
        "ru": "🌳 **Главное меню**\n\nВыберите действие:",
        "en": "🌳 **Main Menu**\n\nChoose an action:"
    },
    
    # Session Management
    "start_session_prompt": {
        "ru": "⏱️ **Начать сессию фокуса**\n\nВыберите длительность:",
        "en": "⏱️ **Start Focus Session**\n\nChoose duration:"
    },
    
    "choose_plant": {
        "ru": "🌱 **Выберите растение для выращивания**\n\nДоступные растения:",
        "en": "🌱 **Choose Plant to Grow**\n\nAvailable plants:"
    },
    
    "session_started": {
        "ru": "🌱 **Сессия началась!**\n\n⏱️ Длительность: {duration} минут\n🌿 Растение: {plant}\n\n💡 Сосредоточьтесь на работе. Если вы покинете бот, растение погибнет!\n\nЗавершите сессию через {duration} минут кнопкой ниже.",
        "en": "🌱 **Session Started!**\n\n⏱️ Duration: {duration} minutes\n🌿 Plant: {plant}\n\n💡 Stay focused. If you leave, your plant will die!\n\nComplete session in {duration} minutes using button below."
    },
    
    "session_completed": {
        "ru": "🎉 **Отличная работа!**\n\n✅ Сессия завершена\n{plant} **{plant_name}** вырос в вашем лесу!\n\n📊 Статистика:\n🌳 Всего растений: {total}\n⏱️ Время фокуса: {minutes} мин\n🔥 Серия: {streak} дней\n\n{achievement_text}",
        "en": "🎉 **Great Work!**\n\n✅ Session completed\n{plant} **{plant_name}** grew in your forest!\n\n📊 Stats:\n🌳 Total plants: {total}\n⏱️ Focus time: {minutes} min\n🔥 Streak: {streak} days\n\n{achievement_text}"
    },
    
    "plant_died": {
        "ru": "😢 **Растение погибло...**\n\nВы покинули сессию раньше времени. Попробуйте снова!",
        "en": "😢 **Plant Died...**\n\nYou left the session early. Try again!"
    },
    
    # Statistics
    "forest_view": {
        "ru": "🌲 **Ваш лес**\n\n🌳 Растений выращено: {total}\n⏱️ Часов фокуса: {hours}\n🔥 Текущая серия: {streak} дней\n🏆 Лучшая серия: {best_streak} дней\n\n{recent_plants}\n\n💡 Следующее растение откроется через {next} растений",
        "en": "🌲 **Your Forest**\n\n🌳 Plants grown: {total}\n⏱️ Focus hours: {hours}\n🔥 Current streak: {streak} days\n🏆 Best streak: {best_streak} days\n\n{recent_plants}\n\n💡 Next plant unlocks in {next} plants"
    },
    
    # Streak
    "streak_broken": {
        "ru": "💔 **Серия прервана**\n\nВы не выращивали растения вчера. Серия сброшена до 1.\n\n💎 У вас есть {freezes} заморозок серии. Используйте их, чтобы сохранить прогресс!",
        "en": "💔 **Streak Broken**\n\nYou didn't grow plants yesterday. Streak reset to 1.\n\n💎 You have {freezes} streak freezes. Use them to save progress!"
    },
    
    "milestone_reached": {
        "ru": "🎊 **Веха достигнута!**\n\n🔥 Серия {days} дней!\n\n{reward_text}",
        "en": "🎊 **Milestone Reached!**\n\n🔥 {days} day streak!\n\n{reward_text}"
    },
    
    # Buttons
    "btn_start_focus": {
        "ru": "🎯 Начать фокус",
        "en": "🎯 Start Focus"
    },
    "btn_my_forest": {
        "ru": "🌲 Мой лес",
        "en": "🌲 My Forest"
    },
    "btn_statistics": {
        "ru": "📊 Статистика",
        "en": "📊 Statistics"
    },
    "btn_achievements": {
        "ru": "🏆 Достижения",
        "en": "🏆 Achievements"
    },
    "btn_settings": {
        "ru": "⚙️ Настройки",
        "en": "⚙️ Settings"
    },
    "btn_help": {
        "ru": "❓ Помощь",
        "en": "❓ Help"
    },
    "btn_complete_session": {
        "ru": "✅ Завершить сессию",
        "en": "✅ Complete Session"
    },
    "btn_abandon_session": {
        "ru": "❌ Прервать (растение погибнет)",
        "en": "❌ Abandon (plant dies)"
    },
    "btn_25min": {
        "ru": "⏱️ 25 минут (Pomodoro)",
        "en": "⏱️ 25 minutes (Pomodoro)"
    },
    "btn_50min": {
        "ru": "⏱️ 50 минут",
        "en": "⏱️ 50 minutes"
    },
    "btn_custom": {
        "ru": "🔧 Своя длительность",
        "en": "🔧 Custom duration"
    }
}

def get_message(key: str, lang: str = "ru", **kwargs) -> str:
    """Get localized message with formatting"""
    template = MESSAGES.get(key, {}).get(lang, "")
    if kwargs:
        return template.format(**kwargs)
    return template
