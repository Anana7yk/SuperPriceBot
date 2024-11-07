import time

class Scheduler:
    def __init__(self, notification_manager):
        self.notification_manager = notification_manager

    def start(self):
        while True:
            self.notification_manager.check_prices()
            time.sleep(3600)