"""
مدير الجلسات التفاعلية للبوت
إدارة حالة المحادثات والتفاعلات المخصصة
"""

from typing import Dict, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import json

class SessionState(Enum):
    """حالات الجلسة"""
    NORMAL = "normal"
    EXPLORING_CONCEPT = "exploring_concept"
    AWAITING_CHOICE = "awaiting_choice"
    LEARNING_MODE = "learning_mode"

class UserSession:
    """جلسة المستخدم"""
    
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.state = SessionState.NORMAL
        self.context = {}
        self.last_activity = datetime.now()
        self.conversation_history = []
        self.preferences = {
            "detail_level": "medium",
            "language": "arabic",
            "learning_pace": "normal"
        }
    
    def update_activity(self):
        """تحديث وقت آخر نشاط"""
        self.last_activity = datetime.now()
    
    def set_context(self, key: str, value: Any):
        """تعيين سياق المحادثة"""
        self.context[key] = value
        self.update_activity()
    
    def get_context(self, key: str, default=None):
        """الحصول على سياق المحادثة"""
        return self.context.get(key, default)
    
    def clear_context(self):
        """مسح سياق المحادثة"""
        self.context.clear()
        self.state = SessionState.NORMAL
        self.update_activity()
    
    def add_to_history(self, message_type: str, content: str):
        """إضافة رسالة للتاريخ"""
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "type": message_type,
            "content": content
        })
        # الاحتفاظ بآخر 50 رسالة فقط
        if len(self.conversation_history) > 50:
            self.conversation_history = self.conversation_history[-50:]
    
    def is_expired(self, timeout_minutes: int = 30) -> bool:
        """فحص انتهاء صلاحية الجلسة"""
        return datetime.now() - self.last_activity > timedelta(minutes=timeout_minutes)

class SessionManager:
    """مدير الجلسات"""
    
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}
        self.session_timeout = 30  # دقيقة
    
    def get_session(self, user_id: int) -> UserSession:
        """الحصول على جلسة المستخدم أو إنشاء جديدة"""
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id)
        elif self.sessions[user_id].is_expired(self.session_timeout):
            # إنشاء جلسة جديدة للجلسات المنتهية الصلاحية
            self.sessions[user_id] = UserSession(user_id)
        
        self.sessions[user_id].update_activity()
        return self.sessions[user_id]
    
    def clear_session(self, user_id: int):
        """مسح جلسة المستخدم"""
        if user_id in self.sessions:
            self.sessions[user_id].clear_context()
    
    def cleanup_expired_sessions(self):
        """تنظيف الجلسات المنتهية الصلاحية"""
        expired_users = []
        for user_id, session in self.sessions.items():
            if session.is_expired(self.session_timeout):
                expired_users.append(user_id)
        
        for user_id in expired_users:
            del self.sessions[user_id]
    
    def get_active_sessions_count(self) -> int:
        """عدد الجلسات النشطة"""
        self.cleanup_expired_sessions()
        return len(self.sessions)
    
    def get_session_stats(self) -> Dict[str, Any]:
        """إحصائيات الجلسات"""
        self.cleanup_expired_sessions()
        
        states_count = {}
        for session in self.sessions.values():
            state = session.state.value
            states_count[state] = states_count.get(state, 0) + 1
        
        return {
            "total_active": len(self.sessions),
            "states_distribution": states_count,
            "average_history_length": sum(len(s.conversation_history) for s in self.sessions.values()) / max(1, len(self.sessions))
        }