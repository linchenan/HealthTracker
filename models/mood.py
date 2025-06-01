from dataclasses import dataclass
from datetime import date

@dataclass
class MoodRecord:
    id: int
    user_id: int
    mood: str  # 'good' or 'bad'
    mood_date: str  # YYYY-MM-DD
    created_at: str
