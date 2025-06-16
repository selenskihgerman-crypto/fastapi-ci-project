import logging
import random
import threading
import time

TOTAL_TICKETS = 10
MAX_TICKETS = 100
PRINT_THRESHOLD = 4

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Seller(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        self.tickets_sold = 0
        logger.info('Seller started work')

    def run(self):
        global TOTAL_TICKETS
        is_running = True
        while is_running:
            self.random_sleep()
            with self.sem:
                if TOTAL_TICKETS <= 0:
                    break
                self.tickets_sold += 1
                TOTAL_TICKETS -= 1
                logger.info(f'{self.getName()} sold one; {TOTAL_TICKETS} left')
        logger.info(f'Seller {self.getName()} sold {self.tickets_sold} tickets')

    def random_sleep(self):
        time.sleep(random.randint(0, 1))

class Director(threading.Thread):
    def __init__(self, semaphore: threading.Semaphore):
        super().__init__()
        self.sem = semaphore
        logger.info('Director started work')

    def run(self):
        global TOTAL_TICKETS
        while True:
            with self.sem:
                if TOTAL_TICKETS <= PRINT_THRESHOLD and TOTAL_TICKETS + 6 <= MAX_TICKETS:
                    added = min(6, MAX_TICKETS - TOTAL_TICKETS)
                    TOTAL_TICKETS += added
                    logger.info(f'Director added {added} tickets; Total now {TOTAL_TICKETS}')
                elif TOTAL_TICKETS <= 0:
                    break
            time.sleep(1)

def main():
    semaphore = threading.Semaphore()
    sellers = []
    
    for _ in range(3):
        seller = Seller(semaphore)
        seller.start()
        sellers.append(seller)
    
    director = Director(semaphore)
    director.start()
    
    for seller in sellers:
        seller.join()
    
    director.join()

if __name__ == '__main__':
    main()
