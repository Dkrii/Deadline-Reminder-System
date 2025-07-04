"""
Task model - Base class for all tasks
"""

from datetime import datetime, date, time
from abc import ABC, abstractmethod
import uuid

class BaseTask(ABC):
    """Abstract base class for all tasks"""
    
    def __init__(self, title: str, description: str = "", deadline_date: date = None, 
                 deadline_time: time = None, priority: int = 2, category: str = "lainnya"):
        self.task_id = str(uuid.uuid4())
        self.title = title
        self.description = description
        self.deadline_date = deadline_date or date.today()
        self.deadline_time = deadline_time
        self.priority = priority  # 1=High, 2=Medium, 3=Low
        self.category = category.lower()
        self.completed = False
        self.created_at = datetime.now()
        self.completed_at = None
    
    @abstractmethod
    def get_urgency_level(self) -> str:
        """Calculate urgency level - must be implemented by subclasses"""
        pass
    
    def mark_completed(self):
        """Mark task as completed"""
        self.completed = True
        self.completed_at = datetime.now()
    
    def get_priority_text(self) -> str:
        """Get priority as text"""
        priority_map = {1: "Tinggi", 2: "Sedang", 3: "Rendah"}
        return priority_map.get(self.priority, "Sedang")
    
    def get_days_until_deadline(self) -> int:
        """Get number of days until deadline"""
        return (self.deadline_date - date.today()).days
    
    def is_overdue(self) -> bool:
        """Check if task is overdue"""
        if self.completed:
            return False
        
        if self.deadline_date < date.today():
            return True
        
        if self.deadline_date == date.today() and self.deadline_time:
            current_time = datetime.now().time()
            return current_time > self.deadline_time
        
        return False
    
    def to_dict(self) -> dict:
        """Convert task to dictionary for JSON serialization"""
        return {
            'task_id': self.task_id,
            'title': self.title,
            'description': self.description,
            'deadline_date': self.deadline_date.isoformat(),
            'deadline_time': self.deadline_time.isoformat() if self.deadline_time else None,
            'priority': self.priority,
            'category': self.category,
            'completed': self.completed,
            'created_at': self.created_at.isoformat(),
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'task_type': self.__class__.__name__
        }
    
    @classmethod
    def from_dict(cls, data: dict):
        """Create task from dictionary"""
        task = cls(
            title=data['title'],
            description=data['description'],
            deadline_date=date.fromisoformat(data['deadline_date']),
            deadline_time=time.fromisoformat(data['deadline_time']) if data['deadline_time'] else None,
            priority=data['priority'],
            category=data['category']
        )
        
        task.task_id = data['task_id']
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed_at = datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        
        return task
    
    def __str__(self):
        status = "✅" if self.completed else "⏳"
        return f"{status} {self.title} - {self.deadline_date} ({self.get_priority_text()})"
    
    def __repr__(self):
        return f"Task(id={self.task_id[:8]}, title='{self.title}', deadline={self.deadline_date})"


class RegularTask(BaseTask):
    """Regular task implementation"""
    
    def get_urgency_level(self) -> str:
        """Calculate urgency level based on days until deadline and priority"""
        if self.completed:
            return "completed"
        
        if self.is_overdue():
            return "overdue"
        
        days_left = self.get_days_until_deadline()
        
        # High priority tasks
        if self.priority == 1:
            if days_left <= 1:
                return "critical"
            elif days_left <= 3:
                return "high"
            else:
                return "medium"
        
        # Medium priority tasks
        elif self.priority == 2:
            if days_left <= 0:
                return "critical"
            elif days_left <= 2:
                return "high"
            elif days_left <= 5:
                return "medium"
            else:
                return "low"
        
        # Low priority tasks
        else:
            if days_left <= 0:
                return "high"
            elif days_left <= 3:
                return "medium"
            else:
                return "low"


class RecurringTask(BaseTask):
    """Recurring task implementation"""
    
    def __init__(self, title: str, description: str = "", deadline_date: date = None,
                 deadline_time: time = None, priority: int = 2, category: str = "lainnya",
                 recurrence_type: str = "daily", recurrence_count: int = 1):
        super().__init__(title, description, deadline_date, deadline_time, priority, category)
        self.recurrence_type = recurrence_type  # daily, weekly, monthly
        self.recurrence_count = recurrence_count  # every X days/weeks/months
        self.original_deadline = deadline_date
    
    def get_urgency_level(self) -> str:
        """Recurring tasks have slightly different urgency calculation"""
        base_urgency = super().get_urgency_level()
        
        # Recurring tasks are generally less urgent since they repeat
        if base_urgency == "critical":
            return "high"
        elif base_urgency == "high":
            return "medium"
        else:
            return base_urgency
    
    def get_next_deadline(self) -> date:
        """Calculate next deadline based on recurrence"""
        from datetime import timedelta
        
        if self.recurrence_type == "daily":
            return self.deadline_date + timedelta(days=self.recurrence_count)
        elif self.recurrence_type == "weekly":
            return self.deadline_date + timedelta(weeks=self.recurrence_count)
        elif self.recurrence_type == "monthly":
            # Approximate month calculation
            return self.deadline_date + timedelta(days=30 * self.recurrence_count)
        else:
            return self.deadline_date
    
    def reset_for_next_cycle(self):
        """Reset task for next recurrence cycle"""
        self.deadline_date = self.get_next_deadline()
        self.completed = False
        self.completed_at = None
    
    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'recurrence_type': self.recurrence_type,
            'recurrence_count': self.recurrence_count,
            'original_deadline': self.original_deadline.isoformat()
        })
        return data
    
    @classmethod
    def from_dict(cls, data: dict):
        task = cls(
            title=data['title'],
            description=data['description'],
            deadline_date=date.fromisoformat(data['deadline_date']),
            deadline_time=time.fromisoformat(data['deadline_time']) if data['deadline_time'] else None,
            priority=data['priority'],
            category=data['category'],
            recurrence_type=data.get('recurrence_type', 'daily'),
            recurrence_count=data.get('recurrence_count', 1)
        )
        
        task.task_id = data['task_id']
        task.completed = data['completed']
        task.created_at = datetime.fromisoformat(data['created_at'])
        task.completed_at = datetime.fromisoformat(data['completed_at']) if data['completed_at'] else None
        task.original_deadline = date.fromisoformat(data.get('original_deadline', data['deadline_date']))
        
        return task