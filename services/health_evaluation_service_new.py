# filepath: d:\Git\HealthTracker\services\health_evaluation_service.py
"""
Health evaluation service implementation following SOLID principles
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, date
from interfaces.services import IHealthEvaluationService
from interfaces.repositories import IUserRepository, IHealthDataRepository


class HealthEvaluationService(IHealthEvaluationService):
    """Implementation of health evaluation service"""
    
    def __init__(self, user_repository: IUserRepository, health_data_repository: IHealthDataRepository):
        self.user_repository = user_repository
        self.health_data_repository = health_data_repository
    
    def calculate_bmi(self, height: float, weight: float) -> float:
        """Calculate BMI"""
        if height <= 0 or weight <= 0:
            return 0.0
        height_m = height / 100  # Convert cm to meters
        return weight / (height_m * height_m)
    
    def evaluate_bmi(self, bmi: float) -> str:
        """Evaluate BMI category"""
        if bmi < 18.5:
            return "體重過輕"
        elif bmi < 24:
            return "正常體重"
        elif bmi < 27:
            return "體重過重"
        elif bmi < 30:
            return "輕度肥胖"
        elif bmi < 35:
            return "中度肥胖"
        else:
            return "重度肥胖"
    
    def evaluate_blood_pressure(self, systolic: int, diastolic: int) -> str:
        """Evaluate blood pressure category"""
        if systolic < 90 or diastolic < 60:
            return "低血壓"
        elif systolic < 120 and diastolic < 80:
            return "正常血壓"
        elif systolic < 130 and diastolic < 80:
            return "血壓偏高"
        elif systolic < 140 or diastolic < 90:
            return "第一期高血壓"
        elif systolic < 180 or diastolic < 120:
            return "第二期高血壓"
        else:
            return "高血壓危象"
    
    def calculate_age(self, birthday: str) -> int:
        """Calculate age from birthday"""
        if not birthday:
            return 0
        
        try:
            birth_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            today = date.today()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return 0
    
    def get_health_trends(self, user_id: int) -> Dict[str, Any]:
        """Get health trends for user"""
        try:
            # Get recent records
            bp_records = self.health_data_repository.get_blood_pressure_records_by_user(user_id)
            hw_records = self.health_data_repository.get_height_weight_records_by_user(user_id)
            
            # Prepare trend data (latest 10 records)
            bp_trend = []
            for record in bp_records[:10]:
                bp_trend.append({
                    'date': record.date,
                    'systolic': record.systolic,
                    'diastolic': record.diastolic,
                    'category': self.evaluate_blood_pressure(record.systolic, record.diastolic)
                })
            
            weight_trend = []
            bmi_trend = []
            for record in hw_records[:10]:
                weight_trend.append({
                    'date': record.date,
                    'weight': record.weight
                })
                
                if record.height > 0:
                    bmi = self.calculate_bmi(record.height, record.weight)
                    bmi_trend.append({
                        'date': record.date,
                        'bmi': round(bmi, 1),
                        'category': self.evaluate_bmi(bmi)
                    })
            
            return {
                'blood_pressure_trend': bp_trend,
                'weight_trend': weight_trend,
                'bmi_trend': bmi_trend
            }
        except Exception as e:
            print(f"Error getting health trends: {e}")
            return {
                'blood_pressure_trend': [],
                'weight_trend': [],
                'bmi_trend': []
            }
    
    def get_health_summary(self, user_id: int) -> Dict[str, Any]:
        """Get comprehensive health summary"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return {}
            
            # Get latest records
            bp_records = self.health_data_repository.get_blood_pressure_records_by_user(user_id)
            hw_records = self.health_data_repository.get_height_weight_records_by_user(user_id)
            
            summary = {
                'user_info': {
                    'username': user.username,
                    'age': self.calculate_age(user.birthday) if user.birthday else 0,
                    'gender': user.gender or '未設定'
                }
            }
            
            # Blood pressure summary
            if bp_records:
                latest_bp = bp_records[0]
                summary['blood_pressure'] = {
                    'systolic': latest_bp.systolic,
                    'diastolic': latest_bp.diastolic,
                    'category': self.evaluate_blood_pressure(latest_bp.systolic, latest_bp.diastolic),
                    'date': latest_bp.date
                }
            else:
                summary['blood_pressure'] = None
            
            # BMI summary
            if hw_records:
                latest_hw = hw_records[0]
                if latest_hw.height > 0:
                    bmi = self.calculate_bmi(latest_hw.height, latest_hw.weight)
                    summary['bmi'] = {
                        'value': round(bmi, 1),
                        'category': self.evaluate_bmi(bmi),
                        'height': latest_hw.height,
                        'weight': latest_hw.weight,
                        'date': latest_hw.date
                    }
                else:
                    summary['bmi'] = None
            else:
                summary['bmi'] = None
            
            # Health recommendations
            summary['recommendations'] = self._get_health_recommendations(summary)
            
            return summary
        except Exception as e:
            print(f"Error getting health summary: {e}")
            return {}
    
    def _get_health_recommendations(self, summary: Dict[str, Any]) -> List[str]:
        """Get health recommendations based on current data"""
        recommendations = []
        
        # Blood pressure recommendations
        if summary.get('blood_pressure'):
            bp_category = summary['blood_pressure']['category']
            if bp_category == '低血壓':
                recommendations.append('血壓偏低，建議增加水分攝取，避免快速站立')
            elif bp_category in ['第一期高血壓', '第二期高血壓', '高血壓危象']:
                recommendations.append('血壓偏高，建議調整生活方式，減少鹽分攝取，並諮詢醫師')
            elif bp_category == '正常血壓':
                recommendations.append('血壓正常，請維持健康的生活習慣')
        
        # BMI recommendations
        if summary.get('bmi'):
            bmi_category = summary['bmi']['category']
            if bmi_category == '體重過輕':
                recommendations.append('建議增加營養攝取，適度運動增強體力')
            elif bmi_category in ['體重過重', '輕度肥胖', '中度肥胖', '重度肥胖']:
                recommendations.append('建議控制飲食熱量，增加運動量，如有需要請諮詢專業人士')
            elif bmi_category == '正常體重':
                recommendations.append('體重正常，請維持健康的飲食和運動習慣')
        
        # General recommendations
        recommendations.extend([
            '建議定期監測血壓和體重',
            '保持規律運動習慣',
            '維持均衡飲食',
            '充足睡眠和適當休息'
        ])
        
        return recommendations
