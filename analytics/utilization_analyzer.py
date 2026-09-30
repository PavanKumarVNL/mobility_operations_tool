from collections import defaultdict


class UtilizationAnalyzer:

    def __init__(self, activities, high_threshold=70, medium_threshold=40):
        self.activities = activities
        self.high_threshold = high_threshold
        self.medium_threshold = medium_threshold

    def _group_by_driver(self):

        activity_by_driver = defaultdict(list)

        for activity in self.activities:
            activity_by_driver[activity.driver_id].append(activity)

        for driver_id in activity_by_driver:
            activity_by_driver[driver_id].sort(
                key=lambda activity: activity.timestamp
            )

        return activity_by_driver

    def get_driver_utilization(self, driver_id):

        activity_by_driver = self._group_by_driver()

        driver_activities = activity_by_driver.get(
            driver_id,
            []
        )

        online_seconds = 0
        busy_seconds = 0
        idle_seconds = 0

        for i in range(len(driver_activities) - 1):

            current = driver_activities[i]
            next_activity = driver_activities[i + 1]

            duration = (
                next_activity.timestamp -
                current.timestamp
            ).total_seconds()

            if current.is_online():
                online_seconds += duration

            elif current.is_busy():
                busy_seconds += duration

            elif current.is_idle():
                idle_seconds += duration

        online_hours = online_seconds / 3600
        busy_hours = busy_seconds / 3600
        idle_hours = idle_seconds / 3600

        available_seconds = busy_seconds + idle_seconds

        utilization = (
            busy_seconds / available_seconds * 100
            if available_seconds > 0
            else 0
        )

        classification = self._classify_utilization(
            utilization
        )

        return {
            "driver_id": driver_id,
            "online_hours": online_hours,
            "busy_hours": busy_hours,
            "idle_hours": idle_hours,
            "utilization": utilization,
            "classification": classification
        }

    def _classify_utilization(self, utilization):

        if utilization >= self.high_threshold:
            return "High"

        if utilization >= self.medium_threshold:
            return "Medium"

        return "Low"

    def get_all_driver_utilization(self):

        driver_ids = {
            activity.driver_id
            for activity in self.activities
        }

        return [
            self.get_driver_utilization(driver_id)
            for driver_id in driver_ids
        ]