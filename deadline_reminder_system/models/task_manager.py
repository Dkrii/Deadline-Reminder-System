"""
Task Manager - Handles all task operations and data persistence
"""

import json
import os
from datetime import datetime, date, time, timedelta
from typing import List, Dict, Optional
from models.task import BaseTask, RegularTask, RecurringTask

class TaskManager:
    """Manages all tasks and handles data persistence"""
    
    def __init__(self, data_file: str = "data/tasks.json"):
        self.data_file = data_file
        self.tasks: List[BaseTask] = []
        self._ensure_data_directory()
    
    def _ensure_data_directory(self):
        """Create data directory if it doesn't exist"""
        data_dir = os.path.dirname(self.data_file)
        if data_dir and not os.path.exists(data_dir):
            os.makedirs(data_dir)
    
    def add_task(self, title: str, description: str = "", deadline_date: date = None,
                 deadline_time: time = None, priority: int = 2, category: str = "lainnya",
                 task_type: str = "regular", **kwargs) -> bool:
        """Add a new task"""
        try:
            if task_type == "recurring":
                task = RecurringTask(
                    title=title,
                    description=description,
                    deadline_date=deadline_date,
                    deadline_time=deadline_time,
                    priority=priority,
                    category=category,
                    recurrence_type=kwargs.get('recurrence_type', 'daily'),
                    recurrence_count=kwargs.get('recurrence_count', 1)
                )
            else:
                task = RegularTask(
                    title=title,
                    description=description,
                    deadline_date=deadline_date,
                    deadline_time=deadline_time,
                    priority=priority,
                    category=category
                )
            
            self.tasks.append(task)
            self.save_data()
            return True
        except Exception as e:
            print(f"Error adding task: {e}")
            return False
    
    def get_all_tasks(self) -> List[BaseTask]:
        """Get all tasks sorted by deadline"""
        return sorted(self.tasks, key=lambda t: (t.deadline_date, t.deadline_time or time.min))
    
    def get_task_by_id(self, task_id: str) -> Optional[BaseTask]:
        """Get task by ID"""
        for task in self.tasks:
            if task.task_id == task_id:
                return task
        return None
    
    def get_tasks_by_date(self, target_date: date) -> List[BaseTask]:
        """Get tasks for a specific date"""
        return [task for task in self.tasks if task.deadline_date == target_date]
    
    def get_upcoming_tasks(self, days: int = 7) -> List[BaseTask]:
        """Get tasks in the next X days"""
        today = date.today()
        future_date = today + timedelta(days=days)
        
        upcoming = [
            task for task in self.tasks 
            if today <= task.deadline_date <= future_date and not task.completed
        ]
        
        return sorted(upcoming, key=lambda t: (t.deadline_date, t.deadline_time or time.min))
    
    def get_overdue_tasks(self) -> List[BaseTask]:
        """Get overdue tasks"""
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_completed_tasks(self) -> List[BaseTask]:
        """Get completed tasks"""
        return [task for task in self.tasks if task.completed]
    
    def get_pending_tasks(self) -> List[BaseTask]:
        """Get pending (not completed) tasks"""
        return [task for task in self.tasks if not task.completed]
    
    def get_tasks_by_category(self, category: str) -> List[BaseTask]:
        """Get tasks by category"""
        return [task for task in self.tasks if task.category.lower() == category.lower()]
    
    def get_tasks_by_priority(self, priority: int) -> List[BaseTask]:
        """Get tasks by priority level"""
        return [task for task in self.tasks if task.priority == priority]
    
    def mark_completed(self, task_id: str) -> bool:
        """Mark a task as completed"""
        task = self.get_task_by_id(task_id)
        if task:
            task.mark_completed()
            
            # If it's a recurring task, create next occurrence
            if isinstance(task, RecurringTask):
                self._handle_recurring_task_completion(task)
            
            self.save_data()
            return True
        return False
    
    def _handle_recurring_task_completion(self, recurring_task: RecurringTask):
        """Handle completion of a recurring task"""
        # Create a new task for the next occurrence
        next_task = RecurringTask(
            title=recurring_task.title,
            description=recurring_task.description,
            deadline_date=recurring_task.get_next_deadline(),
            deadline_time=recurring_task.deadline_time,
            priority=recurring_task.priority,
            category=recurring_task.category,
            recurrence_type=recurring_task.recurrence_type,
            recurrence_count=recurring_task.recurrence_count
        )
        self.tasks.append(next_task)
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        task = self.get_task_by_id(task_id)
        if task:
            self.tasks.remove(task)
            self.save_data()
            return True
        return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update task properties"""
        task = self.get_task_by_id(task_id)
        if not task:
            return False
        
        try:
            for key, value in kwargs.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            
            self.save_data()
            return True
        except Exception as e:
            print(f"Error updating task: {e}")
            return False
    
    def search_tasks(self, query: str) -> List[BaseTask]:
        """Search tasks by title or description"""
        query = query.lower()
        return [
            task for task in self.tasks 
            if query in task.title.lower() or query in task.description.lower()
        ]
    
    def get_statistics(self) -> Dict:
        """Get task statistics"""
        total_tasks = len(self.tasks)
        completed_tasks = len(self.get_completed_tasks())
        pending_tasks = len(self.get_pending_tasks())
        overdue_tasks = len(self.get_overdue_tasks())
        
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Statistics by category
        category_stats = {}
        for task in self.tasks:
            category = task.category
            category_stats[category] = category_stats.get(category, 0) + 1
        
        # Statistics by priority
        priority_stats = {1: 0, 2: 0, 3: 0}
        for task in self.tasks:
            priority_stats[task.priority] += 1
        
        return {
            'total': total_tasks,
            'completed': completed_tasks,
            'pending': pending_tasks,
            'overdue': overdue_tasks,
            'completion_rate': completion_rate,
            'by_category': category_stats,
            'by_priority': priority_stats
        }
    
    def save_data(self):
        """Save tasks to JSON file"""
        try:
            data = {
                'tasks': [task.to_dict() for task in self.tasks],
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_data(self):
        """Load tasks from JSON file"""
        if not os.path.exists(self.data_file):
            return
        
        try:
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.tasks = []
            for task_data in data.get('tasks', []):
                task_type = task_data.get('task_type', 'RegularTask')
                
                if task_type == 'RecurringTask':
                    task = RecurringTask.from_dict(task_data)
                else:
                    task = RegularTask.from_dict(task_data)
                
                self.tasks.append(task)
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.tasks = []
    
    def export_tasks(self, filename: str = None) -> str:
        """Export tasks to a formatted text file"""
        if not filename:
            filename = f"task_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("DEADLINE REMINDER SYSTEM - TASK EXPORT\n")
                f.write("=" * 50 + "\n")
                f.write(f"Exported on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                stats = self.get_statistics()
                f.write(f"Total Tasks: {stats['total']}\n")
                f.write(f"Completed: {stats['completed']}\n")
                f.write(f"Pending: {stats['pending']}\n")
                f.write(f"Overdue: {stats['overdue']}\n\n")
                
                f.write("ALL TASKS:\n")
                f.write("-" * 50 + "\n")
                
                for task in self.get_all_tasks():
                    f.write(f"Title: {task.title}\n")
                    f.write(f"Description: {task.description}\n")
                    f.write(f"Deadline: {task.deadline_date}")
                    if task.deadline_time:
                        f.write(f" {task.deadline_time}")
                    f.write(f"\nPriority: {task.get_priority_text()}\n")
                    f.write(f"Category: {task.category.title()}\n")
                    f.write(f"Status: {'Completed' if task.completed else 'Pending'}\n")
                    f.write(f"Urgency: {task.get_urgency_level()}\n")
                    f.write("-" * 30 + "\n")
            
            return filename
        except Exception as e:
            print(f"Error exporting tasks: {e}")
            return None
    
    def cleanup_completed_tasks(self, days_old: int = 30) -> int:
        """Remove completed tasks older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        initial_count = len(self.tasks)
        self.tasks = [
            task for task in self.tasks 
            if not (task.completed and task.completed_at and task.completed_at < cutoff_date)
        ]
        
        removed_count = initial_count - len(self.tasks)
        if removed_count > 0:
            self.save_data()
        
        return removed_count