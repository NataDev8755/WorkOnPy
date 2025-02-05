import threading
import queue
import random
import time

# Задачи в офисе с приоритетами
class Task:
    def __init__(self, task_id, priority, description):
        self.task_id = task_id
        self.priority = priority
        self.description = description

    def __repr__(self):
        return f"Task {self.task_id} (Priority {self.priority}): {self.description}"

# Рабочий, который выполняет задачи
class Worker(threading.Thread):
    def __init__(self, worker_id, task_queue):
        threading.Thread.__init__(self)
        self.worker_id = worker_id
        self.task_queue = task_queue
        self.daemon = True

    def run(self):
        while True:
            # Блокируемся до получения задачи
            task = self.task_queue.get()
            if task is None:  # Завершаем поток
                break
            print(f"Worker {self.worker_id} is working on {task}")
            time.sleep(random.randint(1, 3))  # Время на выполнение задачи
            print(f"Worker {self.worker_id} finished {task}")
            self.task_queue.task_done()

# Менеджер, который создает задачи
class TaskManager:
    def __init__(self, num_workers):
        self.task_queue = queue.PriorityQueue()  # Очередь с приоритетами
        self.workers = []
        for i in range(num_workers):
            worker = Worker(i + 1, self.task_queue)
            self.workers.append(worker)
            worker.start()

    def create_task(self, task_id, priority, description):
        task = Task(task_id, priority, description)
        self.task_queue.put((priority, task))  # Задачи с более низким числом имеют более высокий приоритет
        print(f"Created {task}")

    def wait_for_completion(self):
        self.task_queue.join()  # Ожидаем, пока все задачи не будут выполнены

    def stop_workers(self):
        # Останавливаем всех работников
        for _ in self.workers:
            self.task_queue.put(None)

# Пример работы
if __name__ == "__main__":
    task_manager = TaskManager(num_workers=3)

    # Создаем задачи с разными приоритетами
    task_manager.create_task(1, priority=2, description="Prepare meeting agenda")
    task_manager.create_task(2, priority=1, description="Reply to emails")
    task_manager.create_task(3, priority=3, description="Write project report")
    task_manager.create_task(4, priority=1, description="Update documentation")
    task_manager.create_task(5, priority=2, description="Plan team building event")

    task_manager.wait_for_completion()  # Ожидаем завершения всех задач
    task_manager.stop_workers()  # Останавливаем рабочие потоки
    print("All tasks completed.")
