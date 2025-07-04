# deadline-reminder-system
# 📅 Deadline Reminder System

## About the Application

**This application was inspired by my habit of often forgetting schedules and deadlines!**

As an active student with various college assignments, projects, and personal activities, I often struggle to remember all the deadlines I need to meet. Often I only remember when the deadline is very close or has already passed. This experience made me feel the need to have a more organized and personal reminder system.

From that experience, the idea was born to create a **Deadline Reminder System** - a Python-based application that helps manage and remind various deadlines more effectively. This application is not just an ordinary to-do list, but is equipped with a smart priority system, categorization, and reminder features.

## ✨ Main Features

### 🎯 Task Management
- **Add New Tasks** with deadlines, time, priority, and category
- **View Tasks** by date (today, upcoming, all)
- **Mark Tasks Complete** with completion time tracking
- **Delete Tasks** that are no longer needed
- **Search Tasks** by title or description

### 🔔 Reminder System
- **Urgent Reminders** for today's tasks and overdue ones
- **Upcoming Reminders** for tasks in the next 3 days
- **Overdue Notifications** for missed tasks
- **Daily Summary** with complete statistics

### 📊 Analysis & Statistics
- **Task Completion Rate**
- **Breakdown by Category** (college, work, personal)
- **Priority Analysis** (high, medium, low)
- **Overdue Task Tracking**

### 💾 Data Storage
- **JSON Database** for data persistence
- **Auto-save** every change
- **Export Tasks** to text files
- **Backup & Recovery** data

## 🏗️ OOP Architecture

### 📦 Class Structure

#### 1. **Abstract Base Class**
```python
class BaseTask(ABC):
    # Abstract method that must be implemented
    @abstractmethod
    def get_urgency_level(self) -> str:
        pass
```

#### 2. **Inheritance Relationship**
```python
class RegularTask(BaseTask):      # Regular task
class RecurringTask(BaseTask):    # Recurring task
```

#### 3. **Polymorphism Implementation**
```python
class BaseReminder:               # Base reminder
class ReminderSystem(BaseReminder):     # Standard reminder
class SmartReminder(ReminderSystem):    # Advanced reminder
```

#### 4. **Task Management**
```python
class TaskManager:
    # Manages all CRUD task operations
    # Handle data persistence (JSON)
    # Provide statistics and analytics
```

### 🔗 Inter-Class Relations
- **TaskManager** ↔ **BaseTask** (Composition)
- **ReminderSystem** ↔ **TaskManager** (Dependency)
- **BaseTask** → **RegularTask/RecurringTask** (Inheritance)
- **BaseReminder** → **ReminderSystem** → **SmartReminder** (Inheritance Chain)

## 📁 Project Structure

```
deadline_reminder_system/
├── main.py                 # Application entry point
├── models/                 # Package for all classes
│   ├── __init__.py
│   ├── task.py            # BaseTask, RegularTask, RecurringTask
│   ├── task_manager.py    # TaskManager class
│   └── reminder_system.py # Reminder classes
├── data/                  # Data storage folder
│   └── tasks.json        # JSON database (auto-generated)
├── README.md             # This documentation
└── demo.mp4             # Demo video (to be created)
```

## 🚀 How to Run

### 1. **Environment Setup**
```bash
# Clone or download project
git clone <repository-url>
cd deadline_reminder_system

# Ensure Python 3.7+ is installed
python --version
```

### 2. **Running the Application**
```bash
# Run the application
python main.py

# Or with python3 (for Linux/Mac)
python3 main.py
```

### 3. **Menu Navigation**
- Use numbers **1-9** to select menu options
- Follow the instructions that appear on screen
- Data will automatically be saved to `data/tasks.json`

## 📝 Usage Examples

### Adding a New Task
```
1. Select menu "1. Add New Task"
2. Enter title: "OOP Final Project"
3. Enter description: "Work on deadline reminder project"
4. Enter deadline: "2024-12-15"
5. Enter time: "23:59"
6. Select priority: "1" (High)
7. Enter category: "college"
```

### Check Reminders
```
1. Select menu "7. Check Reminders"
2. System will display:
   - Urgent tasks (today/overdue)
   - Upcoming tasks (next 3 days)
   - Overdue tasks
```

## 🎨 OOP Concepts Implementation

### 1. **Encapsulation**
- Task data stored as private attributes
- Accessor methods to access data
- Validation at class method level

### 2. **Inheritance**
- `RegularTask` and `RecurringTask` inherit from `BaseTask`
- `ReminderSystem` inherits from `BaseReminder`
- `SmartReminder` inherits from `ReminderSystem`

### 3. **Polymorphism**
- `get_urgency_level()` method implemented differently in each subclass
- Reminder system can operate with various task types
- Same interface for different reminder types

### 4. **Abstraction**
- `BaseTask` as abstract class with abstract methods
- Clear interface for task management operations
- Hiding complexity from user interface

## 📊 Database Schema (JSON)

```json
{
  "tasks": [
    {
      "task_id": "uuid-string",
      "title": "string",
      "description": "string", 
      "deadline_date": "YYYY-MM-DD",
      "deadline_time": "HH:MM:SS",
      "priority": 1-3,
      "category": "string",
      "completed": boolean,
      "created_at": "ISO datetime",
      "completed_at": "ISO datetime",
      "task_type": "RegularTask|RecurringTask"
    }
  ],
  "last_updated": "ISO datetime"
}
```

## 🎯 Learning Outcomes

Through this project, I learned:

1. **Practical OOP Implementation**
   - Using inheritance for code reusability
   - Implementing polymorphism in real cases
   - Abstract classes for enforcing interfaces

2. **Data Persistence**
   - JSON serialization/deserialization
   - File handling and error management
   - Data backup and recovery

3. **User Experience Design**
   - User-friendly CLI interface
   - Error handling and validation
   - Clear navigation and feedback

4. **Project Organization**
   - Modular code structure
   - Package management
   - Documentation and testing

## 🚀 Future Enhancements

- [ ] **GUI Interface** with tkinter or PyQt
- [ ] **Database Integration** (SQLite/PostgreSQL)
- [ ] **Web Interface** with Flask/Django
- [ ] **Mobile App** with Kivy
- [ ] **Email Notifications**
- [ ] **Calendar Integration**
- [ ] **Task Templates**
- [ ] **Team Collaboration Features**

## 🎥 Demo Video

Application demo video available at: `demo.mp4` (to be created and uploaded)

## 👨‍💻 Developer

**Name:** Dikri Ali 
**Student ID:** 20230040064
**Course:** Object-Oriented Programming (OOP)  

---

**"From personal struggle with deadlines to a working solution - this is how coding solves real-life problems!"** 🎯
