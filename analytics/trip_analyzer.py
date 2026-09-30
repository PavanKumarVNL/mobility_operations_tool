class TripAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def total_trips(self):
        return len(self.trips)

    def completed_trips(self):
        return [
            trip
            for trip in self.trips
            if trip.is_completed()
        ]

    def cancelled_trips(self):
        return [
            trip
            for trip in self.trips
            if trip.is_cancelled()
        ]

    def completion_rate(self):
        total = self.total_trips()

        if total == 0:
            return 0

        completed = len(self.completed_trips())

        return (completed / total) * 100

    def cancellation_rate(self):
        total = self.total_trips()

        if total == 0:
            return 0

        cancelled = len(self.cancelled_trips())

        return (cancelled / total) * 100

    def total_revenue(self):
        return sum(
            trip.fare
            for trip in self.completed_trips()
        )

    def average_fare(self):
        completed = self.completed_trips()

        if not completed:
            return 0

        return sum(
            trip.fare
            for trip in completed
        ) / len(completed)

    def average_distance(self):
        completed = self.completed_trips()

        if not completed:
            return 0

        return sum(
            trip.distance_km
            for trip in completed
        ) / len(completed)

    def average_duration(self):
        durations = []

        for trip in self.completed_trips():
            duration = trip.calculate_duration()

            if duration is not None:
                durations.append(duration)

        if not durations:
            return 0

        return sum(durations) / len(durations)

    def get_summary(self):
        return {
            "total_trips": self.total_trips(),
            "completed_trips": len(self.completed_trips()),
            "cancelled_trips": len(self.cancelled_trips()),
            "completion_rate": self.completion_rate(),
            "cancellation_rate": self.cancellation_rate(),
            "total_revenue": self.total_revenue(),
            "average_fare": self.average_fare(),
            "average_distance": self.average_distance(),
            "average_duration": self.average_duration(),
            "total_riders": self.total_riders(),
        }
    def total_riders(self):
        return len({
            trip.rider_id
            for trip in self.trips
        })