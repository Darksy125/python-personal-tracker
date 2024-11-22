import datetime
import customtkinter as ctk
from tkinter import messagebox, ttk
from tkcalendar import Calendar
from src.task import Task
from src.scheduler import Scheduler

class TaskTrackerApp:
    """
    Класс для создания и управления графическим интерфейсом приложения.
    """
    
    def __init__(self, root):
        """
        Инициализация приложения.
        """
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.root = root
        self.root.title("Трекер задач")
        self.root.geometry("800x600")

        self.scheduler = Scheduler()
        self.create_widgets()

    def create_widgets(self):
        """
        Создание всех виджетов интерфейса, включая календарь, кнопки и таблицу задач.
        """
        self.calendar = Calendar(self.root)
        self.calendar.pack(pady=10, fill="both", expand=True)
        self.calendar.bind("<<CalendarSelected>>", self.update_task_display)

        button_frame = ctk.CTkFrame(self.root)
        button_frame.pack(pady=5)

        self.add_task_button = ctk.CTkButton(button_frame, text="Добавить задачу", command=self.add_task)
        self.add_task_button.pack(side="left", padx=5)

        self.edit_task_button = ctk.CTkButton(button_frame, text="Редактировать задачу", command=self.edit_task)
        self.edit_task_button.pack(side="left", padx=5)

        self.delete_task_button = ctk.CTkButton(button_frame, text="Удалить задачу", command=self.delete_task)
        self.delete_task_button.pack(side="left", padx=5)

        self.task_tree = ttk.Treeview(self.root, columns=("Название", "Описание", "Оценка времени", "Время начала", "Время окончания", "Приоритет"), show='headings')
        self.task_tree.pack(fill="both", expand=True)

        for col in self.task_tree["columns"]:
            self.task_tree.heading(col, text=col)
            self.task_tree.column(col, anchor="center", width=100)

        self.update_task_display()

    def add_task(self):
        """
        Открывает диалоговое окно для добавления новой задачи.
        После ввода данных задача добавляется в планировщик и отображается в интерфейсе.
        """
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Добавление задачи")
        dialog.geometry("400x300")
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)
        dialog.grid_rowconfigure(2, weight=1)
        dialog.grid_rowconfigure(3, weight=1)
        dialog.grid_rowconfigure(4, weight=1)
        dialog.grid_rowconfigure(5, weight=1)
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(dialog, text="Название задачи:").grid(row=0, column=0, sticky="ew")
        title_entry = ctk.CTkEntry(dialog)
        title_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Описание:").grid(row=1, column=0, sticky="ew")
        description_entry = ctk.CTkEntry(dialog)
        description_entry.grid(row=1, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Оценка времени (ч):").grid(row=2, column=0, sticky="ew")
        estimated_time_entry = ctk.CTkEntry(dialog)
        estimated_time_entry.grid(row=2, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Приоритет:").grid(row=3, column=0, sticky="ew")
        priority_entry = ctk.CTkEntry(dialog)
        priority_entry.grid(row=3, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Часы начала (0-23):").grid(row=4, column=0, sticky="ew")
        start_hour_entry = ctk.CTkEntry(dialog)
        start_hour_entry.grid(row=4, column=1, sticky="ew")

        def save_task():
            """
            Сохраняет введенную задачу, добавляет её в планировщик и обновляет интерфейс.
            """
            try:
                title = title_entry.get()
                description = description_entry.get()
                estimated_time = float(estimated_time_entry.get())
                start_hour = int(start_hour_entry.get())

                # Проверка на допустимые часы (0-23)
                if start_hour < 0 or start_hour > 23:
                    messagebox.showerror("Ошибка", "Введено неверное время. Часы должны быть в пределах от 0 до 23.")
                    return

                start_date_str = self.calendar.get_date()
                start_time = datetime.datetime.strptime(start_date_str, "%d.%m.%Y") + datetime.timedelta(hours=start_hour)
                end_time = start_time + datetime.timedelta(hours=estimated_time)
                priority = int(priority_entry.get())

                task = Task(title, description, estimated_time, start_time, end_time, priority)
                self.scheduler.add_task(task)
                self.update_task_display()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректный ввод данных: {str(e)}")

        save_button = ctk.CTkButton(dialog, text="Сохранить", command=save_task)
        save_button.grid(row=5, columnspan=2, pady=10)

    def edit_task(self):
        """
        Открывает диалоговое окно для редактирования выбранной задачи.
        Если задача выбрана, данные обновляются и отображаются в интерфейсе.
        """
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Задача не выбрана.")
            return

        item = self.task_tree.item(selected_item)
        task_data = item['values']
        
        try:
            start_hour = datetime.datetime.strptime(task_data[3], "%d.%m.%Y %H:%M").hour
        except ValueError:
            messagebox.showerror("Ошибка", "Задача не выбрана.")
            return

        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Редактирование задачи")
        dialog.geometry("400x300")
        dialog.grid_rowconfigure(0, weight=1)
        dialog.grid_rowconfigure(1, weight=1)
        dialog.grid_rowconfigure(2, weight=1)
        dialog.grid_rowconfigure(3, weight=1)
        dialog.grid_rowconfigure(4, weight=1)
        dialog.grid_rowconfigure(5, weight=1)
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(dialog, text="Название задачи:").grid(row=0, column=0, sticky="ew")
        title_entry = ctk.CTkEntry(dialog)
        title_entry.insert(0, task_data[0])
        title_entry.grid(row=0, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Описание:").grid(row=1, column=0, sticky="ew")
        description_entry = ctk.CTkEntry(dialog)
        description_entry.insert(0, task_data[1])
        description_entry.grid(row=1, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Оценка времени (ч):").grid(row=2, column=0, sticky="ew")
        estimated_time_entry = ctk.CTkEntry(dialog)
        estimated_time_entry.insert(0, task_data[2])
        estimated_time_entry.grid(row=2, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Приоритет:").grid(row=3, column=0, sticky="ew")
        priority_entry = ctk.CTkEntry(dialog)
        priority_entry.insert(0, task_data[5])
        priority_entry.grid(row=3, column=1, sticky="ew")

        ctk.CTkLabel(dialog, text="Часы начала (0-23):").grid(row=4, column=0, sticky="ew")
        start_hour_entry = ctk.CTkEntry(dialog)
        start_hour_entry.insert(0, start_hour)
        start_hour_entry.grid(row=4, column=1, sticky="ew")

        def update_task():
            """
            Обновляет задачу в планировщике и обновляет интерфейс с новыми данными.
            """
            try:
                title = title_entry.get()
                description = description_entry.get()
                estimated_time = float(estimated_time_entry.get())
                start_hour = int(start_hour_entry.get())

                # Проверка на допустимые часы (0-23)
                if start_hour < 0 or start_hour > 23:
                    messagebox.showerror("Ошибка", "Введено неверное время. Часы должны быть в пределах от 0 до 23.")
                    return

                start_date_str = self.calendar.get_date()
                start_time = datetime.datetime.strptime(start_date_str, "%d.%m.%Y") + datetime.timedelta(hours=start_hour)
                end_time = start_time + datetime.timedelta(hours=estimated_time)
                priority = int(priority_entry.get())

                task_index = self.scheduler.tasks.index(self.scheduler.get_tasks_for_date(start_time.date())[0])
                self.scheduler.tasks[task_index] = Task(title, description, estimated_time, start_time, end_time, priority)
                self.update_task_display()
                dialog.destroy()
            except ValueError as e:
                messagebox.showerror("Ошибка", f"Некорректный ввод данных: {str(e)}")

        update_button = ctk.CTkButton(dialog, text="Сохранить изменения", command=update_task)
        update_button.grid(row=5, columnspan=2, pady=10)

    def delete_task(self):
        """
        Удаляет выбранную задачу из планировщика.
        Если задача не выбрана или не найдена, выводится сообщение об ошибке.
        """
        selected_item = self.task_tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Задача не выбрана.")
            return

        item = self.task_tree.item(selected_item)
        task_data = item['values']

        start_time_str = task_data[3]  # строка вида 'дд.мм.гггг чч:мм'
        try:
            start_time = datetime.datetime.strptime(start_time_str, "%d.%m.%Y %H:%M")
        except ValueError:
            messagebox.showerror("Ошибка", "Задача не выбрана.")
            return
        
        tasks_for_date = self.scheduler.get_tasks_for_date(start_time.date())
        if not tasks_for_date:
            print("Нет задач на выбранную дату.")
            messagebox.showerror("Ошибка", "Нет задач на выбранную дату.")
            return

        task_to_delete = None
        for task in tasks_for_date:
            if task.title.strip(',') == str(task_data[0]).strip(',') and task.start_time == start_time:
                task_to_delete = task
                break

        if task_to_delete:
            self.scheduler.delete_task(task_to_delete)
            self.update_task_display()
        else:
            messagebox.showerror("Ошибка", "Задача не найдена.")

    def update_task_display(self, event=None):
        """
        Обновляет отображение задач в интерфейсе на основе выбранной даты в календаре.
        """
        selected_date = self.calendar.get_date()
        date_obj = datetime.datetime.strptime(selected_date, "%d.%m.%Y").date()
        self.task_tree.delete(*self.task_tree.get_children())

        tasks_for_date = self.scheduler.get_tasks_for_date(date_obj)
        if tasks_for_date:
            for task in sorted(tasks_for_date):
                display_text = (
                    task.title,
                    task.description,
                    task.estimated_time,
                    task.start_time.strftime('%d.%m.%Y %H:%M'),
                    task.end_time.strftime('%d.%m.%Y %H:%M'),
                    task.priority
                )
                self.task_tree.insert("", "end", values=display_text)
        else:
            self.task_tree.insert("", "end", values=("Нет задач на выбранную дату.", "", "", "", "", ""))