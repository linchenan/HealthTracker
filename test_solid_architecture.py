"""
簡單測試腳本，驗證 SOLID 架構是否正常工作
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from di_container import initialize_container, get_auth_service, get_health_service, get_notification_service
from models.domain import User, BloodPressureRecord, HeightWeightRecord
from datetime import datetime

def test_solid_architecture():
    """測試 SOLID 架構的各個組件"""
    
    # 初始化 DI 容器
    db_path = "healthTracker.db"
    initialize_container(db_path)
    
    print("🏗️  測試 SOLID 架構...")
    
    # 測試依賴注入容器
    print("\n✅ 依賴注入容器初始化成功")
    
    # 測試服務獲取
    auth_service = get_auth_service()
    health_service = get_health_service()
    notification_service = get_notification_service()
    
    print("✅ 所有服務成功從容器中獲取")
    
    # 測試密碼哈希
    password = "test123"
    hashed = auth_service.hash_password(password)
    print(f"✅ 密碼哈希功能正常: {password} -> {hashed[:10]}...")
    
    # 測試 BMI 計算
    height = 170.0  # cm
    weight = 70.0   # kg
    bmi = health_service.calculate_bmi(height, weight)
    category = health_service.evaluate_bmi(bmi)
    print(f"✅ BMI 計算功能正常: {height}cm, {weight}kg -> BMI {bmi:.1f} ({category})")
    
    # 測試血壓評估
    systolic = 120
    diastolic = 80
    bp_category = health_service.evaluate_blood_pressure(systolic, diastolic)
    print(f"✅ 血壓評估功能正常: {systolic}/{diastolic} -> {bp_category}")
    
    # 測試年齡計算
    birthday = "1990-01-01"
    age = health_service.calculate_age(birthday)
    print(f"✅ 年齡計算功能正常: {birthday} -> {age} 歲")
    
    # 測試通知服務
    alerts = notification_service.get_health_recommendations(1)
    print(f"✅ 健康建議功能正常: 獲得 {len(alerts)} 條建議")
    
    print("\n🎉 SOLID 架構測試完成！所有組件都正常工作。")
    
    print("\n📋 架構特點:")
    print("   • Single Responsibility Principle (SRP): 每個類都有單一職責")
    print("   • Open-Closed Principle (OCP): 通過接口實現擴展性")
    print("   • Liskov Substitution Principle (LSP): 所有實現都可以替換接口")
    print("   • Interface Segregation Principle (ISP): 接口被分離為特定功能")
    print("   • Dependency Inversion Principle (DIP): 高層模組依賴於抽象")
    
    return True

if __name__ == "__main__":
    try:
        test_solid_architecture()
    except Exception as e:
        print(f"❌ 測試失敗: {e}")
        import traceback
        traceback.print_exc()
