import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import threading
import time
from plyer import notification

class TaskScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler")
        
        self.task_label = tk.Label(root, text="Enter Task:" , fg='purple')
        self.task_label.grid(row=0, column=0, padx=10, pady=10)
        
        self.task_entry = tk.Entry(root, width=50)
        self.task_entry.grid(row=0, column=1, padx=10, pady=10 )
        
        self.time_label = tk.Label(root, text="Enter Time (YYYY-MM-DD HH:MM:SS):" , fg='purple')
        self.time_label.grid(row=1, column=0, padx=10, pady=10 )
        
        self.time_entry = tk.Entry(root, width=50)
        self.time_entry.grid(row=1, column=1, padx=10, pady=10 )
        
        self.schedule_button = tk.Button(root, text="Schedule Task", command=self.schedule_task , bg = 'light grey' , fg='green')
        self.schedule_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        self.task_listbox = tk.Listbox(root, width=80 , fg='blue')
        self.task_listbox.grid(row=3, column=0 , columnspan=2, padx=10, pady=10 )
        
        self.edit_button = tk.Button(root, text="Edit Task", command=self.edit_selected_task , fg='green')
        self.edit_button.grid(row=4, column=0, padx=10, pady=10)
        
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_selected_task , fg='red')
        self.delete_button.grid(row=4, column=1, padx=10, pady=10)
        
        self.tasks = []
        self.task_index_to_edit = None
    
    def schedule_task(self):
        task = self.task_entry.get()
        time_str = self.time_entry.get()
        
        try:
            scheduled_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
            current_time = datetime.now()
            if scheduled_time >= current_time:
                if self.task_index_to_edit is not None:
                    # If editing, update the existing task
                    self.tasks[self.task_index_to_edit] = (task, scheduled_time)
                    self.task_index_to_edit = None  # Reset the edit index
                else:
                    # If not editing, add a new task
                    self.tasks.append((task, scheduled_time))
                self.task_entry.delete(0, tk.END)
                self.time_entry.delete(0, tk.END)
                messagebox.showinfo("Task Scheduler", "Task scheduled successfully!")
                threading.Thread(target=self.wait_and_notify, args=(task, scheduled_time)).start()
                self.update_task_listbox()
            else:
                messagebox.showerror("Task Scheduler", "Scheduled time must be in the future.")
        except ValueError:
            messagebox.showerror("Task Scheduler", "Invalid date-time format. Please use YYYY-MM-DD HH:MM:SS.")
    
    def wait_and_notify(self, task, scheduled_time):
        time_difference = (scheduled_time - datetime.now()).total_seconds()
        time.sleep(time_difference)
        notification.notify(
            title="Task Reminder",
            message=task,
            app_name="Task Scheduler",
            timeout=10
        )
        
    def delete_selected_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            del self.tasks[index]
            self.update_task_listbox()
            messagebox.showinfo("Task Scheduler", "Task deleted successfully!")
        else:
            messagebox.showerror("Task Scheduler", "Please select a task to delete.")
    
    def edit_selected_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            index = int(selected_index[0])
            task, scheduled_time = self.tasks[index]
            self.task_entry.delete(0, tk.END)
            self.time_entry.delete(0, tk.END)
            self.task_entry.insert(0, task)
            self.time_entry.insert(0, scheduled_time.strftime("%Y-%m-%d %H:%M:%S"))
            self.task_index_to_edit = index
            messagebox.showinfo("Task Scheduler", "Editing task. Please modify and click 'Schedule Task'.")
        else:
            messagebox.showerror("Task Scheduler", "Please select a task to edit.")
    
    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task, scheduled_time in self.tasks:
            self.task_listbox.insert(tk.END, f"{task} - {scheduled_time.strftime('%Y-%m-%d %H:%M:%S')}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskScheduler(root)
    root.mainloop()
