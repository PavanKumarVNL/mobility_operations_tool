class ZoneAnalyzer:

    def __init__(self, trips):
        self.trips = trips

    def get_zone_metrics(self, city, zone):

        zone_trips = [
            trip
            for trip in self.trips
            if trip.city == city
            and trip.pickup_zone == zone
        ]

        completed_trips = [
            trip
            for trip in zone_trips
            if trip.is_completed()
        ]

        cancelled_trips = [
            trip
            for trip in zone_trips
            if trip.is_cancelled()
        ]

        revenue = sum(
            trip.fare
            for trip in completed_trips
        )

        average_fare = (
            revenue / len(completed_trips)
            if completed_trips
            else 0
        )

        cancellation_rate = (
            len(cancelled_trips) / len(zone_trips) * 100
            if zone_trips
            else 0
        )

        return {
            "city": city,
            "zone": zone,
            "total_trips": len(zone_trips),
            "completed_trips": len(completed_trips),
            "cancelled_trips": len(cancelled_trips),
            "cancellation_rate": cancellation_rate,
            "revenue": revenue,
            "average_fare": average_fare
        }

    def get_all_zone_metrics(self):

        zones = set()

        for trip in self.trips:
            zones.add(
                (trip.city, trip.pickup_zone)
            )

        zone_metrics = []

        for city, zone in zones:

            metrics = self.get_zone_metrics(
                city,
                zone
            )

            zone_metrics.append(metrics)

        return zone_metrics