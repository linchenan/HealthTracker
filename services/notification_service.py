"""
Notification service implementation following SOLID principles
"""
from typing import Dict, Any, List
from datetime import datetime, timedelta
from interfaces.services import INotificationService
from interfaces.repositories import IUserRepository, IHealthDataRepository, IMedicalRepository


class NotificationService(INotificationService):
    """Implementation of notification service"""
    
    def __init__(self, user_repository: IUserRepository, 
                 health_data_repository: IHealthDataRepository,
                 medical_repository: IMedicalRepository):
        self.user_repository = user_repository
        self.health_data_repository = health_data_repository
        self.medical_repository = medical_repository
    
    def send_health_reminder(self, user_id: int, message: str) -> bool:
        """Send health reminder to user"""
        try:
            # In a real implementation, this would send actual notifications
            # For now, just log the reminder
            user = self.user_repository.get_user_by_id(user_id)
            if user:
                print(f"健康提醒給 {user.username}: {message}")
                return True
            return False
        except Exception as e:
            print(f"Error sending health reminder: {e}")
            return False
    
    def send_appointment_reminder(self, user_id: int, appointment_details: Dict[str, Any]) -> bool:
        """Send appointment reminder"""
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if user:
                doctor = appointment_details.get('doctor', '醫師')
                date = appointment_details.get('appointment_date', '')
                time = appointment_details.get('appointment_time', '')
                message = f"預約提醒：您有與 {doctor} 的預約，時間為 {date} {time}"
                print(f"預約提醒給 {user.username}: {message}")
                return True
            return False
        except Exception as e:
            print(f"Error sending appointment reminder: {e}")
            return False
    
    def check_health_alerts(self, user_id: int) -> List[str]:
        """Check for health alerts for user"""
        alerts = []
        
        try:
            # Check for overdue health records
            bp_records = self.health_data_repository.get_blood_pressure_records_by_user(user_id)
            hw_records = self.health_data_repository.get_height_weight_records_by_user(user_id)
            
            # Check if no blood pressure records in last 30 days
            if bp_records:
                latest_bp = bp_records[0]
                latest_date = datetime.strptime(latest_bp.date, '%Y-%m-%d').date()
                if (datetime.now().date() - latest_date).days > 30:
                    alerts.append("已超過30天未測量血壓，建議定期監測")
            else:
                alerts.append("尚無血壓記錄，建議開始監測血壓")
            
            # Check if no weight records in last 30 days
            if hw_records:
                latest_hw = hw_records[0]
                latest_date = datetime.strptime(latest_hw.date, '%Y-%m-%d').date()
                if (datetime.now().date() - latest_date).days > 30:
                    alerts.append("已超過30天未記錄體重，建議定期監測")
            else:
                alerts.append("尚無體重記錄，建議開始監測體重變化")
            
            # Check for abnormal blood pressure values
            if bp_records:
                latest_bp = bp_records[0]
                if latest_bp.systolic > 140 or latest_bp.diastolic > 90:
                    alerts.append("最近血壓偏高，建議諮詢醫師")
                elif latest_bp.systolic < 90 or latest_bp.diastolic < 60:
                    alerts.append("最近血壓偏低，如有不適請諮詢醫師")
            
            # Check upcoming appointments
            appointments = self.medical_repository.get_appointments_by_user(user_id)
            today = datetime.now().date()
            for appointment in appointments:
                appointment_date = datetime.strptime(appointment.appointment_date, '%Y-%m-%d').date()
                days_until = (appointment_date - today).days
                
                if days_until == 1:
                    alerts.append(f"明天有預約：{appointment.doctor} - {appointment.appointment_time}")
                elif days_until == 0:
                    alerts.append(f"今天有預約：{appointment.doctor} - {appointment.appointment_time}")
                elif days_until < 0 and days_until > -7:
                    alerts.append(f"錯過的預約：{appointment.doctor} ({appointment.appointment_date})")
            
        except Exception as e:
            print(f"Error checking health alerts: {e}")
            alerts.append("檢查健康提醒時發生錯誤")
        
        return alerts
    
    def get_health_recommendations(self, user_id: int) -> List[str]:
        """Get personalized health recommendations"""
        recommendations = []
        
        try:
            user = self.user_repository.get_user_by_id(user_id)
            if not user:
                return recommendations
            
            # Basic recommendations
            recommendations.extend([
                "每日至少運動30分鐘",
                "維持均衡飲食，多吃蔬果",
                "保持充足睡眠（7-8小時）",
                "定期監測血壓和體重",
                "適量飲水，每日至少8杯水"
            ])
            
            # Age-based recommendations
            if user.birthday:
                from interfaces.services import IHealthEvaluationService
                # This would normally be injected, but for simplicity:
                age = self._calculate_age(user.birthday)
                
                if age >= 40:
                    recommendations.append("建議每年進行全面健康檢查")
                if age >= 50:
                    recommendations.append("注意心血管健康，定期檢查膽固醇")
                if age >= 60:
                    recommendations.append("加強骨質密度檢測，預防骨質疏鬆")
            
        except Exception as e:
            print(f"Error getting health recommendations: {e}")
        
        return recommendations
    
    def _calculate_age(self, birthday: str) -> int:
        """Calculate age from birthday string"""
        try:
            birth_date = datetime.strptime(birthday, '%Y-%m-%d').date()
            today = datetime.now().date()
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        except:
            return 0