import logging
import threading
import random
import time
from contextlib import contextmanager

logging.basicConfig(level='INFO')
logger = logging.getLogger(__name__)

class ForkManager:
    def __init__(self, left_fork, right_fork):
        self.left_fork = left_fork
        self.right_fork = right_fork
    
    @contextmanager
    def acquire_forks(self):
        self.left_fork.acquire()
        logger.info(f'Philosopher {threading.current_thread().getName()} acquired left fork')
        try:
            self.right_fork.acquire()
            logger.info(f'Philosopher {threading.current_thread().getName()} acquired right fork')
            yield
        finally:
            self.right_fork.release()
            self.left_fork.release()

class Philosopher(threading.Thread):
    running = True

    def __init__(self, left_fork: threading.Lock, right_fork: threading.Lock):
        super().__init__()
        self.fork_manager = ForkManager(left_fork, right_fork)

    def run(self):
        while self.running:
            logger.info(f'Philosopher {self.getName()} start thinking.')
            time.sleep(random.randint(1, 10))
            logger.info(f'Philosopher {self.getName()} is hungry.')
            
            with self.fork_manager.acquire_forks():
                self.dining()

    def dining(self):
        logger.info(f'Philosopher {self.getName()} starts eating.')
        time.sleep(random.randint(1, 10))
        logger.info(f'Philosopher {self.getName()} finishes eating and leaves to think.')

def main():
    forks = [threading.Lock() for _ in range(5)]
    philosophers = [
        Philosopher(forks[i % 5], forks[(i + 1) % 5])
        for i in range(5)
    ]
    Philosopher.running = True
    for p in philosophers:
        p.start()
    time.sleep(200)
    Philosopher.running = False
    logger.info("Now we're finishing.")

if __name__ == "__main__":
    main()
