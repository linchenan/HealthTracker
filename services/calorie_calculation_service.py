"""
Calorie calculation service implementation following SOLID principles
"""
from typing import Dict, Any
from interfaces.services import ICalorieCalculationService
from interfaces.repositories import ILifestyleRepository


class CalorieCalculationService(ICalorieCalculationService):
    """Implementation of calorie calculation service"""
    
    def __init__(self, lifestyle_repository: ILifestyleRepository):
        self.lifestyle_repository = lifestyle_repository
    
    def calculate_exercise_calories(self, exercise_type: str, duration: int, weight: float) -> int:
        """Calculate calories burned during exercise"""
        # METs (Metabolic Equivalent of Task) values for different exercises
        mets_table = {
            '快走': 4.5,
            '慢跑': 7.0,
            '騎自行車': 6.0,
            '游泳': 8.0,
            '瑜珈': 3.0,
            '跳繩': 10.0,
            '有氧舞蹈': 6.5,
            '重量訓練': 5.0,
            '登山健行': 6.0,
            '球類運動': 7.0,
            '其他': 4.0
        }
        
        mets = mets_table.get(exercise_type, 4.0)
        # Calories = METs × weight(kg) × duration(hours)
        calories = int(mets * weight * (duration / 60))
        return calories
    
    def calculate_bmr(self, weight: float, height: float, age: int, gender: str) -> int:
        """Calculate Basal Metabolic Rate"""
        if gender.lower() in ['male', '男', 'M', 'm']:
            # Mifflin-St Jeor Equation for men
            bmr = 66 + (13.7 * weight) + (5 * height) - (6.8 * age)
        elif gender.lower() in ['female', '女', 'F', 'f']:
            # Mifflin-St Jeor Equation for women
            bmr = 655 + (9.6 * weight) + (1.8 * height) - (4.7 * age)
        else:
            # Default calculation (average)
            bmr = 1500
        
        return int(bmr)
    
    def get_daily_calorie_recommendation(self, bmr: int, activity_level: str) -> int:
        """Get daily calorie recommendation based on activity level"""
        activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,        # Light exercise 1-3 days/week
            'moderate': 1.55,      # Moderate exercise 3-5 days/week
            'active': 1.725,       # Hard exercise 6-7 days/week
            'very_active': 1.9     # Very hard exercise, physical job
        }
        
        multiplier = activity_multipliers.get(activity_level.lower(), 1.55)
        daily_calories = int(bmr * multiplier)
        
        return daily_calories
    
    def get_food_calories(self, food_item: str, portion_size: str = 'medium') -> int:
        """Get estimated calories for common food items"""
        # Basic food calorie database
        food_calories = {
            '白飯': {'small': 150, 'medium': 200, 'large': 300},
            '麵條': {'small': 180, 'medium': 250, 'large': 350},
            '雞胸肉': {'small': 120, 'medium': 160, 'large': 240},
            '豬肉': {'small': 150, 'medium': 200, 'large': 300},
            '牛肉': {'small': 140, 'medium': 180, 'large': 270},
            '魚肉': {'small': 100, 'medium': 130, 'large': 200},
            '雞蛋': {'small': 70, 'medium': 80, 'large': 90},
            '蔬菜': {'small': 20, 'medium': 30, 'large': 50},
            '水果': {'small': 50, 'medium': 80, 'large': 120},
            '牛奶': {'small': 60, 'medium': 100, 'large': 150},
            '麵包': {'small': 80, 'medium': 120, 'large': 180},
            '餅乾': {'small': 100, 'medium': 150, 'large': 250},
        }
        
        if food_item in food_calories:
            return food_calories[food_item].get(portion_size, food_calories[food_item]['medium'])
        
        # Default estimation for unknown foods
        return 100
    
    def analyze_daily_nutrition(self, user_id: int, date: str) -> Dict[str, Any]:
        """Analyze daily nutrition intake"""
        try:
            # Get diet records for the specific date
            diet_records = self.lifestyle_repository.get_diet_records_by_user(user_id)
            
            total_calories = 0
            protein_grams = 0
            carbs_grams = 0
            fat_grams = 0
            
            # Filter records for the specific date and calculate totals
            for record in diet_records:
                if record.date == date:
                    if record.calories:
                        total_calories += record.calories
                    else:
                        # Estimate calories if not provided
                        estimated_calories = self.get_food_calories(record.food_name, record.portion_size)
                        total_calories += estimated_calories
            
            # Estimate macronutrients (rough approximation)
            protein_grams = int(total_calories * 0.15 / 4)  # 15% of calories from protein
            carbs_grams = int(total_calories * 0.55 / 4)    # 55% of calories from carbs
            fat_grams = int(total_calories * 0.30 / 9)      # 30% of calories from fat
            
            recommendations = []
            if total_calories < 1200:
                recommendations.append("熱量攝取可能不足，建議增加營養均衡的食物")
            elif total_calories > 2500:
                recommendations.append("熱量攝取較高，建議適度控制份量")
            else:
                recommendations.append("熱量攝取在合理範圍內")
            
            return {
                'total_calories': total_calories,
                'protein_grams': protein_grams,
                'carbs_grams': carbs_grams,
                'fat_grams': fat_grams,
                'recommendations': recommendations
            }
        except Exception as e:
            print(f"Error analyzing daily nutrition: {e}")
            return {
                'total_calories': 0,
                'protein_grams': 0,
                'carbs_grams': 0,
                'fat_grams': 0,
                'recommendations': ['無法分析營養攝取，請確保有正確的飲食記錄']
            }
        """Calculate daily calorie needs based on activity level"""
        activity_multipliers = {
            'sedentary': 1.2,      # Little or no exercise
            'light': 1.375,        # Light exercise 1-3 days/week
            'moderate': 1.55,      # Moderate exercise 3-5 days/week
            'active': 1.725,       # Hard exercise 6-7 days/week
            'very_active': 1.9     # Very hard exercise, physical job
        }
        
        multiplier = activity_multipliers.get(activity_level, 1.55)
        daily_calories = int(bmr * multiplier)
        
        return {
            'maintenance': daily_calories,
            'weight_loss': int(daily_calories * 0.8),  # 20% deficit
            'weight_gain': int(daily_calories * 1.2)   # 20% surplus
        }
    
    def get_food_calories(self, food_item: str, portion_size: str = 'medium') -> int:
        """Get estimated calories for common food items"""
        # Basic food calorie database
        food_calories = {
            '白飯': {'small': 150, 'medium': 200, 'large': 300},
            '麵條': {'small': 180, 'medium': 250, 'large': 350},
            '雞胸肉': {'small': 120, 'medium': 160, 'large': 240},
            '豬肉': {'small': 150, 'medium': 200, 'large': 300},
            '牛肉': {'small': 140, 'medium': 180, 'large': 270},
            '魚肉': {'small': 100, 'medium': 130, 'large': 200},
            '雞蛋': {'small': 70, 'medium': 80, 'large': 90},
            '蔬菜': {'small': 20, 'medium': 30, 'large': 50},
            '水果': {'small': 50, 'medium': 80, 'large': 120},
            '牛奶': {'small': 60, 'medium': 100, 'large': 150},
            '麵包': {'small': 80, 'medium': 120, 'large': 180},
            '餅乾': {'small': 100, 'medium': 150, 'large': 250},
        }
        
        if food_item in food_calories:
            return food_calories[food_item].get(portion_size, food_calories[food_item]['medium'])
        
        # Default estimation for unknown foods
        return 100
    
    def analyze_daily_nutrition(self, user_id: int, date: str) -> Dict[str, Any]:
        """Analyze daily nutrition intake"""
        # This would get diet records from the lifestyle repository
        # For now, return a basic analysis structure
        return {
            'total_calories': 0,
            'protein_grams': 0,
            'carbs_grams': 0,
            'fat_grams': 0,
            'recommendations': []
        }