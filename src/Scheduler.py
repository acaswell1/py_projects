"""
Schedule tasks to occur at a given time
"""
import threading
import time
import schedule


class DailyDigestScheduler(threading.Thread):
    """
    Class which allows users to schedule tasks to occur
    """

    def __init__(self):
        super().__init__()
        self.__stop_running = threading.Event()

    def schedule_daily(self, hour, minute, job):
        """
        Schedule a daily task
        """
        schedule.clear()
        schedule.every().day.at(f'{hour:02d}:{minute:02d}').do(job)

    def run(self):
        """
        Execute scheduled tasks
        """
        self.__stop_running.clear()
        while not self.__stop_running.is_set():
            schedule.run_pending()
            time.sleep(1)

    def stop(self):
        """
        Stop scheduled tasks
        """
        self.__stop_running.set()


if __name__ == '__main__':
    from DailyDigestEmail import DailyDigestEmail as Email
    email = Email()

    scheduler = DailyDigestScheduler()
    scheduler.start()


    hour = time.localtime().tm_hour
    minute = time.localtime().tm_min + 1
    print(f'Scheduling email test for {hour:02d}:{minute:02d}')
    scheduler.schedule_daily(hour, minute, email.send_email)

    time.sleep(60)
    scheduler.stop()
