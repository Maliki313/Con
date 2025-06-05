"""
اختبار شارح السياق الثقافي الإسلامي
نصوص اختبار للتأكد من عمل النظام بشكل صحيح
"""

import sys
import os

# إضافة المسار الحالي لاستيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from islamic_context_explainer import IslamicContextExplainer, ConceptCategory
from session_manager import SessionManager, SessionState

def test_islamic_explainer():
    """اختبار أساسي لشارح المفاهيم الإسلامية"""
    print("🧪 بدء اختبار شارح المفاهيم الإسلامية")
    print("=" * 50)
    
    # إنشاء شارح
    explainer = IslamicContextExplainer()
    
    # اختبار البحث
    print("\n1. اختبار البحث:")
    search_queries = ["الصلاة", "prayer", "توحيد", "hajj"]
    
    for query in search_queries:
        results = explainer.search_concepts(query)
        print(f"البحث عن '{query}': {len(results)} نتيجة")
        if results:
            print(f"   النتيجة الأولى: {results[0]}")
    
    # اختبار الشرح
    print("\n2. اختبار الشرح:")
    concept_id = "salah"
    explanation = explainer.explain_concept(concept_id, "medium")
    print(f"شرح مفهوم '{concept_id}':")
    print(explanation[:200] + "..." if len(explanation) > 200 else explanation)
    
    # اختبار القائمة التفاعلية
    print("\n3. اختبار القائمة التفاعلية:")
    menu = explainer.get_interactive_menu(concept_id)
    print("القائمة التفاعلية:")
    print(menu[:300] + "..." if len(menu) > 300 else menu)
    
    # اختبار جوانب المفهوم
    print("\n4. اختبار جوانب المفهوم:")
    aspects = ["1", "2", "8"]
    for aspect in aspects:
        content = explainer.get_concept_aspect(concept_id, aspect)
        print(f"الجانب {aspect}:")
        print(content[:150] + "..." if len(content) > 150 else content)
        print()
    
    # اختبار المفهوم العشوائي
    print("\n5. اختبار المفهوم العشوائي:")
    random_concept = explainer.get_random_concept()
    print("مفهوم عشوائي:")
    print(random_concept[:200] + "..." if len(random_concept) > 200 else random_concept)
    
    print("\n✅ انتهى اختبار شارح المفاهيم الإسلامية بنجاح")

def test_session_manager():
    """اختبار مدير الجلسات"""
    print("\n🧪 بدء اختبار مدير الجلسات")
    print("=" * 50)
    
    # إنشاء مدير الجلسات
    manager = SessionManager()
    
    # اختبار إنشاء جلسة
    print("\n1. اختبار إنشاء الجلسات:")
    user_ids = [12345, 67890, 11111]
    
    for user_id in user_ids:
        session = manager.get_session(user_id)
        print(f"جلسة للمستخدم {user_id}: {session.state.value}")
        session.set_context("test_key", f"test_value_{user_id}")
    
    # اختبار إحصائيات الجلسات
    print("\n2. اختبار الإحصائيات:")
    stats = manager.get_session_stats()
    print(f"عدد الجلسات النشطة: {stats['total_active']}")
    print(f"توزيع الحالات: {stats['states_distribution']}")
    
    # اختبار سياق المحادثة
    print("\n3. اختبار السياق:")
    session = manager.get_session(12345)
    session.state = SessionState.EXPLORING_CONCEPT
    session.set_context("current_concept", "salah")
    session.add_to_history("user_message", "اختبار الرسالة")
    
    print(f"حالة الجلسة: {session.state.value}")
    print(f"السياق: {session.get_context('current_concept')}")
    print(f"طول التاريخ: {len(session.conversation_history)}")
    
    # اختبار مسح الجلسة
    print("\n4. اختبار مسح الجلسة:")
    manager.clear_session(12345)
    cleared_session = manager.get_session(12345)
    print(f"حالة الجلسة بعد المسح: {cleared_session.state.value}")
    print(f"السياق بعد المسح: {len(cleared_session.context)}")
    
    print("\n✅ انتهى اختبار مدير الجلسات بنجاح")

def test_integration():
    """اختبار التكامل بين المكونات"""
    print("\n🧪 بدء اختبار التكامل")
    print("=" * 50)
    
    explainer = IslamicContextExplainer()
    manager = SessionManager()
    
    # محاكاة تفاعل مستخدم
    user_id = 99999
    session = manager.get_session(user_id)
    
    # البحث عن مفهوم
    query = "الصلاة"
    results = explainer.search_concepts(query)
    
    if results:
        concept_id = results[0]
        print(f"1. تم العثور على المفهوم: {concept_id}")
        
        # تعيين حالة الاستكشاف
        session.state = SessionState.EXPLORING_CONCEPT
        session.set_context("current_concept", concept_id)
        session.add_to_history("search", query)
        
        # عرض القائمة التفاعلية
        menu = explainer.get_interactive_menu(concept_id)
        print("2. تم عرض القائمة التفاعلية")
        
        # محاكاة اختيار المستخدم
        choice = "1"
        aspect_content = explainer.get_concept_aspect(concept_id, choice)
        session.add_to_history("choice", choice)
        print(f"3. تم عرض الجانب {choice}")
        
        # عرض الاقتراحات
        suggestions = explainer.suggest_related_concepts(concept_id)
        print("4. تم عرض الاقتراحات")
        
        # إحصائيات نهائية
        stats = manager.get_session_stats()
        print(f"5. إحصائيات نهائية: {stats['total_active']} جلسة نشطة")
        
        print("\n✅ اختبار التكامل مكتمل بنجاح")
    else:
        print("❌ فشل في العثور على المفهوم")

if __name__ == "__main__":
    try:
        test_islamic_explainer()
        test_session_manager()
        test_integration()
        print("\n🎉 جميع الاختبارات اكتملت بنجاح!")
        
    except Exception as e:
        print(f"\n❌ فشل في الاختبار: {e}")
        import traceback
        traceback.print_exc()