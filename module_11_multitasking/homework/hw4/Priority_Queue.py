import threading
import time
import random
from queue import PriorityQueue

class Task:
    def __init__(self, priority, func, *args):
        self.priority = priority
        self.func = func
        self.args = args
    
    def __lt__(self, other):
        return self.priority < other.priority
    
    def __repr__(self):
        return f"Task(priority={self.priority}). {self.func.__name__}({', '.join(map(str, self.args))})"

class Producer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    
    def run(self):
        print("Producer: Running")
        for i in range(10):
            priority = random.randint(0, 10)
            delay = random.random()
            task = Task(priority, time.sleep, delay)
            self.queue.put((priority, task))
            print(f">added {task}")
        print("Producer: Done")

class Consumer(threading.Thread):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
    
    def run(self):
        print("Consumer: Running")
        while True:
            item = self.queue.get()
            if item is None:
                break
            priority, task = item
            print(f">running {task}")
            task.func(*task.args)
            self.queue.task_done()
        print("Consumer: Done")

def main():
    queue = PriorityQueue()
    producer = Producer(queue)
    consumer = Consumer(queue)
    
    producer.start()
    consumer.start()
    
    producer.join()
    queue.put(None)  # Сигнал завершения
    consumer.join()

if __name__ == "__main__":
    main()
