# Plant progression system with Russian names
PLANT_SPECIES = {
    # FREE TIER - Basic plants
    "seedling": {
        "emoji": "🌱",
        "name_ru": "Росток",
        "name_en": "Seedling",
        "tier": "free",
        "unlock_at": 0
    },
    "sprout": {
        "emoji": "🌿",
        "name_ru": "Побег",
        "name_en": "Sprout",
        "tier": "free",
        "unlock_at": 5  # 5 plants grown
    },
    "herb": {
        "emoji": "🍀",
        "name_ru": "Клевер",
        "name_en": "Clover",
        "tier": "free",
        "unlock_at": 10
    },
    
    # BRONZE TIER - Week 1-2
    "flower": {
        "emoji": "🌸",
        "name_ru": "Цветок",
        "name_en": "Flower",
        "tier": "bronze",
        "unlock_at": 15
    },
    "sunflower": {
        "emoji": "🌻",
        "name_ru": "Подсолнух",
        "name_en": "Sunflower",
        "tier": "bronze",
        "unlock_at": 20
    },
    "rose": {
        "emoji": "🌹",
        "name_ru": "Роза",
        "name_en": "Rose",
        "tier": "bronze",
        "unlock_at": 25
    },
    
    # SILVER TIER - Week 3-8
    "sapling": {
        "emoji": "🌳",
        "name_ru": "Саженец",
        "name_en": "Sapling",
        "tier": "silver",
        "unlock_at": 30
    },
    "pine": {
        "emoji": "🌲",
        "name_ru": "Сосна",
        "name_en": "Pine",
        "tier": "silver",
        "unlock_at": 40
    },
    "palm": {
        "emoji": "🌴",
        "name_ru": "Пальма",
        "name_en": "Palm",
        "tier": "silver",
        "unlock_at": 50
    },
    
    # GOLD TIER - Week 9+ (Premium)
    "cherry": {
        "emoji": "🌸",
        "name_ru": "Сакура",
        "name_en": "Cherry Blossom",
        "tier": "gold",
        "unlock_at": 60,
        "premium": True
    },
    "bamboo": {
        "emoji": "🎋",
        "name_ru": "Бамбук",
        "name_en": "Bamboo",
        "tier": "gold",
        "unlock_at": 70,
        "premium": True
    },
    "cactus": {
        "emoji": "🌵",
        "name_ru": "Кактус",
        "name_en": "Cactus",
        "tier": "gold",
        "unlock_at": 80,
        "premium": True
    }
}

def get_available_plants(user_data: dict, is_premium: bool = False) -> list:
    """Return list of plants user can currently grow"""
    total_plants = user_data["stats"]["total_plants"]
    available = []
    
    for plant_id, plant_info in PLANT_SPECIES.items():
        # Check if unlocked by count
        if total_plants >= plant_info["unlock_at"]:
            # Check if premium required
            if plant_info.get("premium", False) and not is_premium:
                continue
            available.append((plant_id, plant_info))
    
    return available

def get_next_unlock(user_data: dict) -> dict:
    """Get info about next plant to unlock"""
    total_plants = user_data["stats"]["total_plants"]
    
    for plant_id, plant_info in sorted(PLANT_SPECIES.items(), 
                                       key=lambda x: x[1]["unlock_at"]):
        if total_plants < plant_info["unlock_at"]:
            return {
                "plant": plant_info,
                "plants_needed": plant_info["unlock_at"] - total_plants
            }
    
    return None

# Achievement system
ACHIEVEMENTS = {
    "first_plant": {
        "icon": "🏆",
        "name_ru": "Первый росток",
        "description_ru": "Вырастил первое растение",
        "condition": lambda user: user["stats"]["total_plants"] >= 1
    },
    "week_streak": {
        "icon": "🔥",
        "name_ru": "Неделя продуктивности",
        "description_ru": "Поддерживал серию 7 дней",
        "condition": lambda user: user["stats"]["longest_streak"] >= 7
    },
    "forest_builder": {
        "icon": "🌲",
        "name_ru": "Строитель леса",
        "description_ru": "Вырастил 100 растений",
        "condition": lambda user: user["stats"]["total_plants"] >= 100
    },
    "focus_master": {
        "icon": "⏱️",
        "name_ru": "Мастер концентрации",
        "description_ru": "Накопил 1000 минут фокуса",
        "condition": lambda user: user["stats"]["total_focus_minutes"] >= 1000
    }
}
