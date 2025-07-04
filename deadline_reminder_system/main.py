#!/usr/bin/env python3
"""
Deadline Reminder System
Main application file
"""

import os
import sys
from datetime import datetime, timedelta
from models.task_manager import TaskManager
from models.reminder_system import ReminderSystem

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_menu():
    """Display main menu"""
    print("\n" + "="*50)
    print("    📅 DEADLINE REMINDER SYSTEM")
    print("="*50)
    print("1. Tambah Task Baru")
    print("2. Lihat Semua Task")
    print("3. Lihat Task Hari Ini")
    print("4. Lihat Task Mendatang")
    print("5. Tandai Task Selesai")
    print("6. Hapus Task")
    print("7. Cek Reminder")
    print("8. Statistik Task")
    print("9. Keluar")
    print("="*50)

def get_task_input():
    """Get task input from user"""
    print("\n--- Tambah Task Baru ---")
    title = input("Judul task: ").strip()
    if not title:
        print("❌ Judul tidak boleh kosong!")
        return None
    
    description = input("Deskripsi (opsional): ").strip()
    
    # Get deadline date
    while True:
        try:
            date_input = input("Deadline (YYYY-MM-DD): ").strip()
            deadline_date = datetime.strptime(date_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("❌ Format tanggal salah! Gunakan format YYYY-MM-DD")
    
    # Get deadline time
    while True:
        try:
            time_input = input("Waktu deadline (HH:MM, opsional): ").strip()
            if not time_input:
                deadline_time = None
                break
            deadline_time = datetime.strptime(time_input, "%H:%M").time()
            break
        except ValueError:
            print("❌ Format waktu salah! Gunakan format HH:MM")
    
    # Get priority
    while True:
        try:
            priority_input = input("Prioritas (1=Tinggi, 2=Sedang, 3=Rendah): ").strip()
            priority = int(priority_input)
            if priority in [1, 2, 3]:
                break
            else:
                print("❌ Prioritas harus 1, 2, atau 3!")
        except ValueError:
            print("❌ Prioritas harus berupa angka!")
    
    # Get category
    category = input("Kategori (kuliah/kerja/pribadi/lainnya): ").strip().lower()
    if not category:
        category = "lainnya"
    
    return {
        'title': title,
        'description': description,
        'deadline_date': deadline_date,
        'deadline_time': deadline_time,
        'priority': priority,
        'category': category
    }

def display_tasks(tasks, title="Task List"):
    """Display tasks in formatted table"""
    if not tasks:
        print(f"\n📝 {title}: Tidak ada task")
        return
    
    print(f"\n📝 {title}:")
    print("-" * 80)
    print(f"{'No':<3} {'Judul':<25} {'Deadline':<12} {'Waktu':<8} {'Prior':<5} {'Status':<10}")
    print("-" * 80)
    
    for i, task in enumerate(tasks, 1):
        deadline_str = task.deadline_date.strftime("%Y-%m-%d")
        time_str = task.deadline_time.strftime("%H:%M") if task.deadline_time else "-"
        priority_str = task.get_priority_text()
        status_str = "✅ Selesai" if task.completed else "⏳ Belum"
        
        print(f"{i:<3} {task.title[:24]:<25} {deadline_str:<12} {time_str:<8} {priority_str:<5} {status_str:<10}")
    print("-" * 80)

def main():
    """Main application function"""
    # Initialize system
    task_manager = TaskManager()
    reminder_system = ReminderSystem(task_manager)
    
    # Load existing data
    task_manager.load_data()
    
    print("🎉 Selamat datang di Deadline Reminder System!")
    print("Aplikasi ini terinspirasi dari kebiasaan saya yang sering lupa jadwal dan deadline!")
    
    while True:
        try:
            display_menu()
            choice = input("\nPilih menu (1-9): ").strip()
            
            if choice == '1':
                # Add new task
                clear_screen()
                task_data = get_task_input()
                if task_data:
                    if task_manager.add_task(**task_data):
                        print("✅ Task berhasil ditambahkan!")
                    else:
                        print("❌ Gagal menambahkan task!")
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '2':
                # View all tasks
                clear_screen()
                all_tasks = task_manager.get_all_tasks()
                display_tasks(all_tasks, "Semua Task")
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '3':
                # View today's tasks
                clear_screen()
                today_tasks = task_manager.get_tasks_by_date(datetime.now().date())
                display_tasks(today_tasks, "Task Hari Ini")
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '4':
                # View upcoming tasks
                clear_screen()
                upcoming_tasks = task_manager.get_upcoming_tasks(days=7)
                display_tasks(upcoming_tasks, "Task 7 Hari Ke Depan")
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '5':
                # Mark task as completed
                clear_screen()
                all_tasks = task_manager.get_all_tasks()
                incomplete_tasks = [t for t in all_tasks if not t.completed]
                
                if not incomplete_tasks:
                    print("📝 Tidak ada task yang belum selesai!")
                else:
                    display_tasks(incomplete_tasks, "Task Yang Belum Selesai")
                    try:
                        task_num = int(input("\nPilih nomor task yang selesai: ")) - 1
                        if 0 <= task_num < len(incomplete_tasks):
                            task_id = incomplete_tasks[task_num].task_id
                            if task_manager.mark_completed(task_id):
                                print("✅ Task berhasil ditandai selesai!")
                            else:
                                print("❌ Gagal menandai task!")
                        else:
                            print("❌ Nomor task tidak valid!")
                    except ValueError:
                        print("❌ Input harus berupa angka!")
                
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '6':
                # Delete task
                clear_screen()
                all_tasks = task_manager.get_all_tasks()
                
                if not all_tasks:
                    print("📝 Tidak ada task untuk dihapus!")
                else:
                    display_tasks(all_tasks, "Semua Task")
                    try:
                        task_num = int(input("\nPilih nomor task yang akan dihapus: ")) - 1
                        if 0 <= task_num < len(all_tasks):
                            task_id = all_tasks[task_num].task_id
                            confirm = input(f"Yakin ingin menghapus '{all_tasks[task_num].title}'? (y/n): ")
                            if confirm.lower() == 'y':
                                if task_manager.delete_task(task_id):
                                    print("✅ Task berhasil dihapus!")
                                else:
                                    print("❌ Gagal menghapus task!")
                        else:
                            print("❌ Nomor task tidak valid!")
                    except ValueError:
                        print("❌ Input harus berupa angka!")
                
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '7':
                # Check reminders
                clear_screen()
                print("🔔 Cek Reminder:")
                print("-" * 50)
                
                urgent_tasks = reminder_system.get_urgent_reminders()
                if urgent_tasks:
                    print("🚨 URGENT - Deadline hari ini:")
                    for task in urgent_tasks:
                        time_str = task.deadline_time.strftime("%H:%M") if task.deadline_time else "Sepanjang hari"
                        print(f"   • {task.title} - {time_str}")
                
                upcoming_reminders = reminder_system.get_upcoming_reminders()
                if upcoming_reminders:
                    print("\n⏰ Deadline dalam 3 hari ke depan:")
                    for task in upcoming_reminders:
                        days_left = (task.deadline_date - datetime.now().date()).days
                        time_str = task.deadline_time.strftime("%H:%M") if task.deadline_time else "Sepanjang hari"
                        print(f"   • {task.title} - {task.deadline_date} {time_str} ({days_left} hari lagi)")
                
                overdue_tasks = reminder_system.get_overdue_reminders()
                if overdue_tasks:
                    print("\n❗ TERLAMBAT:")
                    for task in overdue_tasks:
                        days_overdue = (datetime.now().date() - task.deadline_date).days
                        print(f"   • {task.title} - Terlambat {days_overdue} hari")
                
                if not urgent_tasks and not upcoming_reminders and not overdue_tasks:
                    print("✅ Tidak ada reminder saat ini!")
                
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '8':
                # Statistics
                clear_screen()
                stats = task_manager.get_statistics()
                
                print("📊 Statistik Task:")
                print("-" * 30)
                print(f"Total Task: {stats['total']}")
                print(f"Selesai: {stats['completed']}")
                print(f"Belum Selesai: {stats['pending']}")
                print(f"Terlambat: {stats['overdue']}")
                print(f"Rate Penyelesaian: {stats['completion_rate']:.1f}%")
                
                print("\n📈 Berdasarkan Kategori:")
                for category, count in stats['by_category'].items():
                    print(f"  {category.title()}: {count}")
                
                print("\n🎯 Berdasarkan Prioritas:")
                priority_names = {1: "Tinggi", 2: "Sedang", 3: "Rendah"}
                for priority, count in stats['by_priority'].items():
                    print(f"  {priority_names[priority]}: {count}")
                
                input("\nTekan Enter untuk melanjutkan...")
            
            elif choice == '9':
                # Exit
                print("\n👋 Terima kasih telah menggunakan Deadline Reminder System!")
                print("Jangan lupa cek deadline Anda secara rutin! 😊")
                task_manager.save_data()
                sys.exit(0)
            
            else:
                print("❌ Pilihan tidak valid! Silakan pilih 1-9.")
                input("\nTekan Enter untuk melanjutkan...")
        
        except KeyboardInterrupt:
            print("\n\n👋 Program dihentikan oleh user.")
            task_manager.save_data()
            sys.exit(0)
        except Exception as e:
            print(f"\n❌ Terjadi error: {e}")
            input("\nTekan Enter untuk melanjutkan...")

if __name__ == "__main__":
    main()