class Task:
    """
    Класс для представления задачи в планировщике.
    Задача содержит информацию о названии, описании, времени, приоритете и статусе.

    Атрибуты:
        title (str): Название задачи.
        description (str): Описание задачи.
        estimated_time (float): Оценка времени для выполнения задачи (в часах).
        start_time (datetime): Время начала задачи.
        end_time (datetime): Время окончания задачи.
        priority (int): Приоритет задачи.
        status (str): Статус задачи, по умолчанию "в процессе".
    """
    
    def __init__(self, title, description, estimated_time, start_time, end_time, priority):
        """
        Инициализация задачи с указанными параметрами.

        :param title: Название задачи.
        :param description: Описание задачи.
        :param estimated_time: Оценка времени (в часах) для выполнения задачи.
        :param start_time: Время начала задачи (тип: datetime).
        :param end_time: Время окончания задачи (тип: datetime).
        :param priority: Приоритет задачи (целое число).
        """
        self.title = title
        self.description = description
        self.estimated_time = estimated_time
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority
        self.status = "в процессе"

    def __lt__(self, other):
        """
        Метод для сравнения задач по времени начала.

        :param other: Другая задача для сравнения.
        :return: True, если время начала текущей задачи меньше времени начала другой задачи.
        """
        return self.start_time < other.start_time
