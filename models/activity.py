from datetime import datetime


class DriverActivity:
    def __init__(self, driver_id, timestamp, status):
        self.driver_id = driver_id
        self.timestamp = datetime.strptime(
            timestamp,
            "%Y-%m-%d %H:%M:%S"
        )
        self.status = status

    def is_online(self):
        return self.status == "Online"

    def is_busy(self):
        return self.status == "Busy"

    def is_idle(self):
        return self.status == "Idle"

    def is_offline(self):
        return self.status == "Offline"