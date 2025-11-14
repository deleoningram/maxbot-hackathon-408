from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

class UserDatabase:
    """Local JSON-based database for hackathon MVP"""
    
    def __init__(self, filepath: str = "user_data.json"):
        self.filepath = filepath
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def get_user(self, user_id: str) -> dict:
        """Get user data or create new user profile"""
        if user_id not in self.data:
            self.data[user_id] = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "language": "ru",
                "plants": [],  # List of grown plants
                "current_session": None,
                "stats": {
                    "total_focus_minutes": 0,
                    "total_plants": 0,
                    "current_streak": 0,
                    "longest_streak": 0,
                    "last_activity_date": None,
                    "streak_freezes": 2  # Free recovery tokens
                },
                "preferences": {
                    "session_duration": 25,  # Pomodoro default
                    "favorite_plant": "🌱"
                },
                "achievements": []
            }
            self._save_data()
        return self.data[user_id]
    
    def update_user(self, user_id: str, data: dict):
        """Update user data"""
        if user_id in self.data:
            self.data[user_id].update(data)
            self._save_data()
    
    def start_session(self, user_id: str, duration: int, plant_type: str):
        """Start a focus session"""
        user = self.get_user(user_id)
        session = {
            "start_time": datetime.now().isoformat(),
            "duration_minutes": duration,
            "plant_type": plant_type,
            "status": "active"
        }
        user["current_session"] = session
        self.update_user(user_id, user)
        return session
    
    def complete_session(self, user_id: str):
        """Complete a focus session and award plant"""
        user = self.get_user(user_id)
        session = user.get("current_session")
        
        if not session or session["status"] != "active":
            return None
        
        # Mark session complete
        session["status"] = "completed"
        session["end_time"] = datetime.now().isoformat()
        
        # Award plant
        plant = {
            "type": session["plant_type"],
            "grown_at": datetime.now().isoformat(),
            "session_minutes": session["duration_minutes"]
        }
        user["plants"].append(plant)
        
        # Update stats
        user["stats"]["total_focus_minutes"] += session["duration_minutes"]
        user["stats"]["total_plants"] += 1
        
        # Update streak
        today = datetime.now().date().isoformat()
        last_activity = user["stats"]["last_activity_date"]
        
        if last_activity == today:
            # Already counted today
            pass
        elif last_activity == (datetime.now().date() - timedelta(days=1)).isoformat():
            # Consecutive day - increment streak
            user["stats"]["current_streak"] += 1
            if user["stats"]["current_streak"] > user["stats"]["longest_streak"]:
                user["stats"]["longest_streak"] = user["stats"]["current_streak"]
        else:
            # Streak broken - reset to 1
            user["stats"]["current_streak"] = 1
        
        user["stats"]["last_activity_date"] = today
        user["current_session"] = None
        
        self.update_user(user_id, user)
        return plant
    
    def abandon_session(self, user_id: str):
        """User abandoned session - plant dies"""
        user = self.get_user(user_id)
        if user.get("current_session"):
            user["current_session"]["status"] = "abandoned"
            user["current_session"] = None
            self.update_user(user_id, user)
            return True
        return False

# Initialize global database
db = UserDatabase()
