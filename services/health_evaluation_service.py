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
        
    def evaluate_bmi(self, latest_hw: Optional[Dict], gender: str, age: int) -> str:
        """Evaluate BMI based on latest height/weight record"""
        if not latest_hw or latest_hw.get('height', 0) <= 0 or latest_hw.get('weight', 0) <= 0:
            return "無法計算BMI，請確認身高體重數據"
        
        bmi = self.calculate_bmi(latest_hw['height'], latest_hw['weight'])
        category = self.evaluate_bmi(bmi)
        return f"{category} (BMI: {bmi:.1f})"
    
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
    
    def get_user_profile(self, user_id: int) -> tuple:
        """Get user profile (gender, birthday)"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if user:
                return (user.gender, user.birthday)
            return (None, None)
        except Exception as e:
            print(f"Error getting user profile: {e}")
            return (None, None)
    
    def update_user_profile(self, user_id: int, gender: str, birthday: str) -> bool:
        """Update user profile"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if user:
                user.gender = gender
                user.birthday = birthday
                return self.user_repository.update_user(user)
            return False
        except Exception as e:
            print(f"Error updating user profile: {e}")
            return False
    
    def calculate_age_and_days(self, birthday: str) -> tuple:
        """Calculate age and days lived"""
        if not birthday:
            return ("未設定", 0)
        
        try:
            birth_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            today = date.today()
            age_years = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            days_lived = (today - birth_date).days
            age_str = f"{age_years}歲 ({days_lived}天)"
            return (age_str, age_years)
        except:
            return ("計算錯誤", 0)
    
    def get_disease_info_and_prevention(self, age: int) -> tuple:
        """Get disease information and prevention tips based on age"""
        if age < 20:
            disease_info = "青少年時期應注意：生長發育、營養均衡、運動習慣養成"
            prevention = "建議：規律作息、均衡飲食、適度運動、避免熬夜"
        elif age < 30:
            disease_info = "青年時期應注意：代謝症候群預防、壓力管理"
            prevention = "建議：定期健檢、維持運動習慣、注意心理健康"
        elif age < 40:
            disease_info = "成年時期應注意：高血壓、糖尿病、心血管疾病預防"
            prevention = "建議：年度健檢、控制體重、戒菸限酒、壓力管理"
        elif age < 50:
            disease_info = "中年時期應注意：代謝疾病、癌症篩檢、骨質疏鬆預防"
            prevention = "建議：定期癌症篩檢、補充鈣質、維持肌力訓練"
        elif age < 65:
            disease_info = "中老年時期應注意：心血管疾病、糖尿病併發症、關節退化"
            prevention = "建議：定期追蹤慢性病、適度運動、社交活動參與"
        else:
            disease_info = "高齡時期應注意：失智症預防、跌倒預防、營養不良"
            prevention = "建議：認知訓練、居家安全、營養評估、定期健檢"
        
        return (disease_info, prevention)
    
    def get_blood_pressure_records(self, user_id: int) -> List[Dict[str, Any]]:
        """Get blood pressure records for user"""
        try:
            records = self.health_data_repository.get_blood_pressure_records_by_user(user_id)
            return [
                {
                    'id': record.id,
                    'systolic': record.systolic,
                    'diastolic': record.diastolic,
                    'pulse': record.pulse,
                    'notes': record.notes,
                    'date': record.date,
                    'created_at': record.created_at
                }
                for record in records
            ]
        except Exception as e:
            print(f"Error getting blood pressure records: {e}")
            return []
    
    def get_height_weight_records(self, user_id: int) -> List[Dict[str, Any]]:
        """Get height/weight records for user"""
        try:
            records = self.health_data_repository.get_height_weight_records_by_user(user_id)
            return [
                {
                    'id': record.id,
                    'height': record.height,
                    'weight': record.weight,
                    'notes': record.notes,
                    'date': record.date,
                    'created_at': record.created_at
                }
                for record in records
            ]
        except Exception as e:
            print(f"Error getting height/weight records: {e}")
            return []
    
    def evaluate_blood_pressure(self, bp_record: Optional[Dict]) -> Dict[str, str]:
        """Evaluate blood pressure record (dict input)"""
        if not bp_record:
            return {'status': '無血壓數據', 'recommendation': '請記錄血壓數據以獲得評估'}
        systolic = bp_record.get('systolic', 0)
        diastolic = bp_record.get('diastolic', 0)
        category = self._bp_category(systolic, diastolic)
        recommendations = {
            "低血壓": "建議諮詢醫師，注意水分攝取，避免突然起身",
            "正常血壓": "請保持良好的生活習慣",
            "血壓偏高": "建議減少鈉攝取，增加運動，定期監測",
            "第一期高血壓": "建議就醫諮詢，調整生活型態",
            "第二期高血壓": "建議盡快就醫治療",
            "高血壓危機": "請立即就醫！"
        }
        return {
            'status': category,
            'recommendation': recommendations.get(category, '請諮詢醫師')
        }

    def _bp_category(self, systolic: int, diastolic: int) -> str:
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
            return "高血壓危機"
    
    def evaluate_bmi(self, hw_record: Optional[Dict], gender: str, age: int) -> Dict[str, str]:
        """Evaluate BMI record"""
        if not hw_record:
            return {'status': '無身高體重數據', 'recommendation': '請記錄身高體重數據以獲得評估'}
        height = hw_record.get('height', 0)
        weight = hw_record.get('weight', 0)
        if height <= 0 or weight <= 0:
            return {'status': '數據錯誤', 'recommendation': '請確認身高體重數據正確性'}
        bmi = self.calculate_bmi(height, weight)
        category = self._bmi_category(bmi)
        recommendations = {
            "體重過輕": "建議增加營養攝取，適度重量訓練",
            "正常體重": "請保持良好的飲食和運動習慣",
            "體重過重": "建議控制飲食，增加有氧運動",
            "輕度肥胖": "建議制定減重計畫，諮詢營養師",
            "中度肥胖": "建議醫療減重介入，定期追蹤",
            "重度肥胖": "強烈建議就醫評估，考慮醫療介入"
        }
        return {
            'status': f"{category} (BMI: {bmi:.1f})",
            'recommendation': recommendations.get(category, '請諮詢醫師')
        }

    def _bmi_category(self, bmi: float) -> str:
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
    
    def delete_blood_pressure_record(self, record_id: int, user_id: int) -> bool:
        """Delete blood pressure record"""
        try:
            return self.health_data_repository.delete_blood_pressure_record(record_id)
        except Exception as e:
            print(f"Error deleting blood pressure record: {e}")
            return False
    
    def delete_height_weight_record(self, record_id: int, user_id: int) -> bool:
        """Delete height/weight record"""
        try:
            return self.health_data_repository.delete_height_weight_record(record_id)
        except Exception as e:
            print(f"Error deleting height/weight record: {e}")
            return False
