"""
Reminder System - Handles notifications and reminders (Inheritance example)
"""

from datetime import datetime, date, timedelta
from typing import List, Dict
from models.task import BaseTask
from models.task_manager import TaskManager

class BaseReminder:
    """Base class for all reminder types"""
    
    def __init__(self, task_manager: TaskManager):
        self.task_manager = task_manager
        self.reminder_settings = {
            'urgent_threshold': 0,  # days
            'upcoming_threshold': 3,  # days  
            'enable_sound': False,
            'enable_notifications': True
        }
    
    def get_tasks_by_urgency(self, urgency_level: str) -> List[BaseTask]:
        """Get tasks by urgency level"""
        tasks = self.task_manager.get_pending_tasks()
        return [task for task in tasks if task.get_urgency_level() == urgency_level]
    
    def update_settings(self, **kwargs):
        """Update reminder settings"""
        for key, value in kwargs.items():
            if key in self.reminder_settings:
                self.reminder_settings[key] = value


class ReminderSystem(BaseReminder):
    """Main reminder system - inherits from BaseReminder"""
    
    def __init__(self, task_manager: TaskManager):
        super().__init__(task_manager)
        self.notification_history = []
    
    def get_urgent_reminders(self) -> List[BaseTask]:
        """Get urgent reminders (due today or overdue)"""
        today = date.today()
        urgent_tasks = []
        
        # Get today's tasks
        today_tasks = [
            task for task in self.task_manager.get_pending_tasks()
            if task.deadline_date == today
        ]
        
        # Get overdue tasks
        overdue_tasks = self.task_manager.get_overdue_tasks()
        
        urgent_tasks.extend(today_tasks)
        urgent_tasks.extend(overdue_tasks)
        
        # Remove duplicates
        seen_ids = set()
        unique_urgent = []
        for task in urgent_tasks:
            if task.task_id not in seen_ids:
                unique_urgent.append(task)
                seen_ids.add(task.task_id)
        
        return sorted(unique_urgent, key=lambda t: (t.deadline_date, t.priority))
    
    def get_upcoming_reminders(self) -> List[BaseTask]:
        """Get upcoming reminders (within threshold days)"""
        threshold = self.reminder_settings['upcoming_threshold']
        upcoming_tasks = self.task_manager.get_upcoming_tasks(days=threshold)
        
        # Exclude today's tasks (they're in urgent)
        today = date.today()
        return [task for task in upcoming_tasks if task.deadline_date != today]
    
    def get_overdue_reminders(self) -> List[BaseTask]:
        """Get overdue reminders"""
        return self.task_manager.get_overdue_tasks()
    
    def get_priority_reminders(self, priority: int) -> List[BaseTask]:
        """Get reminders by priority level"""
        pending_tasks = self.task_manager.get_pending_tasks()
        return [task for task in pending_tasks if task.priority == priority]
    
    def get_category_reminders(self, category: str) -> List[BaseTask]:
        """Get reminders by category"""
        pending_tasks = self.task_manager.get_pending_tasks()
        return [task for task in pending_tasks if task.category.lower() == category.lower()]
    
    def create_daily_summary(self) -> Dict:
        """Create daily summary of tasks and reminders"""
        today = date.today()
        
        summary = {
            'date': today.isoformat(),
            'urgent_count': len(self.get_urgent_reminders()),
            'upcoming_count': len(self.get_upcoming_reminders()),
            'overdue_count': len(self.get_overdue_reminders()),
            'total_pending': len(self.task_manager.get_pending_tasks()),
            'today_tasks': self.task_manager.get_tasks_by_date(today),
            'high_priority_pending': len(self.get_priority_reminders(1)),
            'completion_rate': self.task_manager.get_statistics()['completion_rate']
        }
        
        return summary
    
    def get_weekly_outlook(self) -> List[Dict]:
        """Get 7-day outlook of tasks"""
        outlook = []
        today = date.today()
        
        for i in range(7):
            target_date = today + timedelta(days=i)
            day_tasks = self.task_manager.get_tasks_by_date(target_date)
            
            outlook.append({
                'date': target_date.isoformat(),
                'day_name': target_date.strftime('%A'),
                'is_today': target_date == today,
                'task_count': len(day_tasks),
                'tasks': day_tasks,
                'has_high_priority': any(task.priority == 1 for task in day_tasks)
            })
        
        return outlook
    
    def generate_reminder_message(self, reminder_type: str = "daily") -> str:
        """Generate formatted reminder message"""
        if reminder_type == "daily":
            return self._generate_daily_message()
        elif reminder_type == "urgent":
            return self._generate_urgent_message()
        elif reminder_type == "weekly":
            return self._generate_weekly_message()
        else:
            return "No reminders available."
    
    def _generate_daily_message(self) -> str:
        """Generate daily reminder message"""
        summary = self.create_daily_summary()
        message = []
        
        message.append("🌅 DAILY REMINDER")
        message.append("=" * 30)
        message.append(f"📅 {datetime.now().strftime('%A, %B %d, %Y')}")
        
        if summary['urgent_count'] > 0:
            message.append(f"\n🚨 URGENT: {summary['urgent_count']} task(s) need immediate attention!")
        
        if summary['today_tasks']:
            message.append(f"\n📝 Today's Tasks ({len(summary['today_tasks'])}):")
            for task in summary['today_tasks'][:5]:  # Show max 5
                time_str = task.deadline_time.strftime("%H:%M") if task.deadline_time else ""
                message.append(f"   • {task.title} {time_str}")
            
            if len(summary['today_tasks']) > 5:
                message.append(f"   ... and {len(summary['today_tasks']) - 5} more")
        
        if summary['upcoming_count'] > 0:
            message.append(f"\n⏰ Upcoming: {summary['upcoming_count']} task(s) in next 3 days")
        
        if summary['overdue_count'] > 0:
            message.append(f"\n❗ Overdue: {summary['overdue_count']} task(s) need attention")
        
        message.append(f"\n📊 Completion Rate: {summary['completion_rate']:.1f}%")
        
        return "\n".join(message)
    
    def _generate_urgent_message(self) -> str:
        """Generate urgent reminder message"""
        urgent_tasks = self.get_urgent_reminders()
        
        if not urgent_tasks:
            return "✅ No urgent tasks at the moment!"
        
        message = []
        message.append("🚨 URGENT REMINDERS")
        message.append("=" * 30)
        
        for task in urgent_tasks[:10]:  # Show max 10 urgent tasks
            status = "OVERDUE" if task.is_overdue() else "DUE TODAY"
            time_str = task.deadline_time.strftime(" at %H:%M") if task.deadline_time else ""
            message.append(f"❗ {status}: {task.title}{time_str}")
        
        if len(urgent_tasks) > 10:
            message.append(f"\n... and {len(urgent_tasks) - 10} more urgent tasks")
        
        return "\n".join(message)
    
    def _generate_weekly_message(self) -> str:
        """Generate weekly outlook message"""
        outlook = self.get_weekly_outlook()
        
        message = []
        message.append("📅 WEEKLY OUTLOOK")
        message.append("=" * 30)
        
        for day_info in outlook:
            day_name = day_info['day_name']
            task_count = day_info['task_count']
            
            if day_info['is_today']:
                day_name += " (TODAY)"
            
            priority_indicator = " 🔥" if day_info['has_high_priority'] else ""
            message.append(f"{day_name}: {task_count} task(s){priority_indicator}")
        
        return "\n".join(message)
    
    def log_notification(self, notification_type: str, message: str):
        """Log notification to history"""
        self.notification_history.append({
            'timestamp': datetime.now().isoformat(),
            'type': notification_type,
            'message': message
        })
        
        # Keep only last 100 notifications
        if len(self.notification_history) > 100:
            self.notification_history = self.notification_history[-100:]
    
    def get_notification_history(self, limit: int = 20) -> List[Dict]:
        """Get notification history"""
        return self.notification_history[-limit:] if self.notification_history else []


