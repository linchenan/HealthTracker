from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class User:
    """User domain model"""
    id: Optional[int] = None
    username: str = ""
    password: str = ""
    email: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class BloodPressureRecord:
    """Blood pressure record domain model"""
    id: Optional[int] = None
    user_id: int = 0
    systolic: int = 0
    diastolic: int = 0
    pulse: Optional[int] = None
    notes: Optional[str] = None
    date: str = ""
    recorded_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class HeightWeightRecord:
    """Height and weight record domain model"""
    id: Optional[int] = None
    user_id: int = 0
    height: float = 0.0
    weight: float = 0.0
    notes: Optional[str] = None
    date: str = ""
    recorded_at: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class MedicalRecord:
    """Medical record domain model"""
    id: Optional[int] = None
    user_id: int = 0
    record_type: str = ""
    description: str = ""
    doctor: Optional[str] = None
    hospital: Optional[str] = None
    date: str = ""
    notes: Optional[str] = None
    created_at: Optional[str] = None


@dataclass
class Appointment:
    """Appointment domain model"""
    id: Optional[int] = None
    user_id: int = 0
    doctor: str = ""
    hospital: Optional[str] = None
    appointment_date: str = ""
    appointment_time: str = ""
    purpose: str = ""
    notes: Optional[str] = None
    status: str = "scheduled"
    created_at: Optional[str] = None


@dataclass
class ExerciseRecord:
    """Exercise record domain model"""
    id: Optional[int] = None
    user_id: int = 0
    exercise_type: str = ""
    duration: int = 0  # minutes
    intensity: str = ""
    calories_burned: Optional[int] = None
    notes: Optional[str] = None
    date: str = ""
    created_at: Optional[str] = None


@dataclass
class DietRecord:
    """Diet record domain model"""
    id: Optional[int] = None
    user_id: int = 0
    food_name: str = ""
    meal_type: str = ""
    portion_size: str = ""
    calories: Optional[int] = None
    notes: Optional[str] = None
    date: str = ""
    created_at: Optional[str] = None