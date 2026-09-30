from collections import defaultdict


class CancellationAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def total_cancellations(self):
        return sum(
            1
            for trip in self.trips
            if trip.is_cancelled()
        )

    def by_reason(self):

        reason_counts = defaultdict(int)

        for trip in self.trips:

            if trip.is_cancelled():

                reason = trip.cancellation_reason

                if not reason:
                    reason = "Unknown"

                reason_counts[reason] += 1

        return dict(
            sorted(
                reason_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    def by_zone(self):

        zone_counts = defaultdict(int)

        for trip in self.trips:

            if trip.is_cancelled():

                key = (
                    trip.city,
                    trip.pickup_zone
                )

                zone_counts[key] += 1

        return [
            {
                "city": city,
                "zone": zone,
                "cancelled_trips": count
            }
            for (city, zone), count
            in sorted(
                zone_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        ]

    def by_driver(self):

        driver_counts = defaultdict(int)

        for trip in self.trips:

            if trip.is_cancelled():
                driver_counts[trip.driver_id] += 1

        return dict(
            sorted(
                driver_counts.items(),
                key=lambda item: item[1],
                reverse=True
            )
        )

    def by_hour(self):

        hour_counts = defaultdict(int)

        for trip in self.trips:

            if trip.is_cancelled():

                hour = trip.request_time.hour

                hour_counts[hour] += 1

        return dict(
            sorted(
                hour_counts.items()
            )
        )

    def get_summary(self):

        return {
            "total_cancellations":
                self.total_cancellations(),

            "by_reason":
                self.by_reason(),

            "by_zone":
                self.by_zone(),

            "by_driver":
                self.by_driver(),

            "by_hour":
                self.by_hour()
        }