class SmartReminder(ReminderSystem):
    """Advanced reminder system with smart features - demonstrates polymorphism"""
    
    def __init__(self, task_manager: TaskManager):
        super().__init__(task_manager)
        self.learning_data = {
            'completion_patterns': {},
            'category_preferences': {},
            'time_preferences': {}
        }
    
    def get_smart_recommendations(self) -> List[str]:
        """Get smart recommendations based on user patterns"""
        recommendations = []
        stats = self.task_manager.get_statistics()
        
        # Analyze completion rate
        if stats['completion_rate'] < 70:
            recommendations.append("💡 Consider breaking large tasks into smaller ones")
        
        # Analyze overdue tasks
        if stats['overdue'] > 3:
            recommendations.append("⚠️ You have many overdue tasks. Consider rescheduling or prioritizing")
        
        # Analyze category distribution
        category_stats = stats['by_category']
        if len(category_stats) == 1:
            recommendations.append("📋 Try categorizing your tasks for better organization")
        
        # Analyze priority distribution
        priority_stats = stats['by_priority']
        if priority_stats[1] > priority_stats[2] + priority_stats[3]:
            recommendations.append("🎯 Consider if all high-priority tasks are truly urgent")
        
        return recommendations
    
    def get_optimal_schedule_suggestion(self) -> Dict:
        """Suggest optimal task scheduling"""
        pending_tasks = self.task_manager.get_pending_tasks()
        high_priority = [t for t in pending_tasks if t.priority == 1]
        
        suggestion = {
            'morning_tasks': [],
            'afternoon_tasks': [],
            'evening_tasks': []
        }
        
        # Simple scheduling logic
        for task in high_priority[:3]:
            suggestion['morning_tasks'].append(task.title)
        
        medium_priority = [t for t in pending_tasks if t.priority == 2]
        for task in medium_priority[:2]:
            suggestion['afternoon_tasks'].append(task.title)
        
        low_priority = [t for t in pending_tasks if t.priority == 3]
        for task in low_priority[:1]:
            suggestion['evening_tasks'].append(task.title)
        
        return suggestion
    
    def analyze_productivity_trends(self) -> Dict:
        """Analyze user's productivity trends"""
        completed_tasks = self.task_manager.get_completed_tasks()
        
        if not completed_tasks:
            return {'message': 'Not enough data for analysis'}
        
        # Analyze completion by category
        category_completion = {}
        for task in completed_tasks:
            category = task.category
            category_completion[category] = category_completion.get(category, 0) + 1
        
        # Find most productive category
        most_productive_category = max(category_completion.items(), key=lambda x: x[1]) if category_completion else None
        
        return {
            'total_completed': len(completed_tasks),
            'category_breakdown': category_completion,
            'most_productive_category': most_productive_category[0] if most_productive_category else None,
            'average_completion_time': 'Analysis not implemented',  # Could be enhanced
            'suggestions': self.get_smart_recommendations()
        }